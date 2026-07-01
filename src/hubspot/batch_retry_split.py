from src.hubspot.conflict_handler import handle_conflict


def _payload_email(payload: dict) -> str | None:
    return payload.get("id") or payload.get("email")


def _chunks(items: list[dict], size: int) -> list[list[dict]]:
    return [items[index : index + size] for index in range(0, len(items), size)]


def safe_batch_upsert(client, payloads: list[dict], batch_size: int = 100) -> dict:
    result = {"successful": [], "failed": [], "logs": []}

    for batch in _chunks(payloads, batch_size):
        _upsert_with_split(client, batch, result)

    return result


def _upsert_with_split(client, payloads: list[dict], result: dict) -> None:
    if not payloads:
        return

    response = client.batch_upsert_contacts(payloads)
    if response.get("ok"):
        result["successful"].extend(payloads)
        result["logs"].append({"event": "batch_upsert_success", "count": len(payloads)})
        return

    error = response.get("error", {})
    result["logs"].append({"event": "batch_upsert_failed", "count": len(payloads), "error": error})

    # HubSpot batch APIs can reject the whole batch because of one bad record.
    # Splitting prevents one bad record from blocking all valid records.
    if len(payloads) == 1:
        payload = payloads[0]
        if error.get("type") == "conflict":
            conflict = handle_conflict(payload, error)
            result["failed"].append({**payload, "error": error, "conflict": conflict})
            result["logs"].append({"event": "conflict_record_isolated", "email": _payload_email(payload)})
            return

        result["failed"].append({**payload, "error": error})
        result["logs"].append({"event": "failed_record_isolated", "email": _payload_email(payload)})
        return

    midpoint = len(payloads) // 2
    _upsert_with_split(client, payloads[:midpoint], result)
    _upsert_with_split(client, payloads[midpoint:], result)
