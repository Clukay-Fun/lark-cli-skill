# Batch Update Records

Chinese translation: [batch-update.zh-CN.md](batch-update.zh-CN.md)

## API

```text
POST /open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/records/batch_update
```

## Request Body

```json
{
  "records": [
    { "record_id": "rec_xxx", "fields": { "Status": "Done", "Completed At": "2026-03-20 18:00:00" } },
    { "record_id": "rec_yyy", "fields": { "Status": "In Progress" } }
  ]
}
```

## Response Example

```json
{
  "data": {
    "records": [
      { "record_id": "rec_xxx", "fields": { "Status": "Done" } },
      { "record_id": "rec_yyy", "fields": { "Status": "In Progress" } }
    ]
  }
}
```

## Script Usage

```bash
python scripts/base_batch.py update <app_token> <table_id> \
  --json '[{"record_id":"rec_xxx","fields":{"Status":"Done"}},{"record_id":"rec_yyy","fields":{"Status":"Done"}}]'
```
