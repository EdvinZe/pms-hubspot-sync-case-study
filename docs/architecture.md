# Architecture

This sanitized case study uses a representative pipeline that mirrors production-style integration patterns without calling real APIs.

```text
Guesty / Hostaway
  → Platform Adapter
  → Normalized PMS Record
  → Email Identity Resolution
  → Validation
  → Deduplication
  → HubSpot Payload Builder
  → Batch Upsert
  → Retry / Conflict Handler
  → Structured Logs
```

The integration boundary is deliberately narrow. Guesty and Hostaway records are first normalized into a shared PMS record shape, then the rest of the pipeline can process either platform consistently.

Guesty and Hostaway have different source data shapes, but both flow into the same shared integration core. This keeps platform-specific mapping separate from shared CRM sync logic.

Platform adapters handle Guesty and Hostaway data shape differences. Email identity resolution creates the stable contact key used by the shared HubSpot sync layer, so validation, deduplication and HubSpot payload mapping all work from the same normalized email identity.
