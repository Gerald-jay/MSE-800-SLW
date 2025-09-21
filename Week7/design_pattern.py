import sqlite3
from contextlib import contextmanager
from dataclasses import dataclass
from typing import Iterable, Optional, Any, Dict, List

# ---------------------------
# Connection Factory (DI target)
# ---------------------------
class SQLiteConnectionFactory:
    def __init__(self, dsn: str = "app.db"):
        self._dsn = dsn

    @contextmanager
    def connect(self):
        conn = sqlite3.connect(self._dsn)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
        finally:
            conn.close()

# ---------------------------
# Repository Layer
# ---------------------------
class UserRepository:
    def __init__(self, conn_factory: SQLiteConnectionFactory):
        self._cf = conn_factory

    def get_by_id(self, user_id: int) -> Optional[Dict[str, Any]]:
        sql = "SELECT * FROM users WHERE id = ?"
        with self._cf.connect() as conn:
            cur = conn.execute(sql, (user_id,))
            row = cur.fetchone()
            return dict(row) if row else None

class OrderRepository:
    def __init__(self, conn_factory: SQLiteConnectionFactory):
        self._cf = conn_factory

    def list_by_user(self, user_id: int) -> List[Dict[str, Any]]:
        sql = "SELECT * FROM orders WHERE user_id = ?"
        with self._cf.connect() as conn:
            cur = conn.execute(sql, (user_id,))
            return [dict(r) for r in cur.fetchall()]

# ---------------------------
# Service Layer (depends on repositories)
# ---------------------------
@dataclass
class UserService:
    users: UserRepository

    def get_user(self, user_id: int) -> Optional[Dict[str, Any]]:
        return self.users.get_by_id(user_id)

@dataclass
class OrderService:
    orders: OrderRepository

    def get_orders(self, user_id: int) -> List[Dict[str, Any]]:
        return self.orders.list_by_user(user_id)

# ---------------------------
# Composition Root (wire DI)
# ---------------------------
def build_services(db_path: str = "app.db") -> tuple[UserService, OrderService]:
    cf = SQLiteConnectionFactory(db_path)
    user_repo = UserRepository(cf)
    order_repo = OrderRepository(cf)
    return UserService(user_repo), OrderService(order_repo)

# ---------------------------
# Example usage
# ---------------------------
if __name__ == "__main__":
    user_svc, order_svc = build_services()
    user = user_svc.get_user(1)
    orders = order_svc.get_orders(1)
    print("User:", user)
    print("Orders:", orders)
