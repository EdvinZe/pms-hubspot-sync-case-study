# Deduplication Strategy

HubSpot contacts are deduplicated by normalized email.

The representative implementation:

1. trims and lowercases email addresses
2. rejects missing or invalid email addresses
3. groups records by normalized email
4. chooses one best record per email
5. sends only clean records to the payload builder

When duplicate records exist, the latest `arrival_date` or `updated_at` wins. If dates are equal or unavailable, the record with more filled fields wins.

This prevents duplicate CRM contacts and avoids pushing bad data into HubSpot.

## Relationship to email identity resolution

Deduplication depends on email identity resolution. The integration first extracts and normalizes the email, then groups records by normalized email, then selects the best or latest record per email before creating the HubSpot payload.

This keeps the HubSpot upsert identity aligned with the deduplication key: one normalized email should produce one HubSpot Contact update or create operation.
