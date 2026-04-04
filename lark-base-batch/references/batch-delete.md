# Batch Delete Records

Chinese translation: [batch-delete.zh-CN.md](batch-delete.zh-CN.md)

## API

```text
POST /open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/records/batch_delete
```

## Request Body

```json
{
  "records": ["rec_xxx", "rec_yyy", "rec_zzz"]
}
```

## Response Example

```json
{
  "data": {
    "records": [
      { "id": "rec_xxx", "deleted": true },
      { "id": "rec_yyy", "deleted": true }
    ]
  }
}
```

## Script Usage

```bash
python scripts/base_batch.py delete <app_token> <table_id> \
  --json '["rec_xxx","rec_yyy","rec_zzz"]'
```

## Safety Reminder

Batch delete is irreversible. Show the `record_id` list first and require explicit confirmation.
