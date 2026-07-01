def map_hostaway_reservation(raw: dict) -> dict:
    return {
        "reservation_id": raw.get("id"),
        "guest_email": raw.get("customer_email"),
        "guest_first_name": raw.get("customer_first_name"),
        "guest_last_name": raw.get("customer_last_name"),
        "guest_phone": raw.get("customer_phone"),
        "listing_name": raw.get("property"),
        "arrival_date": raw.get("check_in"),
        "departure_date": raw.get("check_out"),
        "booking_source": raw.get("channel"),
        "status": raw.get("reservation_status"),
        "updated_at": raw.get("modified_at"),
        "pms_platform": "Hostaway",
    }


def map_hostaway_reservations(raw_records: list[dict]) -> list[dict]:
    return [map_hostaway_reservation(record) for record in raw_records]
