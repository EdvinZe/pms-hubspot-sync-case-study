# Guesty → HubSpot

The Guesty case-study flow loads sanitized sample reservation records from `data/guesty_sample_reservations.json`.

This represents the platform-specific adapter side of the public technical sample. The adapter converts Guesty-shaped reservation data into the shared PMS record used by the HubSpot sync core.

The mapper converts platform-flavored input into a normalized PMS record with generic fields:

- `reservation_id`
- `guest_email`
- `guest_first_name`
- `guest_last_name`
- `guest_phone`
- `listing_name`
- `arrival_date`
- `departure_date`
- `booking_source`
- `status`
- `updated_at`
- `pms_platform`

From there, the shared email identity resolution, validation, deduplication, payload mapping, batch upsert, retry and logging logic handles the representative integration workflow.
