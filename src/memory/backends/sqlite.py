import aiosqlite
import os
from datetime import datetime
from typing import List, Dict, Optional
from ..base import BaseMemory

class SQLiteMemory(BaseMemory):
    def __init__(self, db_path: str = "data/friday.db"):
        self.db_path = db_path
        # Ensure the data directory exists
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)

    async def _init_db(self):
        async with aiosqlite.connect(self.db_path) as db:
            # Future-proofed schema with score and embedding columns
            await db.execute("""
                CREATE TABLE IF NOT EXISTS facts (
                    user_id TEXT,
                    key TEXT,
                    value TEXT,
                    updated_at TIMESTAMP,
                    score REAL,
                    embedding BLOB,
                    PRIMARY KEY(user_id, key)
                )
            """)
            await db.commit()

    async def remember(self, user_id: str, key: str, value: str, ttl: Optional[int] = None) -> None:
        await self._init_db()
        async with aiosqlite.connect(self.db_path) as db:
            # SQLite ignores TTL, just upserts the value
            await db.execute("""
                INSERT INTO facts (user_id, key, value, updated_at)
                VALUES (?, ?, ?, ?)
                ON CONFLICT(user_id, key) DO UPDATE SET
                    value=excluded.value,
                    updated_at=excluded.updated_at
            """, (user_id, key, value, datetime.utcnow()))
            await db.commit()

    async def recall(self, user_id: str, query: Optional[str] = None, limit: int = 5) -> List[Dict[str, str]]:
        await self._init_db()
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            # v0 ignores 'query' and just grabs the most recently updated facts
            cursor = await db.execute("""
                SELECT key, value FROM facts 
                WHERE user_id = ? 
                ORDER BY updated_at DESC LIMIT ?
            """, (user_id, limit))
            rows = await cursor.fetchall()
            return [{"key": row["key"], "value": row["value"]} for row in rows]