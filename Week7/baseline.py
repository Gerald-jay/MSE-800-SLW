import sqlite3

class UserRepoBaseline:
    def __init__(self, db_path: str = "app.db"):
        self.db_path = db_path

    def get_names(self, repeats: int = 1) -> list[str]:
        out = []
        for _ in range(repeats):
            conn = sqlite3.connect(self.db_path)
            cur = conn.execute("SELECT name FROM users ORDER BY id")
            out.extend([r[0] for r in cur.fetchall()])
            conn.close()
        return out
