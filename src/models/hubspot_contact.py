from dataclasses import dataclass


@dataclass
class HubSpotContact:
    email: str
    firstname: str | None
    lastname: str | None
    phone: str | None
    property_name: str | None
    check_in: str | None
    check_out: str | None
    source_system: str | None
    pms_platform: str | None
    external_reservation_id: str | None
    last_reservation_date: str | None
