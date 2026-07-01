from src.mapping.hubspot_payload import to_hubspot_contact_payload


def test_payload_mapping_produces_expected_hubspot_properties():
    record = {
        "reservation_id": "demo-001",
        "guest_email": " John.Smith@Example.com ",
        "guest_first_name": "John",
        "guest_last_name": "Smith",
        "guest_phone": "+10000000000",
        "listing_name": "Demo Apartment A",
        "arrival_date": "2026-07-10",
        "departure_date": "2026-07-14",
        "booking_source": "Direct",
        "pms_platform": "Guesty",
    }

    payload = to_hubspot_contact_payload(record)

    assert payload["email"] == "john.smith@example.com"
    assert payload["properties"] == {
        "email": "john.smith@example.com",
        "firstname": "John",
        "lastname": "Smith",
        "phone": "+10000000000",
        "property_name": "Demo Apartment A",
        "check_in": "2026-07-10",
        "check_out": "2026-07-14",
        "source_system": "Direct",
        "pms_platform": "Guesty",
        "external_reservation_id": "demo-001",
        "last_reservation_date": "2026-07-10",
    }
