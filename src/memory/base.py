from abc import ABC, abstractmethod
from typing import List, Dict, Optional

class BaseMemory(ABC):
    @abstractmethod
    async def remember(self, user_id: str, key: str, value: str, ttl: Optional[int] = None) -> None:
        """Store a key-value fact for a user."""
        pass

    @abstractmethod
    async def recall(self, user_id: str, query: Optional[str] = None, limit: int = 5) -> List[Dict[str, str]]:
        """Retrieve facts. Query is unused in v0, reserved for v1 vector search."""
        pass