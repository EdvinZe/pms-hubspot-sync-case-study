import json
from pathlib import Path

from src.deduplication.dedupe_contacts import deduplicate_by_email
from src.hubspot.batch_retry_split import safe_batch_upsert
from src.hubspot.fake_hubspot_client import FakeHubSpotClient
from src.mapping.hostaway_mapper import map_hostaway_reservations
from src.mapping.hubspot_payload import to_hubspot_contact_payload
from src.sync.logger import log_event


DATA_PATH = Path(__file__).resolve().parents[2] / "data" / "hostaway_sample_reservations.json"


def run_hostaway_sync() -> dict:
    raw_records = json.loads(DATA_PATH.read_text())
    log_event("fetched_records", pms_platform="Hostaway", count=len(raw_records))

    mapped_records = map_hostaway_reservations(raw_records)
    clean_records, skipped_records = deduplicate_by_email(mapped_records)
    log_event("invalid_or_skipped_records", pms_platform="Hostaway", count=len(skipped_records))
    for skipped_record in skipped_records:
        log_event(
            "record_skipped_before_hubspot",
            pms_platform="Hostaway",
            reservation_id=skipped_record.get("reservation_id"),
            reason=skipped_record.get("skip_reason"),
        )
    log_event("duplicates_removed", pms_platform="Hostaway", count=len(mapped_records) - len(clean_records) - len(skipped_records))

    payloads = [payload for record in clean_records if (payload := to_hubspot_contact_payload(record)) is not None]
    log_event("payloads_prepared", pms_platform="Hostaway", count=len(payloads))

    result = safe_batch_upsert(FakeHubSpotClient(), payloads, batch_size=4)
    log_event("upsert_summary", pms_platform="Hostaway", upserted=len(result["successful"]), failed=len(result["failed"]))
    return {"clean_records": clean_records, "skipped_records": skipped_records, "upsert_result": result}


if __name__ == "__main__":
    run_hostaway_sync()
