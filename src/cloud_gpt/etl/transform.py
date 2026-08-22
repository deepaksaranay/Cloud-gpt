import re
from dataclasses import dataclass, field
from datetime import date

REQUIRED_FIELDS = ("order_id", "customer_name", "email", "product", "order_date")
EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


@dataclass
class TransformResult:
    records: list[dict] = field(default_factory=list)
    rejected: list[tuple[dict, str]] = field(default_factory=list)


def _validate(row: dict) -> str | None:
    """Return a rejection reason, or None if the row is valid."""
    for name in REQUIRED_FIELDS:
        if not row.get(name, "").strip():
            return f"missing {name}"

    if not EMAIL_RE.match(row["email"].strip()):
        return "invalid email"

    try:
        date.fromisoformat(row["order_date"].strip())
    except ValueError:
        return "invalid order_date"

    try:
        quantity = int(row["quantity"])
        unit_price = float(row["unit_price"])
    except (KeyError, ValueError):
        return "invalid quantity or unit_price"

    if quantity <= 0:
        return "quantity must be positive"
    if unit_price <= 0:
        return "unit_price must be positive"

    return None


def transform(rows: list[dict]) -> TransformResult:
    """Validate, clean, and dedupe raw CSV rows into loadable order records."""
    result = TransformResult()
    seen_order_ids: set[str] = set()

    for row in rows:
        reason = _validate(row)
        if reason:
            result.rejected.append((row, reason))
            continue

        order_id = row["order_id"].strip()
        if order_id in seen_order_ids:
            result.rejected.append((row, "duplicate order_id"))
            continue
        seen_order_ids.add(order_id)

        quantity = int(row["quantity"])
        unit_price = float(row["unit_price"])
        result.records.append(
            {
                "order_id": order_id,
                "customer_name": row["customer_name"].strip(),
                "email": row["email"].strip().lower(),
                "product": row["product"].strip(),
                "quantity": quantity,
                "unit_price": unit_price,
                "total_price": round(quantity * unit_price, 2),
                "order_date": row["order_date"].strip(),
            }
        )

    return result
