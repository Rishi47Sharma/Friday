# Friday Project - Context Summary
Date: 2026-05-10

## 1. Goal
Build a pluggable AI personal companion as a Python package.
- User provides: persona.yaml + LLM config
- v0 features: chat with personality, remember facts, web search, set reminder
- Design for scale from day 1

## 2. Key Decisions Made
- Language: Python 3.11+ with Poetry
- LLM routing: LiteLLM adapter (supports OpenAI, Groq, Ollama, Anthropic)
- Architecture: 4 layers - LLM Adapter, Persona Engine, Memory, Tool Router
- Token strategy: system prompt <300 tokens, history window 6 turns, memory top 5 facts
- Packaging: pip installable, core separated from interfaces

## 3. Artifacts Created So Far
1. v0 Task Checklist (22 tasks across 7 milestones)
   - File: v0_tasks.md
2. Token-efficient docs/ (6 files)
   - 00-token-principles.md
   - 01-architecture.md
   - 02-persona-spec.md
   - 03-tool-contracts.md
   - 04-memory-policy.md
   - 05-dev-checklist.md
3. Scalable directory scaffold
   - Full structure with src/ai_companion/, interfaces/, plugins/, infra/
   - Ready for providers, memory backends, API, CLI, WebSocket
   - Includes placeholders for future scale (chroma, redis, k8s)

## 4. v0 Scope Locked
Milestone 0: Setup
Milestone 1: LLM abstraction
Milestone 2: Persona system
Milestone 3: Core agent loop
Milestone 4: SQLite memory
Milestone 5: 2 tools (search, reminder)
Milestone 6: Packaging
Milestone 7: Validation

Success criteria: pip install -> load persona -> chat -> remember name after restart -> search -> reminder works

## 5. Directory Structure Highlights
- src/ai_companion/core/ : Companion orchestrator
- src/ai_companion/llm/providers/ : one file per model
- src/ai_companion/memory/backends/ : sqlite (v0), chroma/redis (future)
- src/ai_companion/tools/builtin/ : search, reminder
- src/ai_companion/interfaces/ : cli, api, websocket (separate from core)
- plugins/ : external tools without touching core
- infra/ : docker and k8s ready

## 6. Next Immediate Steps
1. Fill core/companion.py and agent/loop.py using docs/01-architecture.md
2. Implement BaseLLM and LiteLLMAdapter
3. Create first persona at persona/templates/kavi.yaml
4. Run token benchmark using scripts/benchmark_tokens.py


