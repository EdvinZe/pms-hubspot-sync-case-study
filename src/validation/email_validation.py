from src.core.email_identity import is_valid_email as _is_valid_email
from src.core.email_identity import normalize_email as _normalize_email


def normalize_email(email: str | None) -> str | None:
    """Return a normalized email only when it is valid."""
    normalized = _normalize_email(email)
    return normalized if _is_valid_email(normalized) else None


def is_valid_email(email: str | None) -> bool:
    """Return whether an email is present and has a simple valid format."""
    return _is_valid_email(email)
