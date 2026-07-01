def map_guesty_reservation(raw: dict) -> dict:
    guest = raw.get("guest", {})
    stay = raw.get("stay", {})

    return {
        "reservation_id": raw.get("reservation_id"),
        "guest_email": guest.get("email"),
        "guest_first_name": guest.get("first_name"),
        "guest_last_name": guest.get("last_name"),
        "guest_phone": guest.get("phone"),
        "listing_name": stay.get("listing_name"),
        "arrival_date": stay.get("arrival_date"),
        "departure_date": stay.get("departure_date"),
        "booking_source": raw.get("booking_source"),
        "status": raw.get("status"),
        "updated_at": raw.get("updated_at"),
        "pms_platform": "Guesty",
    }


def map_guesty_reservations(raw_records: list[dict]) -> list[dict]:
    return [map_guesty_reservation(record) for record in raw_records]
