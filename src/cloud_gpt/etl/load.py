import sqlite3
from pathlib import Path

SCHEMA = """
CREATE TABLE IF NOT EXISTS {table} (
    order_id TEXT PRIMARY KEY,
    customer_name TEXT NOT NULL,
    email TEXT NOT NULL,
    product TEXT NOT NULL,
    quantity INTEGER NOT NULL,
    unit_price REAL NOT NULL,
    total_price REAL NOT NULL,
    order_date TEXT NOT NULL
)
"""


def load_to_sqlite(records: list[dict], db_path: str | Path, table: str = "orders") -> int:
    """Idempotently upsert records into a SQLite table, returning the row count loaded."""
    with sqlite3.connect(db_path) as conn:
        conn.execute(SCHEMA.format(table=table))
        conn.executemany(
            f"""
            INSERT OR REPLACE INTO {table}
                (order_id, customer_name, email, product, quantity, unit_price, total_price, order_date)
            VALUES
                (:order_id, :customer_name, :email, :product, :quantity, :unit_price, :total_price, :order_date)
            """,
            records,
        )
        conn.commit()
    return len(records)
