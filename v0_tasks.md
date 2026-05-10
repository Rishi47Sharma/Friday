# AI Companion v0 - Task Checklist

Goal: package jisme user apna persona.yaml aur apna LLM config de, aur basic chat + memory + 2 tools chale.

## Milestone 0: Setup (Day 1)
- [ ] **T0.1 Repo init** - `poetry new ai-companion`, git init, README.md banao
- [ ] **T0.2 Folder structure** - ai_companion/llm, persona, memory, tools, tests/ banao
- [ ] **T0.3 Env setup** - .env.example with OPENAI_API_KEY, GROQ_API_KEY etc
- [ ] **T0.4 Dependencies** - poetry add litellm pydantic pyyaml aiosqlite duckduckgo-search

Done when: `poetry run python -m ai_companion` error nahi deta

## Milestone 1: LLM Abstraction (Day 1-2)
- [ ] **T1.1 BaseLLM interface** - base.py me abstract class with async chat(messages) -> str
- [ ] **T1.2 LiteLLMAdapter** - litellm.acompletion wrap karo, provider/model dict se
- [ ] **T1.3 Config loader** - llm = {"provider":"groq","model":"llama3-70b"} accept karo
- [ ] **T1.4 Test** - 2 models se "hello" test pass

Done when: same code se OpenAI aur Ollama dono chale

## Milestone 2: Persona System (Day 2)
- [ ] **T2.1 Schema design** - personas/kavi.yaml: name, core_prompt, voice[], boundaries[]
- [ ] **T2.2 PersonaLoader** - YAML load, validate with pydantic
- [ ] **T2.3 Prompt builder** - system prompt = core_prompt + voice instructions
- [ ] **T2.4 Hot-swap test** - 2 personas switch karke tone change dikhe

Done when: persona file badlo, bot ka personality badle bina code change

## Milestone 3: Core Agent Loop (Day 3)
- [ ] **T3.1 Companion class** - __init__(persona_path, llm_config, tools=[])
- [ ] **T3.2 Chat method** - history + system prompt + user msg -> LLM
- [ ] **T3.3 Streaming** - async generator for token stream
- [ ] **T3.4 CLI test** - simple REPL banao

Done when: `await bot.chat("hi")` se persona-style reply aaye

## Milestone 4: Memory v0 (Day 3-4)
- [ ] **T4.1 SQLite store** - memory/store.py, table: facts(user_id, key, value, ts)
- [ ] **T4.2 remember()** - LLM se extract "remember: X" ya manual call
- [ ] **T4.3 recall()** - query pe top 5 facts retrieve
- [ ] **T4.4 Auto-inject** - har turn me recalled facts system prompt me add

Done when: "mera naam Rahul hai" bolo, restart ke baad bhi yaad rahe

## Milestone 5: Tools (Day 4-5)
- [ ] **T5.1 BaseTool** - name, description, parameters schema (json)
- [ ] **T5.2 Tool registry** - tools ko dict me register
- [ ] **T5.3 Web search** - DuckDuckGo search tool implement
- [ ] **T5.4 Reminder** - reminder.py, local JSON me save, list karo
- [ ] **T5.5 Tool calling loop** - LLM JSON output parse, tool run, result feed back

Done when: "Delhi weather search karo" aur "mujhe 7pm coffee yaad dilao" kaam kare

## Milestone 6: Packaging (Day 5)
- [ ] **T6.1 Public API** - from ai_companion import Companion only expose
- [ ] **T6.2 pyproject.toml** - version 0.1.0, entry points
- [ ] **T6.3 Build test** - poetry build, fresh venv me pip install dist/*.whl
- [ ] **T6.4 Example script** - examples/basic.py banao

Done when: dusre folder se import karke chal jaye

## Milestone 7: v0 Validation (Day 6)
- [ ] **T7.1 E2E test** - 1) persona load 2) chat 3) remember name 4) search 5) reminder
- [ ] **T7.2 README** - installation, persona format, llm config examples
- [ ] **T7.3 Demo video/gif** - optional but useful

v0 DONE = user apna persona.yaml aur apna model deke, `pip install ai-companion` ke baad 5 minute me chala sake
