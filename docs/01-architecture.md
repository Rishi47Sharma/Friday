# Architecture v0

Components:
- Companion: orchestrator
- LLMAdapter: chat(messages)
- PersonaLoader: yaml -> system_prompt
- MemoryStore: sqlite, remember/recall
- ToolRouter: register + execute

Flow:
1. load persona (once)
2. recall facts
3. build messages = [sys, mem, history(6), user]
4. llm.chat
5. if tool_call -> execute -> feed back
6. summarize -> save

No vector DB in v0. Keep stateless tools.
