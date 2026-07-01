from src.hubspot.batch_retry_split import safe_batch_upsert
from src.hubspot.fake_hubspot_client import FakeHubSpotClient


def test_batch_split_retry_isolates_one_bad_record():
    payloads = [
        {"email": "one@example.com", "properties": {"email": "one@example.com"}},
        {"email": "invalid-email", "properties": {"email": "invalid-email"}},
        {"email": "two@example.com", "properties": {"email": "two@example.com"}},
    ]

    result = safe_batch_upsert(FakeHubSpotClient(), payloads, batch_size=3)

    assert [payload["email"] for payload in result["successful"]] == ["one@example.com", "two@example.com"]
    assert [payload["email"] for payload in result["failed"]] == ["invalid-email"]
    assert any(log["event"] == "failed_record_isolated" for log in result["logs"])


def test_conflict_record_is_marked_failed_with_conflict_action():
    payloads = [
        {"email": "conflict@example.com", "properties": {"email": "conflict@example.com"}},
    ]

    result = safe_batch_upsert(FakeHubSpotClient(), payloads, batch_size=1)

    assert len(result["failed"]) == 1
    assert result["failed"][0]["conflict"]["action"] == "update_existing_contact"
