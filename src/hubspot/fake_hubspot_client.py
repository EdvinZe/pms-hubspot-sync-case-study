from src.validation.email_validation import is_valid_email


def _payload_email(payload: dict) -> str | None:
    return payload.get("id") or payload.get("email")


class FakeHubSpotClient:
    def __init__(self, conflict_emails: set[str] | None = None):
        self.conflict_emails = conflict_emails or {"conflict@example.com"}
        self.upserted: list[dict] = []

    def batch_upsert_contacts(self, payloads: list[dict]) -> dict:
        bad_payloads = [payload for payload in payloads if not is_valid_email(_payload_email(payload))]
        conflicts = [payload for payload in payloads if _payload_email(payload) in self.conflict_emails]

        if bad_payloads:
            return {
                "ok": False,
                "error": {
                    "type": "invalid_email",
                    "message": "Batch rejected because one record has an invalid email.",
                },
            }

        if conflicts:
            return {
                "ok": False,
                "error": {
                    "type": "conflict",
                    "message": "Batch rejected because one record conflicts with an existing contact.",
                    "conflict_id": "demo-existing-contact-id",
                },
            }

        self.upserted.extend(payloads)
        return {"ok": True, "results": payloads}
