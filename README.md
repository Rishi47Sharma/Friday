# Project Friday — v1 Roadmap

Friday is a model-agnostic, memory-first AI companion inspired by Tony Stark's FRIDAY. Built to run locally, swap LLMs in one line, and remember you across restarts.

> **Status: v0 complete** — LLM adapter, persona, SQLite memory, and tools (web_search, reminder) are working.

---

## What v0 proved

✅ **Swappable LLM** — Gemini 2.0 Flash tested at 79 prompt tokens, Groq/Ollama ready via registry
✅ **Persona engine** — YAML-driven personality, no hardcoding
✅ **Persistent memory** — SQLite fact-store, <50 tokens injected per turn
✅ **Tools** — model-agnostic JSON tool calling (web_search + set_reminder)
✅ **Token budget** — full turn under 300 tokens

Tested: `poetry run python examples/basic_chat.py` remembers name and coffee across restarts.

## v1 Goals

v1 turns the prototype into a daily driver. Focus: speed, semantic memory, and real actions.

### 1. Memory v2
- **Redis backend** — <5ms recall, native TTL for reminders
- **Semantic recall** — add embeddings column, use cosine search instead of "last 5"
- **Auto-extraction** — LLM extracts facts from chat, no regex rules
- **Memory types:** `facts`, `episodic` (summaries), `procedural` (preferences)

### 2. Tools v2
- **Native function calling** — use Gemini/Groq tool schemas instead of JSON parsing
- **Background scheduler** — APScheduler to fire reminders
- **New tools:**
  - `calendar_check` — read Google Calendar
  - `send_message` — WhatsApp/Telegram
  - `long_term_search` — search your own memory

### 3. Voice & Realtime
- **STT/TTS** — Whisper + Piper for local voice
- **Streaming responses** — token-by-token output
- **Wake word** — "Hey Friday"

### 4. Multi-user & Privacy
- Real user_id isolation
- Local-first encryption for `data/friday.db`
- Configurable memory retention

## Architecture (unchanged)

```
src/
  core/companion.py      # orchestrator
  llm/registry.py        # swap models
  memory/registry.py     # sqlite → redis → vector
  tools/registry.py      # web_search → 10+ tools
  persona/loader.py
```

All layers talk via interfaces, not implementations.

## Getting Started (v0)

```bash
git clone <repo>
cd friday
poetry install
cp .env.example .env  # add GEMINI_API_KEY
poetry run python examples/basic_chat.py
```

## Configuration for v1

`config/default.yaml`:
```yaml
llm:
  provider: gemini
  model: gemini-2.0-flash

memory:
  backend: redis  # was sqlite
  url: redis://localhost:6379/0
  semantic: true

tools:
  - web_search
  - set_reminder
  - calendar_check
```

## Roadmap

- [x] v0 — core loop + memory + 2 tools
- [ ] v1.0 — Redis + semantic memory
- [ ] v1.1 — background scheduler + voice
- [ ] v1.2 — mobile app (React Native) + local sync
- [ ] v2 — multi-agent (Friday delegates to specialist agents)

## Why build this

ChatGPT remembers, but you can't swap the model, own the memory, or run it offline. Friday is the companion you control — local-first, model-agnostic, and built for <300 tokens per turn.

---

Built with: Python 3.11, Poetry, aiosqlite, DuckDuckGo Search. Next: Redis, sentence-transformers, APScheduler.
