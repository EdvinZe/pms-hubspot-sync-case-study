from collections import defaultdict
from datetime import datetime
from typing import Any

from src.core.email_identity import resolve_contact_identity


def count_filled_fields(record: dict) -> int:
    return sum(1 for value in record.values() if value not in (None, "", [], {}))


def _parse_date(value: Any) -> datetime:
    if not value:
        return datetime.min
    try:
        return datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    except ValueError:
        return datetime.min


def choose_best_record(records: list[dict]) -> dict:
    def score(record: dict) -> tuple[datetime, datetime, int]:
        return (
            _parse_date(record.get("arrival_date")),
            _parse_date(record.get("updated_at")),
            count_filled_fields(record),
        )

    return max(records, key=score)


def deduplicate_by_email(records: list[dict]) -> tuple[list[dict], list[dict]]:
    # This prevents duplicate CRM contacts and avoids pushing bad data into HubSpot.
    grouped: dict[str, list[dict]] = defaultdict(list)
    skipped: list[dict] = []

    for record in records:
        identity = resolve_contact_identity(record)
        if not identity["is_valid"]:
            skipped.append({**record, "skip_reason": identity["reason"]})
            continue

        normalized_email = identity["identity_value"]
        grouped[normalized_email].append({**record, "guest_email": normalized_email})

    clean_records = [choose_best_record(email_records) for email_records in grouped.values()]
    return clean_records, skipped
