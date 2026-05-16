from typing import Dict, Any
from .base import BaseTool

class ReminderTool(BaseTool):
    name = "set_reminder"
    description = "Save a reminder"
    parameters = {
        "type": "object",
        "properties": {
            "text": {"type": "string"},
            "time": {"type": "string"}
        },
        "required": ["text", "time"]
    }

    async def run(self, text: str, time: str, memory=None, user_id=None, **kwargs) -> Dict[str, Any]:
        if memory and user_id:
            # We prefix the key with 'reminder:' to keep the SQLite database organized
            await memory.remember(user_id, f"reminder:{time}", text)
            return {"status": "saved", "time": time, "text": text}
        return {"error": "Internal Error: Memory backend not connected to tool."}