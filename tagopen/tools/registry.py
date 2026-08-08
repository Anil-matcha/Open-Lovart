"""Tool registry — loads allowed tools per channel from tools.toml.

Built-in tools are always available. Channel admins can add MCP servers via
``[[mcp_server]]`` entries in tools.toml. Each server's tools are listed over
the MCP protocol, converted to LiteLLM function schemas, and exposed to the
model namespaced as ``<server>__<tool>``.

Server entry schema (tools.toml)::

    [[mcp_server]]
    name = "github"                      # required — namespace prefix
    url = "https://example.com/mcp"      # required — HTTP(S) MCP endpoint
    auth_env = "GITHUB_MCP_TOKEN"        # optional — NAME of an env var holding
                                         #   a bearer token (resolved at connect
                                         #   time; no secret sits in tools.toml)
    allowed_tools = ["list_prs"]         # optional — allowlist; omit = all tools
    task_mode = false                    # optional — run tools as MCP background
                                         #   tasks (SEP-1686) and poll for the
                                         #   result instead of blocking the call
    timeout = 1200                       # optional — max seconds a single tool
                                         #   call may run (foreground call or
                                         #   background-task wait)

MCP failures never crash the agent loop: listing failures drop that server's
tools for the turn, and dispatch failures return a plain error string as the
tool result so the model can tell the user what went wrong.
"""

from __future__ import annotations

import json
import logging
import os
import time
from dataclasses import dataclass
from typing import Any

import httpx
import toml
from fastmcp import Client

from tagopen.config import settings
from tagopen.tools.builtins import BUILTIN_TOOLS, dispatch_builtin

logger = logging.getLogger(__name__)

# How long listed MCP tool schemas are reused before re-listing (seconds).
# A busy channel re-lists at most once per TTL; edits to tools.toml or
# server-side tool changes are picked up within this window.
MCP_TOOLS_TTL_SECONDS = 60.0

# Default cap on a single MCP tool call — a foreground call or a
# background-task wait. Override per server with `timeout` in tools.toml.
DEFAULT_TOOL_TIMEOUT_SECONDS = 1200.0

# Connect + list timeout while building a channel's schema — kept short so an
# unreachable server cannot stall message handling.
LIST_TOOLS_TIMEOUT_SECONDS = 15.0


@dataclass
class _ChannelTools:
    """Cached MCP tool schemas for one channel."""

    mcp_tools: list[dict]
    expires_at: float  # time.monotonic() deadline


# Cache of listed MCP tool schemas per channel
_tool_configs: dict[str, _ChannelTools] = {}


def _load_server_configs(channel_id: str) -> dict[str, dict]:
    """Parse ``[[mcp_server]]`` entries from the channel's tools.toml.

    Returns ``{server_name: entry}``. Invalid entries (missing name/url,
    non-HTTP url) are skipped with a warning. Never raises.
    """
    path = settings.channels_dir / channel_id / "tools.toml"
    if not path.exists():
        return {}
    try:
        config = toml.loads(path.read_text())
    except Exception:
        logger.exception("Failed to parse tools.toml for channel=%s", channel_id)
        return {}

    servers: dict[str, dict] = {}
    for entry in config.get("mcp_server", []):
        name, url = entry.get("name"), entry.get("url")
        if not name or not url:
            logger.warning(
                "Skipping [[mcp_server]] entry without name/url in channel=%s", channel_id
            )
            continue
        if not str(url).startswith(("http://", "https://")):
            logger.warning(
                "Skipping MCP server '%s' in channel=%s: only HTTP(S) URLs are supported, got %r",
                name,
                channel_id,
                url,
            )
            continue
        servers[str(name)] = entry
    return servers


def _resolve_auth(server: dict) -> tuple[str | None, str | None]:
    """Resolve the bearer token for a server entry.

    ``auth_env`` names an environment variable holding the token. Returns
    ``(token, error_message)`` — exactly one is set when auth is configured.
    """
    auth_env = server.get("auth_env")
    if not auth_env:
        return None, None
    token = os.environ.get(auth_env)
    if not token:
        return None, (
            f"MCP server '{server['name']}' requires a bearer token in environment "
            f"variable '{auth_env}', which is not set."
        )
    return token, None


async def _list_server_tools(name: str, server: dict) -> list[dict]:
    """Connect to one MCP server and return its tools as LiteLLM schemas."""
    token, auth_err = _resolve_auth(server)
    if auth_err:
        logger.warning("%s Skipping tool listing.", auth_err)
        return []

    allowed = server.get("allowed_tools")
    schemas: list[dict] = []
    async with Client(
        server["url"],
        auth=token,
        timeout=LIST_TOOLS_TIMEOUT_SECONDS,
        init_timeout=LIST_TOOLS_TIMEOUT_SECONDS,
    ) as client:
        for tool in await client.list_tools():
            if allowed is not None and tool.name not in allowed:
                continue
            schemas.append(
                {
                    "type": "function",
                    "function": {
                        "name": f"{name}__{tool.name}",
                        "description": tool.description or "",
                        "parameters": tool.inputSchema or {"type": "object", "properties": {}},
                    },
                }
            )
    return schemas


async def get_channel_tools(channel_id: str) -> list[dict]:
    """Return LiteLLM-compatible tool schemas for this channel.

    Built-ins are always included. MCP tools are listed live from each
    configured server and cached for MCP_TOOLS_TTL_SECONDS. A server that is
    unreachable or misconfigured contributes no tools for the turn — the agent
    keeps working with whatever else is available.
    """
    tools = list(BUILTIN_TOOLS)  # always include built-ins

    cached = _tool_configs.get(channel_id)
    if cached is not None and time.monotonic() < cached.expires_at:
        return tools + cached.mcp_tools

    mcp_tools: list[dict] = []
    for name, server in _load_server_configs(channel_id).items():
        try:
            listed = await _list_server_tools(name, server)
            mcp_tools.extend(listed)
            logger.debug(
                "MCP server '%s': %d tools listed for channel=%s", name, len(listed), channel_id
            )
        except Exception as e:
            logger.warning("MCP server '%s' unavailable for channel=%s: %s", name, channel_id, e)

    _tool_configs[channel_id] = _ChannelTools(
        mcp_tools=mcp_tools, expires_at=time.monotonic() + MCP_TOOLS_TTL_SECONDS
    )
    return tools + mcp_tools


async def dispatch_tool(fn_name: str, args: dict[str, Any], channel_id: str) -> Any:
    """Dispatch a tool call to built-ins or MCP servers."""
    if fn_name in {t["function"]["name"] for t in BUILTIN_TOOLS}:
        return await dispatch_builtin(fn_name, args)

    # Memory tools are handled directly in the agent loop
    if fn_name in ("memory_append", "memory_replace"):
        return None

    for name, server in _load_server_configs(channel_id).items():
        prefix = f"{name}__"
        if fn_name.startswith(prefix):
            return await _dispatch_mcp(name, server, fn_name[len(prefix) :], fn_name, args)

    logger.warning("Unknown tool: %s in channel=%s", fn_name, channel_id)
    return f"Tool '{fn_name}' not found."


async def _dispatch_mcp(
    server_name: str, server: dict, tool_name: str, fn_name: str, args: dict[str, Any]
) -> str:
    """Call one MCP tool. On any failure, return an honest error string.

    The allowed_tools allowlist is enforced here as well as at listing time,
    so a call to a filtered tool fails even if the model hallucinates it.
    In task_mode the call is submitted as an MCP background task and polled
    to completion, keeping long-running work off the request path.
    """
    allowed = server.get("allowed_tools")
    if allowed is not None and tool_name not in allowed:
        msg = f"Tool '{fn_name}' is not in this channel's allowed_tools for '{server_name}'."
        logger.warning("%s", msg)
        return msg

    token, auth_err = _resolve_auth(server)
    if auth_err:
        logger.warning("%s", auth_err)
        return auth_err

    timeout = float(server.get("timeout", DEFAULT_TOOL_TIMEOUT_SECONDS))
    try:
        async with Client(server["url"], auth=token) as client:
            if server.get("task_mode"):
                task = await client.call_tool(tool_name, args, task=True)
                await task.wait(timeout=timeout)
                result = await task.result()
            else:
                result = await client.call_tool(tool_name, args, timeout=timeout)
        return _render_result(result)
    except TimeoutError:
        msg = f"MCP tool '{fn_name}' timed out after {timeout:.0f}s."
    except httpx.HTTPStatusError as e:
        code = e.response.status_code
        if code in (401, 403):
            msg = (
                f"MCP server '{server_name}' rejected the call as unauthorized (HTTP {code}). "
                f"Check the token in the '{server.get('auth_env', '<unset>')}' env var."
            )
        else:
            msg = f"MCP server '{server_name}' returned HTTP {code} for '{fn_name}'."
    except Exception as e:
        msg = f"MCP tool '{fn_name}' failed: {e}"
    logger.warning("%s", msg)
    return msg


def _render_result(result: Any) -> str:
    """Render a CallToolResult for the model: structured content, else text."""
    if result.structured_content is not None:
        return json.dumps(result.structured_content, default=str)
    texts = [block.text for block in result.content if hasattr(block, "text")]
    return "\n".join(texts) if texts else "(empty result)"
