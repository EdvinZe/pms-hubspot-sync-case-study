Built by Edvin Zenevič — Automation & Integration Engineer · [ezenevic.com](https://www.ezenevic.com/) · [LinkedIn](https://www.linkedin.com/in/edvin-zenevic/)


# PMS → HubSpot Sync Case Study

Sanitized public case study based on real commercial automation work: Guesty → HubSpot and Hostaway → HubSpot data sync workflows.

The production implementations were delivered for a real client and remain private.  
This repository shows a safe, anonymized version of the architecture, data flow and engineering patterns used in that work.

Built to demonstrate how real-world integrations handle messy data before it reaches the CRM.

A key part of the commercial work was making sure the sync updated the correct HubSpot contact by resolving and normalizing the guest email before deduplication and upsert.

## Overview

This repository is a public technical sample for an Automation & Integration Engineer portfolio. It shows how PMS guest and reservation data can be normalized, validated, deduplicated, mapped and synced into HubSpot Contacts using production-style data quality handling.

## Commercial work represented

This case study is based on two commercial automation integrations:

- Guesty → HubSpot CRM sync
- Hostaway → HubSpot CRM sync

Both integrations synced PMS guest/reservation data into HubSpot Contacts.

The platform-specific part:

- mapping Guesty data into a normalized internal record
- mapping Hostaway data into a normalized internal record

The shared integration core:

- email identity resolution
- email normalization and validation
- deduplication by normalized email
- best/latest record selection
- HubSpot contact payload mapping
- batch upsert handling
- recursive batch split retry
- conflict handling
- structured logging
- scheduled sync structure

## What this repository demonstrates

- PMS data normalization
- email-based contact identity resolution
- normalized email as HubSpot upsert identity
- invalid/missing email filtering before CRM sync
- deduplication before HubSpot upsert
- best-record selection from duplicate PMS records
- HubSpot contact payload mapping
- batch upsert fallback strategy
- recursive batch split retry
- bad-record isolation
- conflict handling
- scheduled sync structure
- structured logging

## What is included here

This public repository includes:

- sanitized sample data
- generic PMS field names
- fake HubSpot client with no network calls
- representative sync logic
- validation and deduplication patterns
- batch retry/split strategy
- conflict handling examples
- scheduled sync structure

## What is not included

This repository does not include:

- private client source code
- real customer data
- API keys or access tokens
- production logs
- client-specific business rules
- real property/listing names
- real company names
- production environment configuration

## Why this matters

Real PMS → CRM automations rarely fail because of the happy path.

They fail because of messy production data:

- invalid emails
- missing emails
- duplicate guests
- inconsistent reservation fields
- multiple reservations linked to one guest
- CRM conflicts
- batch API failures
- partial sync failures

This repository demonstrates the engineering patterns used to keep valid records moving while isolating bad data safely.

## Architecture

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

Guesty and Hostaway have different source data shapes, but both flow into the same shared integration core. This keeps platform-specific mapping separate from shared CRM sync logic.

## How to run

macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest
python -m src.sync.sync_runner
```

Windows:

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
pytest
python -m src.sync.sync_runner
```

## Confidentiality

This repository is intentionally anonymized.

It does not include:

- private client source code
- real customer data
- API keys or access tokens
- production logs
- client-specific business rules
- real property/listing names
- real company names
- production environment configuration

The goal is to demonstrate the engineering approach while respecting client confidentiality.



Need a similar integration? I build custom PMS/CRM/payment integrations. → ezenevic.com