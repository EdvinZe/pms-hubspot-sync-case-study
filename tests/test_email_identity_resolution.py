from src.core.email_identity import (
    extract_email,
    is_valid_email,
    normalize_email,
    resolve_contact_identity,
)
from src.mapping.hubspot_payload import to_hubspot_contact_payload


def test_extracts_guest_email_from_pms_record():
    record = {"guest_email": "john.smith@example.com"}

    assert extract_email(record) == "john.smith@example.com"


def test_normalize_email_trims_whitespace():
    assert normalize_email("  john.smith@example.com ") == "john.smith@example.com"


def test_normalize_email_lowercases_email():
    assert normalize_email("JOHN.SMITH@EXAMPLE.COM") == "john.smith@example.com"


def test_rejects_missing_email():
    identity = resolve_contact_identity({"guest_email": "  "})

    assert identity == {
        "identity_key": "email",
        "identity_value": None,
        "is_valid": False,
        "reason": "missing_email",
    }


def test_rejects_invalid_email():
    identity = resolve_contact_identity({"guest_email": "invalid-email"})

    assert identity == {
        "identity_key": "email",
        "identity_value": None,
        "is_valid": False,
        "reason": "invalid_email",
    }
    assert is_valid_email("invalid-email") is False


def test_returns_normalized_email_as_identity_value():
    identity = resolve_contact_identity({"guest_email": "  JOHN.SMITH@EXAMPLE.COM "})

    assert identity["identity_value"] == "john.smith@example.com"


def test_returns_identity_key_email():
    identity = resolve_contact_identity({"guest_email": "john.smith@example.com"})

    assert identity["identity_key"] == "email"


def test_hubspot_payload_uses_normalized_email_as_id_and_property_email():
    record = {
        "reservation_id": "demo-1001",
        "guest_email": "  JOHN.SMITH@EXAMPLE.COM ",
        "guest_first_name": "John",
        "guest_last_name": "Smith",
        "arrival_date": "2026-07-10",
    }

    payload = to_hubspot_contact_payload(record)

    assert payload["idProperty"] == "email"
    assert payload["id"] == "john.smith@example.com"
    assert payload["properties"]["email"] == "john.smith@example.com"


def test_hubspot_payload_skips_invalid_email():
    assert to_hubspot_contact_payload({"guest_email": "invalid-email"}) is None
