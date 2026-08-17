# Awesome DeepSeek Harness [![Awesome](https://awesome.re/badge.svg)](https://awesome.re)

> A curated guide to [DeepSeek Harness](https://github.com/deepseek-ai/deepseek-harness) (`dsh`) — DeepSeek's open-source, everything-is-a-plugin coding agent — and the best community plugins built on it.

DeepSeek Harness is a runnable coding agent (Web UI + headless) built on [Cordis](https://github.com/cordiverse/cordis), where every part of the system — models, tools, sandboxes, session storage, UI, even the agent loop itself — is a swappable plugin. That architecture has produced a large, fast-moving plugin ecosystem: well over a thousand community plugins at last count. This list exists to make that ecosystem easy to scan: what a plugin does, in one line, sorted into the category you'd actually go looking under.

**See also:** [awesome-openclaw](https://github.com/Anil-matcha/awesome-openclaw) and [awesome-hermes-agent](https://github.com/Anil-matcha/awesome-hermes-agent) — curated resources for OpenClaw and Hermes Agent, the two other self-hosted / everything-is-a-plugin agent harnesses with the closest ecosystems to `dsh`.

> [!WARNING]
> Installing any third-party `dsh` plugin runs its code on your machine with your own permissions. Being listed here is not a security review — read the source before installing, especially for plugins that touch credentials, the network, or your filesystem.

## Contents

- [What is DeepSeek Harness?](#what-is-deepseek-harness)
- [Getting Started](#getting-started)
- [Plugin Categories](#plugin-categories)
  - [UI Enhancements](#ui-enhancements)
  - [Usage & Billing](#usage--billing)
  - [Themes & Appearance](#themes--appearance)
  - [Models & Providers](#models--providers)
  - [Sessions & Messages](#sessions--messages)
  - [Memory](#memory)
  - [Tools & Capabilities](#tools--capabilities)
  - [Vision & Multimodal](#vision--multimodal)
  - [Skills](#skills)
  - [Workflow & Automation](#workflow--automation)
  - [Notifications & Integrations](#notifications--integrations)
  - [Development & Runtime](#development--runtime)
  - [Plugin Markets & Managers](#plugin-markets--managers)
  - [Just for Fun](#just-for-fun)
- [Writing Your Own Plugin](#writing-your-own-plugin)
- [Related Projects](#related-projects)
- [Contributing](#contributing)

## What is DeepSeek Harness?

[`deepseek-ai/deepseek-harness`](https://github.com/deepseek-ai/deepseek-harness) is DeepSeek's open-source agent harness, currently in developer preview. Its defining idea is **everything is a plugin**: the model provider, the sandbox, the tool set, the session store, and the UI are all plugins loaded into a Cordis-based runtime, so you can replace or extend any layer without forking the harness itself. Plugins declare a `dsh.bundle` manifest and install with:

```sh
dsh plugin --profile web add <plugin-name>
```

## Getting Started

```sh
# run the Web UI (served at http://127.0.0.1:3080 by default)
npx @deepseek-ai/dsh web

# or from a source checkout
git clone https://github.com/deepseek-ai/deepseek-harness.git
cd deepseek-harness && pnpm install && pnpm run build && pnpm dsh web
```

Tag your own plugin repo with the [`dsh-plugin`](https://github.com/topics/dsh-plugin) GitHub topic so it's discoverable, and consider a plugin browser like [dsh-market](https://github.com/dsh-market/dsh-market) for one-click install/upgrade from inside the Web UI.

## Plugin Categories

### UI Enhancements

- [0xsline/dsh-spotlight](https://github.com/0xsline/dsh-spotlight) — Keyboard-first command palette for the DSH Web UI.
- [1123762794/dsh-web-restart](https://github.com/1123762794/dsh-web-restart) — Sidebar footer button that restarts the dsh web process and persists across the restart it triggers.
- [13071301808/dsh-composer-expand](https://github.com/13071301808/dsh-composer-expand) — Expand/collapse toggle that grows the composer to a tall 70vh writing view for long drafts.
- [1624318455/dsh-plugin-tts](https://github.com/1624318455/dsh-plugin-tts) — Reads assistant replies aloud via free Edge TTS or your own RVC voice models, with adaptive chunked progressive playback.
- [2nd1st/dsh-plugin-open-app](https://github.com/2nd1st/dsh-plugin-open-app) — Runs open-mcp-apps inside DSH with per-app sidebar containers and inline app rendering in ordinary chats.
- [a1073097082/dsh-model-search](https://github.com/a1073097082/dsh-model-search) — Searchable filtering for the model selector by provider, model name, and model ID.
- [a179-sanae/dsh-auto-collapse](https://github.com/a179-sanae/dsh-auto-collapse) — Codex-style auto-collapse: finished turns fold into a single summary row, fully reversible on uninstall.
- [a735624258/dsh-skill-picker](https://github.com/a735624258/dsh-skill-picker) — Searchable skill picker beside the composer that inserts the official `/skill-name` gesture.
- [a903067276-rgb/dsh-hud](https://github.com/a903067276-rgb/dsh-hud) — HUD panel: Git status, MCP servers, skills, model and token usage, all floating.
- [a903067276-rgb/dsh-file-mentions](https://github.com/a903067276-rgb/dsh-file-mentions) — Clickable file paths in replies, with reveal-in-file-manager and a mentioned-files chip list.
- [AcidGr/dsh-web-lan-access](https://github.com/AcidGr/dsh-web-lan-access) — Fixes the Web UI so it survives LAN or Tailscale direct-IP access.
- [AcidGr/dsh-web-mobile-fix](https://github.com/AcidGr/dsh-web-mobile-fix) — Mobile layout fixes for the Web UI on narrow screens.
- [AikenFra/dsh-alive](https://github.com/AikenFra/dsh-alive) — Zero-token online/offline status dot, refreshed every 15 seconds with no LLM calls.
- [AKS1st/dsh-mermaid](https://github.com/AKS1st/dsh-mermaid) — Renders Mermaid fences as sanitized, theme-aware SVG diagrams.
- [AKS1st/dsh-sysmon](https://github.com/AKS1st/dsh-sysmon) — Floating CPU/memory/disk widget with threshold color warnings.
- [AKS1st/dsh-archived-conversations](https://github.com/AKS1st/dsh-archived-conversations) — Read-only archived-conversations list in the sidebar footer.
- [hanzhangzzz/dsh-diagram](https://github.com/hanzhangzzz/dsh-diagram) — Editable Excalidraw diagrams embedded directly in conversations.
- [giiiiiithub/terminal](https://github.com/giiiiiithub/terminal) — A real PTY terminal panel via node-pty and xterm.js, with multi-tab sessions and a dock/floating window.

### Usage & Billing

- [02Muller25/dsh-api-balance](https://github.com/02Muller25/dsh-api-balance) — Real-time DeepSeek API account balance in the composer dock.
- [283Gawin/dsh-heatmap](https://github.com/283Gawin/dsh-heatmap) — GitHub-style activity heatmap of daily commits, token usage, and estimated spend.
- [940842546/dsh-usage-billing](https://github.com/940842546/dsh-usage-billing) — Usage and cost statistics with peak/off-peak pricing and a day/week/month/year/all usage heatmap.
- [AKS1st/model-usage-plugin](https://github.com/AKS1st/model-usage-plugin) — Per-model token usage and cost estimation with account balance in a Settings tab.
- [BeiZi6/dsh-opencodego-usage](https://github.com/BeiZi6/dsh-opencodego-usage) — OpenCodeGo quota monitor with a breathing indicator and rolling/weekly/monthly usage windows.
- [bobcat848/dsh-calculator](https://github.com/bobcat848/dsh-calculator) — Session and all-time API spend plus account balance, with official pricing support.
- [chenyinrusi/dsh-llm-cost](https://github.com/chenyinrusi/dsh-llm-cost) — Per-turn, per-step LLM cost metering with a cost line under each message.
- [CN-Leo/dsh-deepseek-balance](https://github.com/CN-Leo/dsh-deepseek-balance) — Real-time account balance in the composer dock, auto-refreshing every 15 seconds.
- [dk33333333/dsh-deepseek-quota-left](https://github.com/dk33333333/dsh-deepseek-quota-left) — Quota panel collapsed into a left-edge handle showing balance and live conversation cost.
- [FengHuoLinShan/dsh-plugin-llm-balance](https://github.com/FengHuoLinShan/dsh-plugin-llm-balance) — Draggable card showing balance/quota across your most recently used providers.
- [Ghost011118/dsh-balance-meter](https://github.com/Ghost011118/dsh-balance-meter) — Account balance and session cost in the composer dock with peak/off-peak support.
- [GLFzr/dsh-opencode-go-quota](https://github.com/GLFzr/dsh-opencode-go-quota) — Click-to-cycle quota ring (5h/weekly/monthly) colored by urgency.
- [GPIOX/dsh-api-balance](https://github.com/GPIOX/dsh-api-balance) — Floating, draggable balance badge across DeepSeek, Moonshot, OpenAI, and custom endpoints.
- [Han-1413141/dsh-cost-meter](https://github.com/Han-1413141/dsh-cost-meter) — Per-session and daily cost with a budget bar and one-click official price sync.
- [huanyuLv/dsh-balance-tide](https://github.com/huanyuLv/dsh-balance-tide) — Live peak/off-peak pricing badge with a countdown to the next pricing switch.
- [Floating-Dreaming/dsh-minimax-usage](https://github.com/Floating-Dreaming/dsh-minimax-usage) — MiniMax Token Plan usage (5h/weekly windows) with per-model breakdown.

### Themes & Appearance

- [0nt-one/dsh-neo-skin](https://github.com/0nt-one/dsh-neo-skin) — Neo-brutalism skin with hard shadows, sharp corners, and light/dark support.
- [AKS1st/dsh-cyber-particle](https://github.com/AKS1st/dsh-cyber-particle) — Full-screen, click-through particle-network background overlay.
- [BeiZi6/dsh-theme-plugin](https://github.com/BeiZi6/dsh-theme-plugin) — Theme studio with five presets plus fully customizable palettes, hot-swapped and persisted.
- [caoyiwei850/dsh-client-ui-skins](https://github.com/caoyiwei850/dsh-client-ui-skins) — Custom image skins where the palette follows the photo's dominant hue.
- [chinaRXQ/dsh-wallpaper](https://github.com/chinaRXQ/dsh-wallpaper) — Wallpaper skin with opacity, mask, and blur controls.
- [DamonKoy/dsh-web-ui (dsh-skins)](https://github.com/DamonKoy/dsh-web-ui/tree/main/packages/dsh-skins) — Skin family aggregator bundling a skin center plus multiple themed asset packs.
- [Isilsolme/dsh-anthropic-fonts](https://github.com/Isilsolme/dsh-anthropic-fonts) — Anthropic Sans/Serif/Mono fonts with CJK fallback.
- [KinGao294/dsh-skin](https://github.com/KinGao294/dsh-skin) — Codex-style skin switcher with a custom wallpaper layer.
- [kingOfSoySauce/dsh-liang-skin](https://github.com/kingOfSoySauce/dsh-liang-skin) — Adaptive reasoning-effort slider mapped to a visual intensity scale with synced colors.
- [LeemanCheung/dsh-qq2007-skin](https://github.com/LeemanCheung/dsh-qq2007-skin) — QQ 2007-inspired skin with 72 native theme tokens and reversible Settings switches.
- [Lhy723/dsh-neu-theme](https://github.com/Lhy723/dsh-neu-theme) — Neumorphic theme with ambient lighting, material shadows, and frosted-glass surfaces.

### Models & Providers

- [BruceLanLan/dsh-tier-router](https://github.com/BruceLanLan/dsh-tier-router) — Two-tier routing: a strong tier plans and reviews, a cheap tier implements, with failure auto-escalation.
- [btspoony/dsh-llm-fallbacks](https://github.com/btspoony/dsh-llm-fallbacks) — Role-based LLM retry and fallback strategies.
- [dylan121322/llm-adaptive](https://github.com/dylan121322/llm-adaptive) — Per-request complexity classification with automatic provider routing.
- [fieldnote-ops/keyringseam](https://github.com/fieldnote-ops/keyringseam) — macOS Keychain credential provider replacing the local-file default.
- [franksong2702/dsh-codex-connect](https://github.com/franksong2702/dsh-codex-connect) — Connects ChatGPT OAuth / OpenAI Codex models to the harness.
- [GodD6366/dsh-sub2api](https://github.com/GodD6366/dsh-sub2api) — OpenAI-compatible multi-provider routes (OpenAI/Claude/Grok/Gemini) behind one base URL.
- [jiay98528-dev/dsh-model-sync](https://github.com/jiay98528-dev/dsh-model-sync) — Writes live provider model lists into DSH settings with plan-window/balance display.
- [kam74515-boop/dsh-everything-oauth](https://github.com/kam74515-boop/dsh-everything-oauth) — Imports existing Codex, Grok, Claude, and OpenCode logins so you don't re-auth per tool.
- [katsos/dsh-claude-cli](https://github.com/katsos/dsh-claude-cli) — Runs the local Claude Code CLI as a model backend over an existing subscription instead of a metered key.
- [kinoward/dsh-plugin-subhub](https://github.com/kinoward/dsh-plugin-subhub) — Use third-party subscription accounts for chat, image understanding, generation, and editing.
- [Mars-Sea/dsh-commandcode-provider](https://github.com/Mars-Sea/dsh-commandcode-provider) — Unofficial LLM provider with a live model catalog and reasoning-effort support.
- [NOirBRight/dsh-llm-ollama](https://github.com/NOirBRight/dsh-llm-ollama) — Ollama Cloud native chat adapter with model discovery and web search/fetch providers.
- [r600a-code/dsh-swarm-router](https://github.com/r600a-code/dsh-swarm-router) — Routes heterogeneous tasks to the best-suited model with feedback-driven ranking.

### Sessions & Messages

- [3274375092/dsh-voice](https://github.com/3274375092/dsh-voice) — Voice input: speak into the mic and the recognized text is submitted as a chat message.
- [3403473060/dsh-inline-images](https://github.com/3403473060/dsh-inline-images) — Renders local image paths from assistant replies inline with a click-to-zoom lightbox.
- [Anionex/dsh-turn-rewind](https://github.com/Anionex/dsh-turn-rewind) — Rewind conversation and workspace state via a persistent Change Ledger.
- [beijingwahw/dsh-companion](https://github.com/beijingwahw/dsh-companion) — Smart export (Markdown/PDF/JSON/PNG), context-handoff summaries, cost optimization, and global search.
- [Buyi-wsgzg/dsh-sidechain](https://github.com/Buyi-wsgzg/dsh-sidechain) — `/side` persistent side sessions and `/btw` one-shot questions in a temporary fork.
- [bwndlct/dsh-session-export](https://github.com/bwndlct/dsh-session-export) — Exports the current session to portable, schema-versioned Markdown and JSON.
- [Chinesezjc/dsh-interconnect](https://github.com/Chinesezjc/dsh-interconnect) — Cross-instance message and event handoff between DSH instances.
- [chouyong/dsh-fork-graph](https://github.com/chouyong/dsh-fork-graph) — Git-style conversation fork graph with colored lanes and click-to-jump navigation.
- [cindyguyuehu123/dsh-webchatlike](https://github.com/cindyguyuehu123/dsh-webchatlike) — Brings deepseek.com's chat UX to DSH: edit-and-regenerate with a version pager.
- [czm15053/dsh-peer-link](https://github.com/czm15053/dsh-peer-link) — Lets dsh and Claude Code sessions message each other directly.
- [dongsheng123132/task-passport](https://github.com/dongsheng123132/task-passport) — Carries durable task state across DeepSeek Harness, WorkBuddy, Claude Code, and Codex.
- [dream12347/dsh-session-manager](https://github.com/dream12347/dsh-session-manager) — Session trash/restore/purge, recent-activity stats, workspace grouping, and compaction threshold control.

### Memory

- [863683348/dsh-plugin-focus](https://github.com/863683348/dsh-plugin-focus) — Durable focus board pinning objective, constraints, and decisions across compaction and sessions.
- [aerince/dsh-active-context-pruning](https://github.com/aerince/dsh-active-context-pruning) — Model-authored context pruning through the official compaction API.
- [Aik358/dsh-auto-memory](https://github.com/Aik358/dsh-auto-memory) — Cache-friendly three-layer memory with per-turn consolidation and inheritance from other AI tools.
- [akslcw/dsh-negative-ledger](https://github.com/akslcw/dsh-negative-ledger) — Persists disproven paths and blocks repeat attempts until evidence changes.
- [bowenliang123/dsh-context](https://github.com/bowenliang123/dsh-context) — Context-insight panel showing exactly what's filling the model's window and why.
- [Co-Engram/Co-Engram](https://github.com/Co-Engram/Co-Engram) — Self-evolving team memory as plain Markdown in git, shared across DSH, Claude Code, and OpenClaw hosts.
- [diqierjia/StrataGate-AgentMemory](https://github.com/diqierjia/StrataGate-AgentMemory/tree/main/integrations/deepseek-harness) — Automatic, local-first cross-session memory with layered Event/Element cards and evidence-gated recall.
- [FleetingEcho/dsh-handoff](https://github.com/FleetingEcho/dsh-handoff) — Self-maintaining handoff memory per working directory and git branch.
- [flymysql/dsh-memory](https://github.com/flymysql/dsh-memory) — Cross-session memory vault: remember / recall / forget tools with prompt injection.
- [freehul/sgme](https://github.com/freehul/sgme) — Multi-agent shared long-term memory bridge with layered distillation and unified search.
- [FuRongJun-1999/dsh-memory](https://github.com/FuRongJun-1999/dsh-memory) — Multi-agent spatiotemporal memory graph with a self-evolving knowledge flywheel.
- [GIT121995/dsh-memory-gate](https://github.com/GIT121995/dsh-memory-gate) — Bounded local memory with explainable use/verify/ignore decisions and a full audit trail.
- [highland0971/dsh-native-memory](https://github.com/highland0971/dsh-native-memory) — Native per-workspace memory with approval-gated writes and deterministic recall — no external server.

### Tools & Capabilities

- [1624318455/dsh-plugin-tavily](https://github.com/1624318455/dsh-plugin-tavily) — Tavily-backed web search provider for the built-in `web_search` tool.
- [988hj7tczd-oss/dsh-computer-use](https://github.com/988hj7tczd-oss/dsh-computer-use) — Cross-platform Computer Use: virtual-mouse operation, AX-tree zero-vision-cost mode, and safety guards.
- [AbnerAI/dsh-monitor](https://github.com/AbnerAI/dsh-monitor) — Persistent background watchers that wake the agent on new messages — the harness analog of a Monitor tool.
- [akqwpeter-prog/dsh-agent-conductor](https://github.com/akqwpeter-prog/dsh-agent-conductor) — Dispatches tasks from DSH to 11 external agent CLIs (Codex, Claude Code, Cursor, Gemini, and more).
- [AngelosZou/dsh-multi-folder](https://github.com/AngelosZou/dsh-multi-folder) — Secondary working directories with equal read/write/exec permissions.
- [AngLi1997/dsh-plugin-sync](https://github.com/AngLi1997/dsh-plugin-sync) — Syncs the installed plugin manifest to a GitHub Gist with one-click export/import.
- [Anionex/dsh-computer-use](https://github.com/Anionex/dsh-computer-use) — Accessibility-first macOS computer use with fresh observations and scoped permissions.
- [anweat/dsh-browser](https://github.com/anweat/dsh-browser) — Self-contained Playwright + OpenCLI browser runtime exposing 9 interactive browser tools.
- [anweat/dsh-voice-webspeech](https://github.com/anweat/dsh-voice-webspeech) — Browser Web Speech API voice input: zero server, zero keys.
- [1na-ko/dsh-hdc-bridge](https://github.com/1na-ko/dsh-hdc-bridge) — HarmonyOS device bridge: screenshot/install/log/crash/UI automation loop.
- [6Mikao9/dsh-wsl-workspace](https://github.com/6Mikao9/dsh-wsl-workspace) — Adds a WSL workspace from the web GUI without reinstalling dsh inside WSL.
- [863683348/dsh-plugin-translation](https://github.com/863683348/dsh-plugin-translation) — Translation toolkit: segmentation, glossary extraction, source-target QA, and translation memory.
- [863683348/dsh-plugin-finance-data](https://github.com/863683348/dsh-plugin-finance-data) — Finance toolkit: currency formatting, return/CAGR math, valuation ratios, and risk metrics.

- [maddogfinance/dsh-trading](https://github.com/maddogfinance/dsh-trading) — Research-only trading workbench: typed market-data seam with BYO providers, multi-timeframe indicator snapshots, interactive chart cards with provenance-gated model annotations, and a pre-execute risk-guard that blocks execution-shaped tool calls.
### Vision & Multimodal

- [54xkeee/dsh-vision](https://github.com/54xkeee/dsh-vision) — Zero-cost vision for text-only DeepSeek via a logged-in Chrome CDP bridge, with fallback providers.
- [akqwpeter-prog/dsh-media-skills](https://github.com/akqwpeter-prog/dsh-media-skills) — Free vision bridge and image generation for text-only models with engine failover.
- [Anionex/dsh-vision-toolkit](https://github.com/Anionex/dsh-vision-toolkit) — Intent-aware image Q&A, long-screenshot OCR, UI reproduction, and grounding.
- [ConsoleSun/Gemini-Eyes](https://github.com/ConsoleSun/Gemini-Eyes) — MCP bridge to gemini.google.com for vision analysis plus Imagen/Veo generation, no API key.
- [corrinehu/dsh-chat-imagine](https://github.com/corrinehu/dsh-chat-imagine) — Automatically generates and displays images in chat via API channels or local CLIs.
- [dickpy/dsh-imagegen](https://github.com/dickpy/dsh-imagegen) — Text-to-image and image-to-image through a configurable OpenAI-compatible endpoint.
- [Einskyle/dsh-llm-vision-bridge](https://github.com/Einskyle/dsh-llm-vision-bridge) — Native vision bridge routing pasted images through a local VLM, then feeding the description to text-only DeepSeek.
- [Elohia/dsh-plugin-mm-vision](https://github.com/Elohia/dsh-plugin-mm-vision) — Translates images into compact structured spatial text for pixel-level understanding.
- [FuzzySoul/dsh-free-vision](https://github.com/FuzzySoul/dsh-free-vision) — Free-tier vision bridge (Qwen3-VL-Flash, Doubao, DeepSeek-OCR) with a settings GUI.
- [gloryxpnv/dsh-tool-vision](https://github.com/gloryxpnv/dsh-tool-vision) — Local-first structured vision returning JSON evidence — images never leave the machine.
- [good-boy4069/dsh-vision-guard](https://github.com/good-boy4069/dsh-vision-guard) — Transparent image guard avoiding session deadlocks, plus OCR/PDF/docx/pptx/video analysis.
- [haiziyao/dsh-vision-mix](https://github.com/haiziyao/dsh-vision-mix) — Combines text, vision, and image-generation APIs into one auto-routing Mix model.

### Skills

- [AKS1st/dsh-skill-manager](https://github.com/AKS1st/dsh-skill-manager) — Browse and edit system/user/workspace/preset skills, import from zip, export or delete.
- [Fectivnfy112357/github-explore](https://github.com/Fectivnfy112357/github-explore) — GitHub search, discovery, and audit scripts wrapped as a SKILL.md pack around the `gh` CLI.
- [GanyuanRan/Aegis](https://github.com/GanyuanRan/Aegis) — Software-engineering method pack: baseline-first planning, systematic debugging, and verification before completion.
- [gongyijie85/dsh-ecc](https://github.com/gongyijie85/dsh-ecc) — 273 ECC skills ported from a large operator-system skill catalog.
- [gongyijie85/mattpocock-skills-dsh](https://github.com/gongyijie85/mattpocock-skills-dsh) — Matt Pocock's full promoted skill set (grilling, TDD, code review, wayfinder) ported to DSH.
- [hackerFish/awesome-dsh-skills](https://github.com/hackerFish/awesome-dsh-skills) — 12 tested engineering skills, each passing a format validator and an isolated load smoke test.
- [hatsuyuki0103/oh-my-deepseek-harness](https://github.com/hatsuyuki0103/oh-my-deepseek-harness) — OMX-style workflow skills: deep-interview, ralplan, ralph, autopilot, team, code-review, and more.
- [Ikalus1988/MisakaNet](https://github.com/Ikalus1988/MisakaNet) — Failure-recovery memory with BM25 + semantic RAG retrieval over past engineering sessions.
- [dhicoc/dsh-reverse-skill](https://github.com/dhicoc/dsh-reverse-skill) — 85 SKILL.md pack for reverse engineering and authorized pentesting/security research.

### Workflow & Automation

- [1052326311/dsh-plan-lattice](https://github.com/1052326311/dsh-plan-lattice) — Persistent execution contracts and recursive work graphs for long or underspecified tasks.
- [940842546/dsh-permissions](https://github.com/940842546/dsh-permissions) — Claude Code-style permission tiers (hard/deny/ask/allow) with workspace-scoped rules.
- [alib8b8/dsh-plugin-aflare](https://github.com/alib8b8/dsh-plugin-aflare) — Deterministic YAML workflow DAGs with WAL crash recovery and Saga compensation, 300+ templates.
- [apheli0os/deepseek-harness-orchestrate](https://github.com/apheli0os/deepseek-harness-orchestrate) — Declarative task-DAG orchestration with parallel topological execution.
- [biociao/dsh-science](https://github.com/biociao/dsh-science) — Research workbench: ReAct research loop, versioned artifacts with provenance, and science skills.
- [btspoony/dsh-advisor](https://github.com/btspoony/dsh-advisor) — Pairs a second model that passively reviews each turn and injects notes.
- [Ceelog/dsh-plugins (scheduled-tasks)](https://github.com/Ceelog/dsh-plugins/tree/main/src/plugins/dsh-plugin-scheduled-tasks) — Per-project scheduled prompts run as fresh headless agent sessions on one-time/interval/cron schedules.
- [ChongCyrus/Vibe-Mathematics](https://github.com/ChongCyrus/Vibe-Mathematics) — Multi-agent math solving: brainstorm → solve → multi-verifier debate → verified knowledge base.
- [cloader/dsh-taskboard](https://github.com/cloader/dsh-taskboard) — Task board with project/model assignment and cron scheduling.
- [DamonKoy/dsh-plugins (dsh-approve-for-me)](https://github.com/DamonKoy/dsh-plugins/tree/main/packages/dsh-approve-for-me) — Auto-approves read-only tools and auto-denies dangerous commands via a fail-closed policy engine.
- [dickpy/dsh-cloud-sync](https://github.com/dickpy/dsh-cloud-sync) — Syncs DSH profiles and plugin archives through WebDAV/S3-compatible storage with encrypted snapshots.
- [EvilIrving/dsh-proof](https://github.com/EvilIrving/dsh-proof) — Independent read-only acceptance layer verifying each turn before it closes.
- [february2015/dsh-taskswarm](https://github.com/february2015/dsh-taskswarm) — Dependency-ordered task waves run in parallel git-worktree lanes with cross-model review.

### Notifications & Integrations

- [2006spy/dsh-token-billing](https://github.com/2006spy/dsh-token-billing) — Real-time token billing with official CNY pricing and automatic peak/off-peak switching.
- [AbcdefgXW/dsh-msg-hub](https://github.com/AbcdefgXW/dsh-msg-hub) — IM channel bridge (WeChat/QQ/Feishu) with proactive push to your phone.
- [AI-Galaxy-GPU/dsh-sound](https://github.com/AI-Galaxy-GPU/dsh-sound) — Per-event sound notifications for completion, approval, question, and task-failure.
- [Alan2Z/dsh-speak](https://github.com/Alan2Z/dsh-speak) — Voice-announces the final reply via native OS voices on Windows and macOS.
- [amlyczz/dsh-lark-link](https://github.com/amlyczz/dsh-lark-link) — High-reliability Feishu/Lark bridge with QR auth and card-based approval commands.
- [aokamoaki/dsh-notify](https://github.com/aokamoaki/dsh-notify) — Windows toast + sound on turn done/error/goal, plus ask & approval alerts.
- [BiBoyang/dsh-im-bridge](https://github.com/BiBoyang/dsh-im-bridge) — Two-way WeChat bridge with in-chat approve/reject and message injection.
- [Bing-Bryan/dsh-unread-dot](https://github.com/Bing-Bryan/dsh-unread-dot) — macOS Dock badge and chime built on the Badging API.
- [cdxiaodong/dsh-island](https://github.com/cdxiaodong/dsh-island) — Bridges sessions, tool calls, and approvals to the macOS notch panel.
- [cerebrixos-org/tuning-engines-cli](https://github.com/cerebrixos-org/tuning-engines-cli/tree/main/packages/tuningengines-dsh-plugin) — Exports metadata-only turn/model/tool/approval events for governed traces and cost analysis.
- [117BS/dsh-perlica-ding](https://github.com/117BS/dsh-perlica-ding) — Themed tiered sound notifications for plan-ready, task-done, and error states.

### Development & Runtime

- [2008924/dsh-progress-viz](https://github.com/2008924/dsh-progress-viz) — Real-time stage/ETA/cost dashboard turning the session event stream into a live multi-task grid.
- [863683348/dsh-gov](https://github.com/863683348/dsh-gov) — Agent governance: policy-based tool gating, a structured JSONL audit trail, and per-agent token quotas.
- [863683348/dsh-plugin-gate](https://github.com/863683348/dsh-plugin-gate) — Installation safety gate: antivirus-style scan of install scripts and permissions before `dsh plugin add`.
- [863683348/dsh-plugin-verify](https://github.com/863683348/dsh-plugin-verify) — Evidence-based claim checking against workspace files with line citations.
- [863683348/dsh-trend-radar](https://github.com/863683348/dsh-trend-radar) — Ecosystem trend dashboard: new plugins, star gainers, category heat, and a keyword radar.
- [a179-sanae/dsh-code-check](https://github.com/a179-sanae/dsh-code-check) — Runs `tsc --noEmit` after edits and reports errors via a `code_check` tool.
- [ai-eks/dsh-auth-tunnel](https://github.com/ai-eks/dsh-auth-tunnel) — Password-gated public access through Cloudflare Tunnels with an in-app directory picker.
- [Airmetro/dsh-update-checker](https://github.com/Airmetro/dsh-update-checker) — Compares the harness and every plugin against npm/GitHub releases with one-click updates and rollback.
- [AngelosZou/graphlint](https://github.com/AngelosZou/graphlint/tree/main/integrations/dsh) — Dead-code detection for AI-generated codebases via dependency-graph reachability.
- [aokamoaki/dsh-startup-guard](https://github.com/aokamoaki/dsh-startup-guard) — Repairs corrupt session logs and quarantines crash-causing bundles so a broken plugin can't brick startup.
- [ayahunter/dsh-plugin-clinic](https://github.com/ayahunter/dsh-plugin-clinic) — Read-only health check of the installed plugin set: loader health, dependency integrity, and install-script risk.
- [Raphaelutumn/dsh-change-budget](https://github.com/Raphaelutumn/dsh-change-budget) — Configurable per-turn budgets that limit distinct files, mutation calls, and UTF-8 payload bytes before supported file-mutation tools run.

### Plugin Markets & Managers

- [dsh-market/dsh-market](https://github.com/dsh-market/dsh-market) — (Recommended) In-app plugin marketplace with one-click install/upgrade and search by category.
- [1e0zj/dsh-plugin-mall](https://github.com/1e0zj/dsh-plugin-mall) — Live GitHub `dsh-plugin` topic search with per-repo manifest verification and anti-squatting checks.
- [863683348/dsh-insight](https://github.com/863683348/dsh-insight) — Plugin insight center: needs-matching, environment recipes, health scoring, and a security audit verdict.
- [863683348/dsh-need-finder](https://github.com/863683348/dsh-need-finder) — Requirement-driven plugin discovery matching natural-language needs to a curated directory.
- [863683348/dsh-plugin-audit](https://github.com/863683348/dsh-plugin-audit) — Ecosystem-wide health audit: maintenance/docs/downloads scoring, security scan, and a web leaderboard.
- [863683348/dsh-plugin-recommend](https://github.com/863683348/dsh-plugin-recommend) — Ranks plugins from a 1100+ entry catalog by need, category, and tags, refreshed from this list.
- [863683348/dsh-recipe](https://github.com/863683348/dsh-recipe) — Scenario bundles of plugins ("dotfiles for the plugin world") with ordered install sequences.
- [alex04130/dsh-forge](https://github.com/alex04130/dsh-forge) — Runtime extension suite: cross-session mailbox, agent teams, subagent spawn policy, and plugin market.
- [bradeGithub/DSH-Plugins-Marketplace](https://github.com/bradeGithub/DSH-Plugins-Marketplace) — Settings-page marketplace auto-collected from the `dsh-plugin` topic, CI-refreshed every 2 hours.
- [huguangyu666/dsh-store](https://github.com/huguangyu666/dsh-store) — npm-authoritative catalog plus curated list (550+ plugins), with quality verification.
- [icefall7/dsh-plugin-scout](https://github.com/icefall7/dsh-plugin-scout) — Scouts every `dsh-plugin`-tagged repo and judges each as worth trying, watching, or skipping.

### Just for Fun

- [AmeKrance/anan-thermal-monitor](https://github.com/AmeKrance/anan-thermal-monitor) — Desktop pet showing real-time CPU/RAM/GPU/NVMe temperatures.
- [Awu12277/dsh-stock-watch](https://github.com/Awu12277/dsh-stock-watch) — A-share watchlist with intraday and candlestick charts in a collapsible popup.
- [hellodigua/dsh-emoji](https://github.com/hellodigua/dsh-emoji) — Automatically adds emojis to AI replies.
- [HuanLinOTO/dsh-plugin-d399](https://github.com/HuanLinOTO/dsh-plugin-d399) — Pops up a mini-game menu (wordle, match-3) while the model generates.
- [JAdpp/dsh-whale-galgame](https://github.com/JAdpp/dsh-whale-galgame) — Multi-character Galgame conversation view with affection, memory, and CG galleries.
- [jitengfei/dsh-whale-arcade](https://github.com/jitengfei/dsh-whale-arcade) — Floating browser-local arcade with score games for breaks while waiting on the agent.
- [lhh010/dsh-minigames](https://github.com/lhh010/dsh-minigames) — Side-panel arcade with 18 offline mini-games.
- [lucky8197/dsh-devquest](https://github.com/lucky8197/dsh-devquest) — Turns coding into an RPG: XP, 27+ achievement badges, levels, and seasons.
- [luumod/dsh-achievements](https://github.com/luumod/dsh-achievements) — Achievement/gamification plugin with a badge wall and unlock toasts.
- [minybear/DeepSeek-Harness-Pet](https://github.com/minybear/DeepSeek-Harness-Pet) — Codex-style desktop pet mirroring the agent's running state.
- [Moeblack/deepseek-manners](https://github.com/Moeblack/deepseek-manners) — Appends a thank-you note after every message. Mind your manners.
- [Nagi-ovo/dsh-ads](https://github.com/Nagi-ovo/dsh-ads) — Parody ads in 2005-Chinese-web style. All fictional.

For the complete, continuously-updated plugin index (well over a thousand entries across every category above), see [awesome-dsh-plugin/awesome-dsh-plugin](https://github.com/awesome-dsh-plugin/awesome-dsh-plugin).

## Writing Your Own Plugin

1. Scaffold a `dsh.bundle` manifest declaring what your plugin extends (model, tool, sandbox, UI, session store, or the agent loop itself).
2. Tag the repo with the [`dsh-plugin`](https://github.com/topics/dsh-plugin) GitHub topic for discoverability.
3. Install locally with `dsh plugin --profile web add <path-or-name>` to iterate.
4. Read [deepseek-ai/deepseek-harness](https://github.com/deepseek-ai/deepseek-harness)'s [architecture docs](https://github.com/deepseek-ai/deepseek-harness/blob/master/docs/architecture.md) and [AGENTS.md](https://github.com/deepseek-ai/deepseek-harness/blob/master/AGENTS.md) before building anything that touches the core agent loop.

## Related Projects

- [awesome-openclaw](https://github.com/Anil-matcha/awesome-openclaw) — curated resources for OpenClaw, the self-hosted messaging-first agent with the largest community skill catalog.
- [awesome-hermes-agent](https://github.com/Anil-matcha/awesome-hermes-agent) — curated resources for Hermes Agent (Nous Research), the self-evolving skill-generating agent.
- [Open-Generative-AI](https://github.com/Anil-matcha/Open-Generative-AI) — a broader curated hub of open-source generative AI tools and platforms.
- [Generative-Media-Skills](https://github.com/Anil-matcha/Generative-Media-Skills) — agent-skill building blocks for generative media workflows, in the same plugin/skill spirit as `dsh`.

## Contributing

PRs welcome. Keep entries to one line, link the actual plugin repo (not a fork or mirror), and make sure the plugin installs and does what its description says before submitting.

---

⭐ If this saved you time hunting through the plugin ecosystem, star it so others can find it too.
