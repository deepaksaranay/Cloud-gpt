"""MCP server exposing the orders ETL pipeline as tools for an LLM client."""

import sqlite3
from pathlib import Path

from mcp.server.mcpserver import MCPServer

from cloud_gpt.etl.pipeline import run_pipeline

mcp = MCPServer("cloud-gpt-orders")


@mcp.tool()
def run_orders_etl(source_csv: str, db_path: str) -> dict:
    """Extract, validate, and load an orders CSV file into a SQLite database."""
    summary = run_pipeline(source_csv, db_path)
    return {
        "extracted": summary["extracted"],
        "loaded": summary["loaded"],
        "rejected": summary["rejected"],
        "rejections": [
            {"order_id": row.get("order_id", "?"), "reason": reason}
            for row, reason in summary["rejections"]
        ],
    }


@mcp.tool()
def list_orders(db_path: str, limit: int = 50) -> list[dict]:
    """List orders stored in a SQLite database, most recent order_date first."""
    path = Path(db_path)
    if not path.is_file():
        raise FileNotFoundError(f"Database not found: {path}")

    with sqlite3.connect(path) as conn:
        conn.row_factory = sqlite3.Row
        rows = conn.execute(
            "SELECT * FROM orders ORDER BY order_date DESC LIMIT ?", (limit,)
        ).fetchall()
    return [dict(row) for row in rows]


def main() -> None:
    mcp.run()


if __name__ == "__main__":
    main()
