from src.core.email_identity import resolve_contact_identity


def to_hubspot_contact_payload(record: dict) -> dict | None:
    identity = resolve_contact_identity(record)
    if not identity["is_valid"]:
        return None

    email = identity["identity_value"]

    return {
        "idProperty": "email",
        "id": email,
        "email": email,
        "properties": {
            "email": email,
            "firstname": record.get("guest_first_name"),
            "lastname": record.get("guest_last_name"),
            "phone": record.get("guest_phone"),
            "property_name": record.get("listing_name"),
            "check_in": record.get("arrival_date"),
            "check_out": record.get("departure_date"),
            "source_system": record.get("booking_source"),
            "pms_platform": record.get("pms_platform"),
            "external_reservation_id": record.get("reservation_id"),
            "last_reservation_date": record.get("arrival_date"),
        },
    }
