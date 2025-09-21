import sqlite3
from time import perf_counter
from pathlib import Path
from baseline import UserRepoBaseline
from singleton import UserRepoSingleton

DB_PATH = "app.db"

def ensure_db():
    here = Path(__file__).resolve().parent           # bench.py 所在目录
    sql_path = here / "schema.sql"                   # 拼出绝对路径
    sql = sql_path.read_text(encoding="utf-8")
    conn = sqlite3.connect(DB_PATH)
    conn.executescript(sql)
    conn.close()

def bench(repo_cls, label: str, repeats: int = 500):
    repo = repo_cls(DB_PATH)
    t0 = perf_counter()
    result = repo.get_names(repeats=repeats)
    dt = perf_counter() - t0
    return label, dt, result

if __name__ == "__main__":
    ensure_db()
    repeats = 1000

    b_label, b_time, b_res = bench(UserRepoBaseline, "baseline", repeats)
    s_label, s_time, s_res = bench(UserRepoSingleton, "singleton", repeats)

    assert b_res == s_res, "Results differ between baseline and singleton!"

    print(f"{b_label:9s} time: {b_time:.4f}s")
    print(f"{s_label:9s} time: {s_time:.4f}s")
    speedup = b_time / s_time if s_time > 0 else float('inf')
    print(f"Speedup (baseline/singleton): {speedup:.2f}x")
