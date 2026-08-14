<h1 align="center">Open Claude Tag — The open-source Claude Tag alternative</h1>

> 🔥 **Claude Tag launched June 23, 2026** — Anthropic's always-on AI teammate that lives in Slack, learns your company, and works autonomously. It's closed, paid, locked to Anthropic, and cloud-only. This is the open-source alternative: self-hostable, LLM-agnostic, and channel-native.

<p align="center">
  <a href="https://github.com/Anil-matcha/open-claude-tag/blob/main/LICENSE"><img alt="license" src="https://img.shields.io/badge/license-MIT-blue.svg?style=flat" /></a>
  <a href="https://www.python.org/"><img alt="python" src="https://img.shields.io/badge/python-3.11%2B-blue?style=flat&logo=python&logoColor=white" /></a>
  <img alt="llm-agnostic" src="https://img.shields.io/badge/LLM-agnostic-6366f1?style=flat" />
  <img alt="mcp-native" src="https://img.shields.io/badge/MCP-native-10b981?style=flat" />
  <a href="https://discord.gg/s7KW4fsqXK"><img alt="discord" src="https://img.shields.io/badge/discord-join-5865F2?style=flat&logo=discord&logoColor=white" /></a>
</p>

<p align="center">
  <a href="#quickstart">Quickstart</a> ·
  <a href="#how-it-works">How it works</a> ·
  <a href="#channel-configuration">Channel config</a> ·
  <a href="#supported-llms">LLMs</a> ·
  <a href="#roadmap">Roadmap</a> ·
  <a href="https://discord.gg/s7KW4fsqXK">Discord</a>
</p>

---

**Open Claude Tag** is a free, self-hostable AI teammate for Slack that works the way Claude Tag does — one shared agent per channel, persistent memory, skill auto-creation, ambient monitoring — without Anthropic's paywall, without cloud lock-in, without the single-vendor constraint.

> Most Slack AI bots are personal assistants — one context per user, isolated DMs. Open Claude Tag flips this: **one agent per channel, shared by the whole team.** Everyone sees the same context, picks up mid-thread, and the agent knows who said what.

**Community:** Join [Reddit](https://reddit.com/r/muapi) & [Discord](https://discord.gg/s7KW4fsqXK) for discussions and support.
**Follow** the [creator](https://x.com/matchaman11) for updates.

### Related projects

> **Open-source AI design agent — alternative to Lovart AI, Runway Agent, Luma Labs Agent** → https://github.com/Anil-matcha/Open-AI-Design-Agent

> **Open-source multi-modal chatbot and Poe alternative** → https://github.com/Anil-matcha/Open-Poe-AI

> **Open-source AI voice agent for sales calls and customer support** → https://github.com/Anil-matcha/AI-Voice-Agent

<p align="center">
  <a href="https://github.com/Anil-matcha/awesome-generative-ai-apps">
    <img src="https://img.shields.io/badge/Part%20of-Awesome%20Generative%20AI%20Apps-FFD700?style=for-the-badge&logo=github&logoColor=black" alt="Awesome Generative AI Apps">
  </a>
</p>

> 🤖 **[Explore 50+ more open-source AI apps →](https://github.com/Anil-matcha/awesome-generative-ai-apps)**

---

## Why Open Claude Tag

> **On June 23, 2026, Anthropic released Claude Tag** — the first AI that joins Slack as a shared channel teammate rather than a personal DM bot. It went viral. But it stayed closed-source, paid-only, cloud-only, locked to Claude models, and locked to Anthropic's access control model. No self-host, no BYOK for other providers, no custom tool integrations without Anthropic's approval.

Open Claude Tag is the open-source alternative. Same channel-native mental model, none of the lock-in:

- 🏢 **Channel-scoped, not user-scoped.** One agent per channel, shared by the whole team. All users see the same context, pick up mid-thread.
- 🤖 **LLM-agnostic.** Use Claude, GPT-4o, Gemini, Groq, or local Ollama. Swap with one env var. Different channels can use different models.
- 💾 **Agent-curated memory.** After each conversation, the agent decides what's worth keeping in `MEMORY.md`. No noisy append-only logs.
- 🧠 **Skill auto-creation.** After complex multi-step tasks, the agent writes a `SKILL.md` capturing what it learned. Institutional knowledge accumulates automatically.
- 🔔 **Ambient monitoring.** Configurable heartbeat: the agent proactively surfaces stale threads, approaching deadlines, and forgotten questions.
- 🔌 **MCP-native tools.** Plug in any MCP server per channel. Admins control exactly what each channel's agent can access.
- 📁 **File-based config.** Each channel is a directory of Markdown files. Version-controllable, auditable, no UI required.
- 🔒 **Self-hostable.** Your Slack data stays on your infrastructure. No round-trips to Anthropic's cloud.

### Comparison

| | Claude Tag (Anthropic) | OpenClaw / Hermes | **Open Claude Tag** |
|---|---|---|---|
| Open source | ❌ | ✅ | **✅ MIT** |
| Self-hostable | ❌ | ✅ | **✅** |
| Channel-scoped shared agent | ✅ | ❌ (per-user) | **✅** |
| Multi-user attribution | ✅ | ❌ | **✅** |
| Agent-curated memory | ✅ | Append-only | **✅ Letta inner loop** |
| Skill auto-creation | ❌ | ✅ (Hermes) | **✅** |
| Ambient / proactive mode | ✅ | ❌ | **✅ heartbeat cron** |
| LLM-agnostic | ❌ (Claude only) | ✅ | **✅ LiteLLM** |
| MCP-native tools | ✅ | Partial | **✅** |
| Per-channel model override | ❌ | ❌ | **✅** |
| Per-channel tool scoping | ✅ | ❌ | **✅ tools.toml** |
| Token budget controls | ✅ | ❌ | **✅ BUDGET.md** |
| Discord / Teams support | ❌ (Slack only) | ✅ | Roadmap |
| Pricing | Enterprise + Team plan | Free | **Free** |

---

## How it Works

### The core inversion

Every other Slack bot keys sessions on `user_id`. Open Claude Tag keys sessions on `(workspace_id, channel_id)`. That one change is what makes it feel like a teammate rather than a chatbot.

```
[#engineering channel]

@alice  Can you review the PR for the auth refactor?
@agent  Sure. I pulled the PR — looks good overall, one concern:
        the session expiry logic on line 42 doesn't handle clock skew.
        @bob you mentioned this pattern in the DB migration last week —
        does the same fix apply here?
@bob    Yeah, add a 5s leeway. Same as auth/session.py:L88
@agent  Got it. Adding to MEMORY.md: "session expiry: always add 5s
        leeway for clock skew (pattern from auth/session.py:L88)"
```

Every user in the channel sees the same thread. The agent knows who said what, follows up with the right person, and decides what's worth remembering.

### Agent loop

```
Slack @mention
       │
       ▼
  Channel Router ──── (workspace_id + channel_id) → AgentSession
       │                  ↑ serialized lock: no parallel writes to context
       ▼
  Context Assembler
  ├── CHANNEL.md       (identity, purpose, tone)
  ├── MEMORY.md        (agent-curated facts, always in context)
  ├── skills/*.md      (auto-created playbooks, loaded on semantic match)
  └── Last 50 messages (with @username attribution)
       │
       ▼
  Agent Loop  (ReAct + tool-use via LiteLLM)
  ├── Tool Registry  ← MCP servers defined in tools.toml
  ├── Built-in tools ← web search, Python runner, channel search
  └── Stream reply → Slack thread
       │
       ├── Memory curation turn  ← agent decides what to write to MEMORY.md
       │   (Letta inner-loop: model gets one extra turn to curate)
       │
       └── Skill evaluator  ← ≥5 tool calls? write SKILL.md
           (Hermes pattern: agent authors its own playbooks)
       │
       ▼
  SQLite + FTS5  (per-workspace DB, channel-isolated, WAL mode)
       │
       ▼
  Ambient Engine  (background — Phase 3)
  ├── Per-channel APScheduler crons
  ├── Heartbeat evaluator: "anything worth surfacing?"
  └── Proactive Slack post if yes, SILENT if no
```

### Memory architecture

```
Layer 1 — Context window (always loaded)
  CHANNEL.md + MEMORY.md + active SKILL.md files + last 50 messages

Layer 2 — Session store (SQLite + FTS5, per workspace)
  Full message history with user_id, timestamps, thread_ts
  Full-text search: "what did we decide about X last month?"

Layer 3 — Semantic recall (Mem0, Phase 2)
  Embeddings over key decisions and facts
  Namespace = channel_id (fully isolated per channel)

Layer 4 — Skill library (per channel)
  Auto-created after complex tasks (≥5 tool calls)
  Loaded into context when task description matches
  Curated weekly: stale after 30d, archived after 90d
```

### Ambient heartbeat

The heartbeat evaluator runs on a configurable cron per channel. It dumps recent activity to the LLM and asks: "anything worth surfacing?" It only posts if there's genuine value — stale threads, approaching deadlines, forgotten questions, spotted risks. Otherwise: `SILENT`.

The agent can also create its own monitoring tasks via `schedule_task(cron, description)` — it decides what's worth checking and when.

---

## Quickstart

### Prerequisites

- Python 3.11+
- A Slack app with Socket Mode enabled ([create one here](https://api.slack.com/apps))
- An API key for your preferred LLM provider (Anthropic, OpenAI, Gemini, or Groq)

### 1. Create the Slack app

1. Go to [api.slack.com/apps](https://api.slack.com/apps) → **Create New App** → From scratch
2. **Settings → Socket Mode**: enable it and generate an App-Level Token (`xapp-...`) with `connections:write` scope
3. **Event Subscriptions**: enable and subscribe to `app_mention` and `message.channels`
4. **OAuth & Permissions → Bot Token Scopes**: add `app_mentions:read`, `channels:history`, `channels:read`, `chat:write`, `reactions:write`, `users:read`
5. Install to workspace → copy the Bot Token (`xoxb-...`)

### 2. Install and configure

```bash
# Clone
git clone https://github.com/Anil-matcha/open-claude-tag
cd open-claude-tag

# Install
pip install -e .

# Configure
cp .env.example .env
```

Edit `.env`:

```bash
SLACK_BOT_TOKEN=xoxb-...
SLACK_APP_TOKEN=xapp-...

# Pick one LLM provider:
LLM_MODEL=claude-sonnet-4-6
ANTHROPIC_API_KEY=sk-ant-...

# or: LLM_MODEL=gpt-4o  +  OPENAI_API_KEY=sk-...
# or: LLM_MODEL=gemini/gemini-2.0-flash  +  GEMINI_API_KEY=...
# or: LLM_MODEL=ollama/llama3  (no key needed)
```

### 3. Configure your first channel

Get your channel ID: in Slack, right-click channel name → **View channel details** → scroll to the bottom.

```bash
mkdir -p data/channels/C01234ABC
cp channels/example/CHANNEL.md data/channels/C01234ABC/CHANNEL.md
# Edit CHANNEL.md to describe your channel's purpose and team
```

### 4. Run

```bash
tagopen
```

Then `@open-claude-tag` in your Slack channel.

---

## Channel Configuration

Each channel gets a directory of plain Markdown files under `data/channels/<channel_id>/`. Version-controllable, human-readable, no database required.

```
data/channels/C01234ABC/
  CHANNEL.md      ← identity, purpose, tone
  MEMORY.md       ← agent-maintained facts (auto-updated, don't edit manually)
  tools.toml      ← MCP servers and per-channel LLM override
  skills/         ← auto-created playbooks
    deploy-to-staging.md
    oncall-handoff.md
    pr-review-checklist.md
```

### CHANNEL.md

```markdown
# Engineering Channel

You are the engineering team's AI teammate in #engineering.

## Purpose
Help with deployments, code reviews, incident response, and architecture decisions.

## Tone
Technical, direct, concise. Use code blocks. Ask before triggering deploys.

## Team context
- Stack: Python backend, React frontend, PostgreSQL, AWS
- CI/CD via GitHub Actions
- We do not deploy on Fridays
```

### MEMORY.md — agent-curated facts

The agent writes this automatically. After each conversation it gets one internal LLM turn to decide what's worth persisting — using `memory_append` and `memory_replace` tools. Memory stays clean because the agent curates it, not a dumb append-only log.

Example of what accumulates over time:

```markdown
# Channel Memory

- Session expiry: always add 5s leeway for clock skew (auth/session.py:L88)
- We use squash-merge for all PRs — rebase main before merging
- Alice: infra questions. Bob: auth layer.
- Never restart worker pods on Fridays — cron runs at 11pm PT
```

### tools.toml — MCP servers and model override

```toml
# Per-channel LLM override (optional)
[llm]
model = "gpt-4o"

# MCP servers allowed in this channel
[[mcp_server]]
name = "github"
url = "mcp://localhost:3001"
allowed_tools = ["list_prs", "get_file", "create_comment", "trigger_workflow"]

[[mcp_server]]
name = "linear"
url = "mcp://localhost:3002"
allowed_tools = ["list_issues", "create_issue", "update_status"]
```

### Skills — auto-created institutional knowledge

After any task requiring 5+ tool calls, the agent writes a `SKILL.md`. Next time a similar task comes up, the skill loads into context automatically.

Example auto-created skill:

```markdown
---
name: deploy-to-staging
description: Deploy a service to staging via GitHub Actions
created: 2026-06-25
uses: 3
status: active
---

## When to use this
When someone asks to deploy a service to staging.

## Steps
1. Check CI is passing on the branch (github:list_prs)
2. Confirm with the requester before triggering
3. Trigger `deploy-staging` workflow (github:trigger_workflow)
4. Monitor the run for 2 minutes, post the staging URL

## Known gotchas
- No deploys on Fridays — check day of week first
- `worker` service uses a separate `deploy-worker` workflow
```

Skills lifecycle: active → stale (30d unused) → archived (90d). A weekly curator pass merges overlapping skills and patches outdated ones.

---

## Supported LLMs

Uses [LiteLLM](https://github.com/BerriAI/litellm) — one interface for every provider. Set `LLM_MODEL` and the matching key:

| Provider | `LLM_MODEL` | Key env var |
|---|---|---|
| Anthropic Claude (default) | `claude-sonnet-4-6` | `ANTHROPIC_API_KEY` |
| Anthropic Claude Opus | `claude-opus-4-8` | `ANTHROPIC_API_KEY` |
| Anthropic Claude Haiku | `claude-haiku-4-5-20251001` | `ANTHROPIC_API_KEY` |
| OpenAI GPT-4o | `gpt-4o` | `OPENAI_API_KEY` |
| OpenAI o3 | `o3` | `OPENAI_API_KEY` |
| Google Gemini | `gemini/gemini-2.0-flash` | `GEMINI_API_KEY` |
| Groq (fast open-weight) | `groq/llama-3.3-70b-versatile` | `GROQ_API_KEY` |
| Local Ollama | `ollama/llama3` | *(none needed)* |

**Per-channel model override** — run a lighter model in `#general`, a more powerful one in `#engineering`. Add to `data/channels/<id>/tools.toml`:

```toml
[llm]
model = "claude-opus-4-8"
```

---

## Built-in Tools

Always available in every channel — no configuration needed:

| Tool | What it does |
|---|---|
| `web_search` | DuckDuckGo instant search — no API key required |
| `run_python` | Execute Python snippets and return stdout (sandboxed) |
| `search_channel_history` | Full-text search across this channel's message history |
| `memory_append` | Append a fact to `MEMORY.md` |
| `memory_replace` | Update an outdated fact in `MEMORY.md` |

Add any other tool by listing an MCP server in `tools.toml`. Any MCP-compatible server works — GitHub, Linear, Notion, Jira, Datadog, PagerDuty, Sentry, etc.

---

## Development

```bash
# Install with dev dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Lint
ruff check .

# Type check
mypy tagopen/
```

### Project structure

```
tagopen/
  gateway/
    app.py       ← Slack Bolt async app, @mention handler
    router.py    ← channel router: (workspace_id, channel_id) → AgentSession
  agent/
    loop.py      ← ReAct agent loop, tool dispatch, memory + skill hooks
    context.py   ← system prompt assembler (CHANNEL.md + MEMORY.md + skills)
    skills.py    ← skill auto-creation after complex tasks
  memory/
    store.py     ← SQLite + FTS5 message store, channel-isolated
    writer.py    ← inner loop: agent curates MEMORY.md
  tools/
    registry.py  ← per-channel tool registry, reads tools.toml
    builtins.py  ← web search, Python runner, channel history search
  ambient/
    heartbeat.py ← proactive monitoring (Phase 3)
  llm.py         ← LiteLLM wrapper: key injection, per-channel model resolve
  config.py      ← settings from .env via pydantic-settings
  cli.py         ← entry point: tagopen
channels/
  example/       ← copy these to data/channels/<id>/ to get started
tests/
  unit/          ← channel isolation, SQLite store, router tests
PLAN.md          ← full architecture and design decisions
```

---

## Roadmap

- [x] **Phase 1** — Channel-native reactive teammate
  - [x] Slack Bolt async app, Socket Mode
  - [x] Channel router: `(workspace_id, channel_id)` → shared `AgentSession`
  - [x] Multi-user attribution in context window
  - [x] ReAct agent loop via LiteLLM
  - [x] SQLite + FTS5 per-channel message store
  - [x] File-based channel config (CHANNEL.md, MEMORY.md, tools.toml)
  - [x] Built-in tools: web search, Python runner, channel history search
  - [x] Per-channel model override
  - [x] Multi-provider: Anthropic, OpenAI, Gemini, Groq, Ollama
- [ ] **Phase 2** — Memory + Skills
  - [ ] Letta inner-loop memory curation (agent writes MEMORY.md)
  - [ ] Skill auto-creation (≥5 tool calls → SKILL.md)
  - [ ] Skill loader: semantic match to incoming task
  - [ ] Skill curator: weekly prune, stale/archived lifecycle
  - [ ] Mem0 semantic recall layer
- [ ] **Phase 3** — Ambient mode
  - [ ] Per-channel APScheduler heartbeat crons
  - [ ] LLM heartbeat evaluator (SILENT or post)
  - [ ] Stale thread detection
  - [ ] `schedule_task` tool: agent creates its own monitoring crons
  - [ ] Temporal for durable task orchestration
- [ ] **Phase 4** — Governance + Admin UI
  - [ ] Per-channel audit log (tokens spent, tools invoked)
  - [ ] Hard token budget enforcement via BUDGET.md
  - [ ] Next.js admin UI: channel config, tool access, budget view
- [ ] **Phase 5** — Multi-platform
  - [ ] Discord adapter
  - [ ] Microsoft Teams adapter

See [PLAN.md](PLAN.md) for full architecture decisions and research notes.

---

## Community

- 💬 **Discord** — questions, feature requests, show-and-tell → [discord.gg/s7KW4fsqXK](https://discord.gg/s7KW4fsqXK)
- 🐦 **X / Twitter** — updates and releases → [@matchaman11](https://x.com/matchaman11)
- 🐛 **GitHub Issues** — bug reports, feature requests → [Issues](https://github.com/Anil-matcha/open-claude-tag/issues)

---

## Contributing

Contributions welcome — especially:

| Want to ship… | Where |
|---|---|
| A new built-in tool | `tagopen/tools/builtins.py` + schema in `BUILTIN_TOOLS` |
| A new platform adapter (Discord, Teams) | `tagopen/gateway/` |
| Memory improvements | `tagopen/memory/` |
| Ambient mode (Phase 3) | `tagopen/ambient/heartbeat.py` |
| Example channel configs | `channels/` |
| Bug fixes | [Issues](https://github.com/Anil-matcha/open-claude-tag/issues) |

```bash
git clone https://github.com/Anil-matcha/open-claude-tag
cd open-claude-tag
pip install -e ".[dev]"
pytest && ruff check .
```

---

## Star history

<a href="https://star-history.dera.page/#Anil-matcha/open-claude-tag&Date">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://star-history.dera.page/svg?repos=Anil-matcha/open-claude-tag&type=Date&theme=dark" />
    <source media="(prefers-color-scheme: light)" srcset="https://star-history.dera.page/svg?repos=Anil-matcha/open-claude-tag&type=Date" />
    <img alt="Star history" src="https://star-history.dera.page/svg?repos=Anil-matcha/open-claude-tag&type=Date" />
  </picture>
</a>

---

## References

| Project | Role |
|---|---|
| [Claude Tag — Anthropic](https://www.anthropic.com/news/introducing-claude-tag) | The closed-source product this repo is the open-source alternative to |
| [OpenClaw](https://github.com/openclaw/openclaw) | Gateway architecture, workspace file pattern, multi-agent routing |
| [Hermes Agent](https://github.com/nousresearch/hermes-agent) | Skill auto-creation pattern, agent-managed crons, SQLite + FTS5 |
| [Letta (MemGPT)](https://github.com/letta-ai/letta) | Inner-loop memory curation, memory block tools |
| [LiteLLM](https://github.com/BerriAI/litellm) | Multi-provider LLM routing |

---

## License

MIT — free to use, modify, and self-host.

---

*This project is independent and not affiliated with Anthropic or Slack. References to third-party platforms are for interoperability and educational purposes. All trademarks are the property of their respective owners.*
