# Email-Based Contact Identity Resolution

In PMS -> HubSpot integrations, email is the safest available cross-system identity key for HubSpot Contacts.

Before a contact can be updated or upserted in HubSpot, the integration must:

- extract the guest email from Guesty or Hostaway reservation data
- trim whitespace
- lowercase the email
- validate the email format
- reject missing or invalid emails
- use the normalized email as the HubSpot contact identity
- prevent duplicate contacts from being created
- update the existing HubSpot contact when the same email appears again

This repository shows a representative implementation for a sanitized case study. It demonstrates a production-style pattern based on real commercial automation work without including private implementation code, private records, secrets, logs or client-specific business logic.

## Why this mattered

Guesty and Hostaway can send guest and reservation records with inconsistent or messy email data:

- email casing differences
- leading or trailing spaces
- missing emails
- invalid emails
- duplicate guests across multiple reservations
- multiple reservations linked to the same guest

Without email identity resolution, the sync could:

- create duplicate HubSpot contacts
- fail HubSpot validation
- update the wrong contact
- lose the latest reservation data
- reject an entire batch because of one bad record

Resolving the contact identity early gives the shared HubSpot sync layer one stable key to trust before deduplication, payload mapping and batch upsert.

## Architecture

```text
Guesty / Hostaway record
  -> Extract guest_email
  -> Normalize email
  -> Validate email
  -> Use email as contact identity
  -> Build HubSpot payload
  -> Upsert by email
  -> Update existing contact or create new contact
```

## Sanitized example

Input PMS records:

```json
[
  {
    "reservation_id": "demo-1001",
    "guest_email": "  JOHN.SMITH@EXAMPLE.COM ",
    "guest_first_name": "John",
    "guest_last_name": "Smith",
    "arrival_date": "2026-07-10"
  },
  {
    "reservation_id": "demo-1002",
    "guest_email": "john.smith@example.com",
    "guest_first_name": "John",
    "guest_last_name": "Smith",
    "arrival_date": "2026-08-15"
  }
]
```

Both records belong to the same HubSpot contact after email normalization:

```text
john.smith@example.com
```

The integration should send one clean HubSpot contact payload using email as the identity key:

```json
{
  "idProperty": "email",
  "id": "john.smith@example.com",
  "properties": {
    "email": "john.smith@example.com",
    "firstname": "John",
    "lastname": "Smith",
    "phone": null,
    "property_name": null,
    "check_in": "2026-08-15",
    "check_out": null,
    "source_system": null,
    "pms_platform": null,
    "external_reservation_id": "demo-1002",
    "last_reservation_date": "2026-08-15"
  }
}
```

Missing or invalid emails are skipped before the HubSpot payload is built, and the representative sync logs the skip reason with the reservation identifier when available.
