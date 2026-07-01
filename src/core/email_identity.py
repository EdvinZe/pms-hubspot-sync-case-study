import re


EMAIL_PATTERN = re.compile(r"^[A-Za-z0-9.!#$%&'*+/=?^_`{|}~-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")


def extract_email(record: dict) -> str | None:
    """Extract the guest email from a normalized PMS record."""
    email = record.get("guest_email")
    return email if isinstance(email, str) else None


def normalize_email(email: str | None) -> str | None:
    """Trim and lowercase an email address without validating it."""
    if email is None:
        return None

    normalized = email.strip().lower()
    return normalized or None


def is_valid_email(email: str | None) -> bool:
    """Return whether an email is present and has a simple valid format."""
    normalized = normalize_email(email)
    return bool(normalized and EMAIL_PATTERN.match(normalized))


def resolve_contact_identity(record: dict) -> dict:
    """Resolve the normalized HubSpot Contact identity from a PMS record."""
    raw_email = extract_email(record)
    normalized_email = normalize_email(raw_email)

    if normalized_email is None:
        return {
            "identity_key": "email",
            "identity_value": None,
            "is_valid": False,
            "reason": "missing_email",
        }

    if not is_valid_email(normalized_email):
        return {
            "identity_key": "email",
            "identity_value": None,
            "is_valid": False,
            "reason": "invalid_email",
        }

    return {
        "identity_key": "email",
        "identity_value": normalized_email,
        "is_valid": True,
        "reason": None,
    }
