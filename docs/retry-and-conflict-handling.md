# Retry And Conflict Handling

HubSpot batch APIs can reject an entire batch because of one bad record.

This representative implementation uses a production-style split retry strategy:

1. submit a batch
2. if it fails, split it into smaller batches
3. retry each smaller batch
4. isolate individual failed records
5. continue syncing valid records

Conflict handling is represented without real API calls. The sanitized case study shows how an integration can retry individually, update an existing CRM record when a conflict identifier is known, or mark a record for manual review.
