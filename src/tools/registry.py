from typing import List
from .base import BaseTool
from .web_search import WebSearchTool
from .reminder import ReminderTool

_TOOLS = {
    "web_search": WebSearchTool(),
    "set_reminder": ReminderTool()
}

def get_tool(name: str) -> BaseTool:
    return _TOOLS.get(name)

def get_all_tools() -> List[BaseTool]:
    return list(_TOOLS.values())