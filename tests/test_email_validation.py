from src.validation.email_validation import is_valid_email, normalize_email


def test_normalize_email_trims_and_lowercases():
    assert normalize_email(" Anna.Demo@Example.com ") == "anna.demo@example.com"


def test_normalize_email_returns_none_for_empty_or_none():
    assert normalize_email(None) is None
    assert normalize_email("  ") is None


def test_invalid_email_filtering():
    assert is_valid_email("invalid-email") is False
    assert is_valid_email("john.smith@example.com") is True
