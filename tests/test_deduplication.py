from src.deduplication.dedupe_contacts import deduplicate_by_email


def test_deduplication_by_email_normalizes_case_and_spaces():
    records = [
        {"guest_email": " DUPLICATE@example.com ", "arrival_date": "2026-07-01", "updated_at": "2026-06-01T00:00:00Z"},
        {"guest_email": "duplicate@example.com", "arrival_date": "2026-07-02", "updated_at": "2026-06-02T00:00:00Z"},
    ]

    clean, skipped = deduplicate_by_email(records)

    assert len(clean) == 1
    assert clean[0]["guest_email"] == "duplicate@example.com"
    assert skipped == []


def test_latest_record_wins():
    records = [
        {"guest_email": "demo@example.com", "arrival_date": "2026-07-01", "updated_at": "2026-06-01T00:00:00Z", "reservation_id": "old"},
        {"guest_email": "demo@example.com", "arrival_date": "2026-08-01", "updated_at": "2026-06-01T00:00:00Z", "reservation_id": "new"},
    ]

    clean, _ = deduplicate_by_email(records)

    assert clean[0]["reservation_id"] == "new"


def test_more_complete_record_wins_when_dates_are_equal():
    records = [
        {"guest_email": "demo@example.com", "arrival_date": "2026-07-01", "updated_at": "2026-06-01T00:00:00Z", "guest_phone": ""},
        {"guest_email": "demo@example.com", "arrival_date": "2026-07-01", "updated_at": "2026-06-01T00:00:00Z", "guest_phone": "+10000000000"},
    ]

    clean, _ = deduplicate_by_email(records)

    assert clean[0]["guest_phone"] == "+10000000000"


def test_invalid_or_missing_emails_are_skipped():
    records = [
        {"guest_email": "invalid-email"},
        {"guest_email": None},
        {"guest_email": "valid@example.com"},
    ]

    clean, skipped = deduplicate_by_email(records)

    assert len(clean) == 1
    assert len(skipped) == 2
