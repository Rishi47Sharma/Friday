from typing import List, Dict
from ..llm.registry import get_llm
from ..persona.loader import load_persona

class Companion:
    def __init__(self, persona_path: str, llm_config: dict):
        self.system_prompt = load_persona(persona_path)
        self.llm = get_llm(llm_config)
        self.history: List[Dict[str, str]] = [] 
        self.max_history_turns = 6 

    async def chat(self, user_input: str) -> str:
        # TODO: Integrate actual SQLite memory recall here for Task 4
        memory_context = "Memory: []" 

        # Build messages: System + Memory -> Last 6 Turns -> Current User Input
        messages = [
            {"role": "system", "content": f"{self.system_prompt}\n{memory_context}"}
        ]
        messages.extend(self.history)
        messages.append({"role": "user", "content": user_input})

        # Execute LLM call
        response = await self.llm.chat(messages)
        reply = response.choices[0].message.content

        # Update sliding history window (1 turn = 1 user msg + 1 assistant msg)
        self.history.append({"role": "user", "content": user_input})
        self.history.append({"role": "assistant", "content": reply})
        
        # Keep only the last 6 turns (12 messages)
        if len(self.history) > (self.max_history_turns * 2):
            self.history = self.history[-(self.max_history_turns * 2):]

        return reply