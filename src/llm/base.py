from abc import ABC, abstractmethod
from typing import List, Dict, Any

class BaseLLM(ABC):
    @abstractmethod
    async def chat(self, messages: List[Dict[str, str]], tools: List[Dict[str, Any]] = None) -> Any:
        """Async chat interface for all LLM providers."""
        pass