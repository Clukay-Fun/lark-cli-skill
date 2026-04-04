# Batch Create Records

Chinese translation: [batch-create.zh-CN.md](batch-create.zh-CN.md)

## API

```text
POST /open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/records/batch_create
```

## Request Body

```json
{
  "records": [
    { "fields": { "Name": "Alice", "Department": "Engineering", "Start Date": "2026-01-15 09:00:00" } },
    { "fields": { "Name": "Bob", "Department": "Product", "Start Date": "2026-02-01 09:00:00" } }
  ]
}
```

| Field | Required | Notes |
|------|----------|-------|
| records | Yes | Array of records |
| records[].fields | Yes | Field name or field ID -> value mapping |

The per-request limit is 500 records.

## Response Example

```json
{
  "data": {
    "records": [
      { "record_id": "rec_xxx", "fields": { "Name": "Alice" } },
      { "record_id": "rec_yyy", "fields": { "Name": "Bob" } }
    ]
  }
}
```

## Script Usage

```bash
python scripts/base_batch.py create <app_token> <table_id> \
  --json '[{"Name":"Alice","Department":"Engineering"},{"Name":"Bob","Department":"Product"}]'

python scripts/base_batch.py create <app_token> <table_id> --file data.json

python scripts/base_batch.py create <app_token> <table_id> \
  --json '[{"Name":"Alice"}]' --dry-run
```

The script accepts the short form above and wraps each item into `{"fields": {...}}`.
