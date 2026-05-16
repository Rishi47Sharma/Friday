from .backends.sqlite import SQLiteMemory
from .base import BaseMemory

def get_memory(config: dict) -> BaseMemory:
    """Factory to instantiate the memory backend based on config."""
    backend = config.get("backend", "sqlite")
    
    if backend == "sqlite":
        db_path = config.get("db_path", "data/friday.db")
        return SQLiteMemory(db_path)
        
    raise ValueError(f"Unsupported memory backend: {backend}")