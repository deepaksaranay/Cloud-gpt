import pytest

from cloud_gpt.etl.extract import extract_csv


def test_extract_csv_reads_rows(tmp_path):
    csv_path = tmp_path / "orders.csv"
    csv_path.write_text("order_id,customer_name\n1,Alice\n2,Bob\n")

    rows = extract_csv(csv_path)

    assert rows == [
        {"order_id": "1", "customer_name": "Alice"},
        {"order_id": "2", "customer_name": "Bob"},
    ]


def test_extract_csv_missing_file(tmp_path):
    with pytest.raises(FileNotFoundError):
        extract_csv(tmp_path / "missing.csv")
