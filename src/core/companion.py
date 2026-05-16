import re
import json
from typing import List, Dict
from ..llm.registry import get_llm
from ..persona.loader import load_persona
from ..memory.registry import get_memory
from ..tools.registry import get_all_tools

class Companion:
    def __init__(self, persona_path: str, config: dict):
        self.system_prompt = load_persona(persona_path)
        self.llm = get_llm(config.get("llm", {}))
        self.memory = get_memory(config.get("memory", {}))
        self.history: List[Dict[str, str]] = [] 
        self.max_history_turns = 6 
        
        # 1. Load Tools
        self.tools = {t.name: t for t in get_all_tools()}
        
        # 2. Build Token-Efficient Tool Instructions (~80 tokens)
        tool_schemas = {t.name: {"description": t.description, "parameters": t.parameters} for t in self.tools.values()}
        self.tool_instructions = (
            f"Available tools: {list(self.tools.keys())}. "
            f"To use a tool, reply ONLY with JSON: {{\"tool\":\"name\",\"args\":{{...}}}}\n"
            f"Schemas: {json.dumps(tool_schemas)}"
        )

    async def _extract_facts(self, user_input: str, user_id: str):
        text = user_input.lower()
        match_is = re.search(r"\bmy\s+([a-z_]+)\s+is\s+([a-z0-9\s]+)(?:[.,!?]|$)", text)
        if match_is:
            await self.memory.remember(user_id, match_is.group(1).strip(), match_is.group(2).strip())
        match_pref = re.search(r"remember that i\s+(like|love|hate|prefer)\s+([a-z0-9\s]+)(?:[.,!?]|$)", text)
        if match_pref:
            await self.memory.remember(user_id, match_pref.group(1).strip() + "s", match_pref.group(2).strip())

    async def chat(self, user_input: str, user_id: str = "default_user") -> str:
        await self._extract_facts(user_input, user_id)

        facts = await self.memory.recall(user_id)
        memory_context = "User facts:\n" + "\n".join([f"{f['key']}: {f['value']}" for f in facts]) if facts else ""

        # Inject persona, memory, and tools into the system prompt
        full_system_prompt = f"{self.system_prompt}\n{memory_context}\n{self.tool_instructions}".strip()
        
        messages = [{"role": "system", "content": full_system_prompt}]
        messages.extend(self.history)
        messages.append({"role": "user", "content": user_input})

        # Initial LLM Call
        response = await self.llm.chat(messages)
        reply = response.choices[0].message.content.strip()

        # FIX: Clean out any Markdown wrapping strings the LLM adds
        clean_reply = reply.replace("```json", "").replace("```", "").strip()

        # 3. Detect and Execute Tool Call (Limit 1 per turn)
        if "{" in clean_reply and '"tool"' in clean_reply:
            try:
                # Use regular expression to safely isolate the JSON dictionary block
                json_match = re.search(r'(\{.*\})', clean_reply, re.DOTALL)
                if json_match:
                    parsed = json.loads(json_match.group(1))
                    tool_name = parsed.get("tool")
                    args = parsed.get("args", {})
                    
                    if tool_name in self.tools:
                        # Add a visual indicator to the console so the user knows a tool is running
                        print(f"\n[System: Executing {tool_name}...]")
                        
                        # Inject backend contexts required for execution
                        args["memory"] = self.memory
                        args["user_id"] = user_id
                        
                        # Run the actual tool (Executes write to SQLite for set_reminder)
                        tool_result = await self.tools[tool_name].run(**args)
                        
                        # Append the tool's raw payload to the message block and prompt LLM again
                        messages.append({"role": "assistant", "content": clean_reply})
                        messages.append({"role": "user", "content": f"System Event - Tool Result: {json.dumps(tool_result)}. Please confirm this action to the user naturally based on the result."})
                        
                        final_response = await self.llm.chat(messages)
                        reply = final_response.choices[0].message.content.strip()
            except json.JSONDecodeError:
                pass # Fallback to printing raw output if compilation fails

        # Manage history window
        self.history.append({"role": "user", "content": user_input})
        self.history.append({"role": "assistant", "content": reply})
        if len(self.history) > (self.max_history_turns * 2):
            self.history = self.history[-(self.max_history_turns * 2):]

        return reply