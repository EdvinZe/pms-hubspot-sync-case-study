from datetime import datetime, timezone


def log_event(event: str, **fields) -> dict:
    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "event": event,
        **fields,
    }
    print(entry)
    return entry
