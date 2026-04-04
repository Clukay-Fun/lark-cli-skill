---
name: lark-base-batch
version: 1.0.0
description: "Batch record operations for Lark Bitable: batch create, batch update, and batch delete. Use this skill when many records must be imported, updated, or deleted at once."
metadata:
  requires:
    bins: ["lark-cli"]
---

# lark-base-batch - Batch Bitable Record Operations

Chinese translation: [SKILL.zh-CN.md](SKILL.zh-CN.md)

**Prerequisites:** install the official `larksuite/cli` skill pack first, then review the authentication and safety rules in the official `lark-shared` skill.

This skill covers batch record APIs not exposed by the official `lark-base` skill.
For single-record operations, continue using `+record-upsert` and `+record-delete` from `lark-base`.
Prefer this skill whenever more than one record is being changed.

## Use Cases

- Import many records into a bitable in one run.
- Update many records by `record_id`.
- Delete many records after explicit confirmation.

## Capability Summary

| Operation | API | Per-request limit | Notes |
|-----------|-----|-------------------|-------|
| Batch create | `POST .../records/batch_create` | 500 records | Create many records at once |
| Batch update | `POST .../records/batch_update` | 500 records | Update many records by `record_id` |
| Batch delete | `POST .../records/batch_delete` | 500 records | Delete many records by `record_id` |

All endpoints share the base path `/open-apis/bitable/v1/apps/{app_token}/tables/{table_id}`.

## Record Value Format

Values follow the same format as `+record-upsert`.
Before writing records, use `base +field-list` from the official `lark-base` skill to inspect field types and shape the values correctly.

Common shapes:
- Text: `"Title text"`
- Number: `12.5`
- Single select: `"Todo"`
- Multi select: `["A", "B"]`
- User: `[{"id":"ou_xxx"}]`
- Date/time: `"2026-03-24 10:00:00"`

## Command Examples

`scripts/base_batch.py` wraps all three operations and automatically chunks input larger than 500 records.

### Batch Create

```bash
# Inline JSON array
python scripts/base_batch.py create <app_token> <table_id> \
  --json '[{"Name":"Alice","Department":"Engineering"},{"Name":"Bob","Department":"Product"}]'

# Read from a file
python scripts/base_batch.py create <app_token> <table_id> --file records.json
```

See [references/batch-create.md](references/batch-create.md).

### Batch Update

```bash
python scripts/base_batch.py update <app_token> <table_id> \
  --json '[{"record_id":"rec_xxx","fields":{"Status":"Done"}},{"record_id":"rec_yyy","fields":{"Status":"Done"}}]'
```

See [references/batch-update.md](references/batch-update.md).

### Batch Delete

```bash
python scripts/base_batch.py delete <app_token> <table_id> \
  --json '["rec_xxx","rec_yyy","rec_zzz"]'
```

See [references/batch-delete.md](references/batch-delete.md).

All subcommands support `--as user|bot`, `--format json|pretty|...`, and `--dry-run`.

## Direct `lark-cli api` Usage

You can also call the raw API directly:

```bash
# Batch create
lark-cli api POST /open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/records/batch_create \
  --data '{"records":[{"fields":{"Name":"Alice","Department":"Engineering"}},{"fields":{"Name":"Bob","Department":"Product"}}]}'

# Batch update
lark-cli api POST /open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/records/batch_update \
  --data '{"records":[{"record_id":"rec_xxx","fields":{"Status":"Done"}}]}'

# Batch delete
lark-cli api POST /open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/records/batch_delete \
  --data '{"records":["rec_xxx","rec_yyy"]}'
```

## Safety Rules

- **Batch create / update:** execute only after the user intent is clear.
- **Batch delete:** always show the list of `record_id`s to be deleted and require explicit confirmation before execution. Prefer a `--dry-run` preview first.
- The helper script automatically chunks requests larger than 500 records and waits 200ms between chunks to reduce rate-limit risk.

## Permissions

| Operation | Required scope |
|-----------|----------------|
| batch_create | `base:record:create` |
| batch_update | `base:record:update` |
| batch_delete | `base:record:delete` |

## References

- [Batch create records](references/batch-create.md)
- [Batch update records](references/batch-update.md)
- [Batch delete records](references/batch-delete.md)
- Official `lark-base` skill
