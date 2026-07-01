def handle_conflict(record: dict, error: dict) -> dict:
    conflict_id = error.get("conflict_id")

    if conflict_id:
        return {
            "action": "update_existing_contact",
            "conflict_id": conflict_id,
            "record": record,
        }

    return {
        "action": "mark_for_review",
        "reason": "unresolved_conflict",
        "record": record,
    }
