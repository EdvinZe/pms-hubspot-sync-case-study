# Hostaway → HubSpot

The Hostaway case-study flow uses intentionally messy sanitized sample data to show why integrations need normalization before CRM writes.

Examples include:

- mixed email casing
- extra whitespace
- missing phone values
- missing listing names
- invalid emails
- cancelled reservations

The mapper hides platform shape differences and returns the same normalized PMS record fields used by the Guesty flow.

From that point forward, Hostaway records use the same shared HubSpot sync core: email identity resolution, validation, deduplication, payload mapping, batch upsert, retry handling and structured logging.
