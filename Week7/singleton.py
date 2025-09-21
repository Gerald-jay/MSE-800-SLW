import sqlite3
from typing import Optional

class DB:
    _instance: Optional["DB"] = None
    _conn: Optional[sqlite3.Connection] = None

    def __new__(cls, db_path: str = "app.db"):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._conn = sqlite3.connect(db_path, check_same_thread=False)
        return cls._instance

    @property
    def conn(self) -> sqlite3.Connection:
        assert self._conn is not None, "Database connection is not initialized"
        return self._conn

class UserRepoSingleton:
    def __init__(self, db_path: str = "app.db"):
        self.db = DB(db_path)

    def get_names(self, repeats: int = 1) -> list[str]:
        out = []
        for _ in range(repeats):
            cur = self.db.conn.execute("SELECT name FROM users ORDER BY id")
            out.extend([r[0] for r in cur.fetchall()])
        return out
