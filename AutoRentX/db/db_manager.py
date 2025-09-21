"""
db_manager.py
Database Manager (Peewee ORM + persistent connection, Singleton)
"""

from peewee import SqliteDatabase

# Use a single consistent database filename
DB_PATH = "car_rental.db"


class DatabaseManager:
    """
    DatabaseManager implemented as a Singleton.
    Ensures only one SqliteDatabase instance exists across the app.
    """
    _instance = None
    _db: SqliteDatabase | None = None

    def __new__(cls, path: str = DB_PATH):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            # Initialize database connection
            cls._db = SqliteDatabase(
                path,
                pragmas={
                    "foreign_keys": 1,  # Enable foreign key constraints
                    "synchronous": 0,  # synchronous mode off
                    "journal_mode": "wal",  # Write-ahead logging mode for better concurrency
                    "cache_size": -1024 * 64,  # Optimize cache
                },
            )
            if cls._db.is_closed():
                cls._db.connect()
            print(f"Database connected: {path}")
        return cls._instance

    @property
    def db(self) -> SqliteDatabase:
        if self._db is None:
            raise RuntimeError("Database connection is not initialized")
        return self._db

    def close(self):
        """Close connection safely"""
        if self._db and not self._db.is_closed():
            self._db.close()
            print("Database closed")
