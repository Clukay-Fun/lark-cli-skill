# 批量删除记录

英文原版: [batch-delete.md](batch-delete.md)

## API

```text
POST /open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/records/batch_delete
```

## 请求体

```json
{
  "records": ["rec_xxx", "rec_yyy", "rec_zzz"]
}
```

## 返回示例

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

## 脚本用法

```bash
python scripts/base_batch.py delete <app_token> <table_id> \
  --json '["rec_xxx","rec_yyy","rec_zzz"]'
```
