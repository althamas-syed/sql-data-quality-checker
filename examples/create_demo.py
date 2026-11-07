import sqlite3
from pathlib import Path

db = Path(__file__).with_name("demo.db")
with sqlite3.connect(db) as con:
    con.execute("DROP TABLE IF EXISTS sales")
    con.execute("CREATE TABLE sales (order_id INTEGER, amount REAL, category TEXT)")
    con.executemany("INSERT INTO sales VALUES (?,?,?)", [
        (1, 100.0, "Books"),
        (1, 100.0, "Books"),
        (2, None, "Grocery"),
        (3, -20.0, "Returns")
    ])
print(f"Created {db}")
