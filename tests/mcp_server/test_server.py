import asyncio
from pathlib import Path

import pytest

from cloud_gpt.mcp_server.server import list_orders, mcp, run_orders_etl

SAMPLE_CSV = Path(__file__).resolve().parents[2] / "data" / "sales_sample.csv"


def test_tools_are_registered():
    tools = asyncio.run(mcp.list_tools())
    names = {tool.name for tool in tools}
    assert names == {"run_orders_etl", "list_orders"}


def test_run_orders_etl_tool(tmp_path):
    db_path = tmp_path / "orders.db"

    summary = run_orders_etl(str(SAMPLE_CSV), str(db_path))

    assert summary["extracted"] == 7
    assert summary["loaded"] == 3
    assert summary["rejected"] == 4
    assert {r["order_id"] for r in summary["rejections"]} == {"1003", "1004", "1005", "1001"}


def test_list_orders_tool_returns_rows(tmp_path):
    db_path = tmp_path / "orders.db"
    run_orders_etl(str(SAMPLE_CSV), str(db_path))

    rows = list_orders(str(db_path))

    assert {row["order_id"] for row in rows} == {"1001", "1002", "1006"}
    assert rows[0]["order_date"] >= rows[-1]["order_date"]


def test_list_orders_respects_limit(tmp_path):
    db_path = tmp_path / "orders.db"
    run_orders_etl(str(SAMPLE_CSV), str(db_path))

    rows = list_orders(str(db_path), limit=1)

    assert len(rows) == 1


def test_list_orders_missing_db_raises(tmp_path):
    with pytest.raises(FileNotFoundError):
        list_orders(str(tmp_path / "missing.db"))
