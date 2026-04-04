# 批量创建记录

英文原版: [batch-create.md](batch-create.md)

## API

```text
POST /open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/records/batch_create
```

## 请求体

```json
{
  "records": [
    { "fields": { "姓名": "张三", "部门": "工程", "入职日期": "2026-01-15 09:00:00" } },
    { "fields": { "姓名": "李四", "部门": "产品", "入职日期": "2026-02-01 09:00:00" } }
  ]
}
```

## 返回示例

```json
{
  "data": {
    "records": [
      { "record_id": "rec_xxx", "fields": { "姓名": "张三" } },
      { "record_id": "rec_yyy", "fields": { "姓名": "李四" } }
    ]
  }
}
```

## 脚本用法

```bash
python scripts/base_batch.py create <app_token> <table_id> \
  --json '[{"姓名":"张三","部门":"工程"},{"姓名":"李四","部门":"产品"}]'

python scripts/base_batch.py create <app_token> <table_id> --file data.json
```
