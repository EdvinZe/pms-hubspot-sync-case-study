from dataclasses import dataclass


@dataclass
class PMSRecord:
    reservation_id: str
    guest_email: str | None
    guest_first_name: str | None
    guest_last_name: str | None
    guest_phone: str | None
    listing_name: str | None
    arrival_date: str | None
    departure_date: str | None
    booking_source: str | None
    status: str | None
    updated_at: str | None
    pms_platform: str
