# 批量更新记录

英文原版: [batch-update.md](batch-update.md)

## API

```text
POST /open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/records/batch_update
```

## 请求体

```json
{
  "records": [
    { "record_id": "rec_xxx", "fields": { "状态": "完成", "完成时间": "2026-03-20 18:00:00" } },
    { "record_id": "rec_yyy", "fields": { "状态": "进行中" } }
  ]
}
```

## 返回示例

```json
{
  "data": {
    "records": [
      { "record_id": "rec_xxx", "fields": { "状态": "完成" } },
      { "record_id": "rec_yyy", "fields": { "状态": "进行中" } }
    ]
  }
}
```

## 脚本用法

```bash
python scripts/base_batch.py update <app_token> <table_id> \
  --json '[{"record_id":"rec_xxx","fields":{"状态":"完成"}},{"record_id":"rec_yyy","fields":{"状态":"完成"}}]'
```
