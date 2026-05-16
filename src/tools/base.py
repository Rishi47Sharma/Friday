from abc import ABC, abstractmethod
from typing import Dict, Any

class BaseTool(ABC):
    name: str
    description: str
    parameters: dict

    @abstractmethod
    async def run(self, **kwargs) -> Dict[str, Any]:
        """Execute the tool's function and return a JSON-serializable dictionary."""
        pass