from cloud_gpt.etl.transform import transform


def make_row(**overrides):
    row = {
        "order_id": "1001",
        "customer_name": " Alice Nguyen ",
        "email": "Alice@Example.com",
        "product": "Widget",
        "quantity": "3",
        "unit_price": "9.99",
        "order_date": "2024-01-15",
    }
    row.update(overrides)
    return row


def test_valid_row_is_cleaned_and_totaled():
    result = transform([make_row()])

    assert result.rejected == []
    assert result.records == [
        {
            "order_id": "1001",
            "customer_name": "Alice Nguyen",
            "email": "alice@example.com",
            "product": "Widget",
            "quantity": 3,
            "unit_price": 9.99,
            "total_price": 29.97,
            "order_date": "2024-01-15",
        }
    ]


def test_missing_required_field_is_rejected():
    result = transform([make_row(customer_name="")])

    assert result.records == []
    assert result.rejected[0][1] == "missing customer_name"


def test_invalid_email_is_rejected():
    result = transform([make_row(email="not-an-email")])

    assert result.rejected[0][1] == "invalid email"


def test_invalid_order_date_is_rejected():
    result = transform([make_row(order_date="15-01-2024")])

    assert result.rejected[0][1] == "invalid order_date"


def test_non_positive_quantity_is_rejected():
    result = transform([make_row(quantity="-1")])

    assert result.rejected[0][1] == "quantity must be positive"


def test_non_positive_unit_price_is_rejected():
    result = transform([make_row(unit_price="0")])

    assert result.rejected[0][1] == "unit_price must be positive"


def test_duplicate_order_id_keeps_first_and_rejects_rest():
    result = transform([make_row(), make_row(customer_name="Someone Else")])

    assert len(result.records) == 1
    assert result.records[0]["customer_name"] == "Alice Nguyen"
    assert result.rejected[0][1] == "duplicate order_id"
