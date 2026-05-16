from typing import Dict, Any
from ddgs import DDGS
from .base import BaseTool

class WebSearchTool(BaseTool):
    name = "web_search"
    description = "Search the web for current information"
    parameters = {
        "type": "object",
        "properties": {
            "query": {"type": "string"}
        },
        "required": ["query"]
    }

    async def run(self, query: str, **kwargs) -> Dict[str, Any]:
        try:
            with DDGS() as ddgs:
                # max_results=3 ensures we don't blow up our token budget with massive payloads
                results = list(ddgs.text(query, max_results=3))
                return {
                    "results": [
                        {"title": r['title'], "url": r['href'], "snippet": r['body']} 
                        for r in results
                    ]
                }
        except Exception as e:
            return {"error": str(e)}