# lark-base-batch - 多维表格批量记录操作

英文原版: [SKILL.md](SKILL.md)

本文是中文翻译版，供阅读参考。默认 skill 入口和规范内容以英文版 `SKILL.md` 为准；若两者有差异，请以英文版为准。

**前置条件：** 先安装官方 `larksuite/cli` skill 包，并阅读官方 `lark-shared` skill 中的认证和安全规则。如果当前环境还没有 `lark-cli`，优先使用本仓库的 `lark-setup` skill 完成安装或刷新。

这个 skill 补充了官方 `lark-base` skill 未暴露的批量记录 API。
单条记录操作仍建议使用 `lark-base` 的 `+record-upsert` 和 `+record-delete`。
当一次要处理多条记录时，优先使用本 skill。

## 适用场景

- 一次性导入多条记录到多维表格。
- 按 `record_id` 批量更新多条记录。
- 在用户确认后批量删除多条记录。

## 能力概览

| 操作 | API | 单次上限 | 说明 |
|------|-----|---------|------|
| 批量创建 | `POST .../records/batch_create` | 500 条 | 一次创建多条记录 |
| 批量更新 | `POST .../records/batch_update` | 500 条 | 按 `record_id` 更新多条 |
| 批量删除 | `POST .../records/batch_delete` | 500 条 | 按 `record_id` 删除多条 |

所有接口都基于 `/open-apis/bitable/v1/apps/{app_token}/tables/{table_id}`。

## 记录值格式

记录值格式与 `+record-upsert` 一致。
写入前建议先用官方 `lark-base` skill 的 `base +field-list` 查看字段类型，再按类型组织值。

常见值形状：
- 文本：`"标题内容"`
- 数字：`12.5`
- 单选：`"Todo"`
- 多选：`["A", "B"]`
- 人员：`[{"id":"ou_xxx"}]`
- 日期时间：`"2026-03-24 10:00:00"`

## 命令示例

`scripts/base_batch.py` 封装了三种批量操作，并会自动把超过 500 条的输入拆分成多次请求。

### 批量创建

```bash
python scripts/base_batch.py create <app_token> <table_id> \
  --json '[{"姓名":"张三","部门":"工程"},{"姓名":"李四","部门":"产品"}]'

python scripts/base_batch.py create <app_token> <table_id> --file records.json
```

参见 [references/batch-create.zh-CN.md](references/batch-create.zh-CN.md)。

### 批量更新

```bash
python scripts/base_batch.py update <app_token> <table_id> \
  --json '[{"record_id":"rec_xxx","fields":{"状态":"完成"}},{"record_id":"rec_yyy","fields":{"状态":"完成"}}]'
```

参见 [references/batch-update.zh-CN.md](references/batch-update.zh-CN.md)。

### 批量删除

```bash
python scripts/base_batch.py delete <app_token> <table_id> \
  --json '["rec_xxx","rec_yyy","rec_zzz"]'
```

参见 [references/batch-delete.zh-CN.md](references/batch-delete.zh-CN.md)。

所有子命令都支持 `--as user|bot`、`--format json|pretty|...` 和 `--dry-run`。

## 直接使用 `lark-cli api`

不用脚本时，也可以直接调用原始 API：

```bash
lark-cli api POST /open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/records/batch_create \
  --data '{"records":[{"fields":{"姓名":"张三","部门":"工程"}},{"fields":{"姓名":"李四","部门":"产品"}}]}'

lark-cli api POST /open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/records/batch_update \
  --data '{"records":[{"record_id":"rec_xxx","fields":{"状态":"完成"}}]}'

lark-cli api POST /open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/records/batch_delete \
  --data '{"records":["rec_xxx","rec_yyy"]}'
```

## 安全规则

- 批量创建和批量更新：确认用户意图后再执行。
- 批量删除：必须先展示将删除的 `record_id` 列表，并在执行前获得用户明确确认。建议先用 `--dry-run` 预览。
- 超过 500 条时，脚本会自动分片，并在片段之间等待 200ms 以降低限流风险。

## 权限

| 操作 | 所需 scope |
|------|-----------|
| batch_create | `base:record:create` |
| batch_update | `base:record:update` |
| batch_delete | `base:record:delete` |

## 参考

- [批量创建记录](references/batch-create.zh-CN.md)
- [批量更新记录](references/batch-update.zh-CN.md)
- [批量删除记录](references/batch-delete.zh-CN.md)
- 官方 `lark-base` skill
