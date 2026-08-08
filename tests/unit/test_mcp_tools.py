"""Tests for MCP tool listing and dispatch against a real in-process server."""

import asyncio
import json
import socket
import time

import pytest
from fastmcp import Client, FastMCP
from fastmcp.server.auth.providers.debug import DebugTokenVerifier

from tagopen.config import settings
from tagopen.tools import registry
from tagopen.tools.builtins import BUILTIN_TOOLS
from tagopen.tools.registry import dispatch_tool, get_channel_tools

TEST_TOKEN = "test-bearer-token"
CHANNEL = "C_MCP"

BUILTIN_NAMES = {t["function"]["name"] for t in BUILTIN_TOOLS}


def _free_port() -> int:
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


@pytest.fixture
async def mcp_server_url():
    """Run a bearer-token-protected FastMCP server in-process; yield its URL."""
    server = FastMCP("testsrv", auth=DebugTokenVerifier(validate=lambda t: t == TEST_TOKEN))

    @server.tool(task=True)
    async def echo(text: str) -> dict:
        """Echo the input back."""
        return {"echoed": text}

    @server.tool
    async def add(a: int, b: int) -> dict:
        """Add two integers."""
        return {"sum": a + b}

    port = _free_port()
    run = asyncio.create_task(server.run_http_async(host="127.0.0.1", port=port, show_banner=False))
    url = f"http://127.0.0.1:{port}/mcp"

    deadline = time.monotonic() + 15
    while True:
        try:
            async with Client(url, auth=TEST_TOKEN) as client:
                await client.list_tools()
            break
        except Exception:
            if time.monotonic() > deadline:
                run.cancel()
                raise
            await asyncio.sleep(0.05)

    yield url

    run.cancel()
    try:
        await run
    except (asyncio.CancelledError, Exception):
        pass


@pytest.fixture
def write_tools_toml(tmp_path, monkeypatch):
    """Point the channel dir at tmp_path and return a tools.toml writer."""
    monkeypatch.setattr(settings, "data_dir", tmp_path)
    monkeypatch.setenv("MCP_TEST_TOKEN", TEST_TOKEN)
    registry._tool_configs.clear()

    def write(text: str) -> None:
        path = tmp_path / "channels" / CHANNEL / "tools.toml"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)
        registry._tool_configs.clear()

    return write


def _server_entry(url: str, extra: str = "") -> str:
    return f'''
[[mcp_server]]
name = "testsrv"
url = "{url}"
auth_env = "MCP_TEST_TOKEN"
{extra}
'''


async def test_mcp_tools_listed_namespaced_and_schema_shaped(mcp_server_url, write_tools_toml):
    write_tools_toml(_server_entry(mcp_server_url))

    tools = await get_channel_tools(CHANNEL)
    names = {t["function"]["name"] for t in tools}

    assert BUILTIN_NAMES <= names  # built-ins always present
    assert {"testsrv__echo", "testsrv__add"} <= names

    echo = next(t for t in tools if t["function"]["name"] == "testsrv__echo")
    assert echo["type"] == "function"
    assert echo["function"]["description"]
    params = echo["function"]["parameters"]
    assert params["type"] == "object"
    assert "text" in params["properties"]


async def test_authorized_dispatch_returns_tool_result(mcp_server_url, write_tools_toml):
    write_tools_toml(_server_entry(mcp_server_url))

    result = await dispatch_tool("testsrv__echo", {"text": "hello"}, channel_id=CHANNEL)
    assert json.loads(result) == {"echoed": "hello"}


async def test_wrong_token_yields_error_string(mcp_server_url, write_tools_toml, monkeypatch):
    write_tools_toml(_server_entry(mcp_server_url))
    monkeypatch.setenv("MCP_TEST_TOKEN", "wrong-token")

    # Listing degrades to built-ins only — no exception escapes
    tools = await get_channel_tools(CHANNEL)
    assert {t["function"]["name"] for t in tools} == BUILTIN_NAMES

    # Dispatch returns an honest error string, not an exception
    result = await dispatch_tool("testsrv__echo", {"text": "hi"}, channel_id=CHANNEL)
    assert isinstance(result, str)
    assert "unauthorized" in result.lower()


async def test_missing_auth_env_yields_error_string(mcp_server_url, write_tools_toml, monkeypatch):
    write_tools_toml(_server_entry(mcp_server_url))
    monkeypatch.delenv("MCP_TEST_TOKEN")

    tools = await get_channel_tools(CHANNEL)
    assert {t["function"]["name"] for t in tools} == BUILTIN_NAMES

    result = await dispatch_tool("testsrv__echo", {"text": "hi"}, channel_id=CHANNEL)
    assert isinstance(result, str)
    assert "MCP_TEST_TOKEN" in result and "not set" in result


async def test_allowed_tools_filters_listing_and_dispatch(mcp_server_url, write_tools_toml):
    write_tools_toml(_server_entry(mcp_server_url, 'allowed_tools = ["echo"]'))

    tools = await get_channel_tools(CHANNEL)
    names = {t["function"]["name"] for t in tools}
    assert "testsrv__echo" in names
    assert "testsrv__add" not in names

    # Dispatch enforces the allowlist too, even if the model hallucinates the call
    result = await dispatch_tool("testsrv__add", {"a": 1, "b": 2}, channel_id=CHANNEL)
    assert isinstance(result, str)
    assert "allowed_tools" in result

    # The allowed tool still works
    result = await dispatch_tool("testsrv__echo", {"text": "ok"}, channel_id=CHANNEL)
    assert json.loads(result) == {"echoed": "ok"}


async def test_task_mode_dispatch_completes(mcp_server_url, write_tools_toml):
    write_tools_toml(_server_entry(mcp_server_url, "task_mode = true\ntimeout = 30"))

    result = await dispatch_tool("testsrv__echo", {"text": "background"}, channel_id=CHANNEL)
    assert json.loads(result) == {"echoed": "background"}


async def test_unknown_tool_still_reports_not_found(write_tools_toml):
    write_tools_toml("")  # no MCP servers configured

    result = await dispatch_tool("nosuch__tool", {}, channel_id=CHANNEL)
    assert result == "Tool 'nosuch__tool' not found."
