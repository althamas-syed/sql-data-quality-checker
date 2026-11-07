import sqlite3
import unittest
from sql_quality.cli import inspect_table, quote_identifier

class QualityTests(unittest.TestCase):
    def test_counts(self):
        with sqlite3.connect(":memory:") as db:
            db.execute("CREATE TABLE sales (id INTEGER, amount REAL)")
            db.executemany("INSERT INTO sales VALUES (?,?)", [(1,10),(1,10),(2,None)])
            result = inspect_table(db, "sales")
        self.assertEqual(result["rows"], 3)
        self.assertEqual(result["duplicate_rows"], 1)
        self.assertEqual(result["null_counts"]["amount"], 1)

    def test_missing_table(self):
        with sqlite3.connect(":memory:") as db:
            with self.assertRaises(ValueError):
                inspect_table(db, "missing")

    def test_identifier_escape(self):
        self.assertEqual(quote_identifier('a"b'), '"a""b"')

if __name__ == "__main__":
    unittest.main()
