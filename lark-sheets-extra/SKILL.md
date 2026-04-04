---
name: lark-sheets-extra
version: 1.0.0
description: "Extra helpers for Lark Sheets v2 APIs such as merge cells, styling, and row or column operations that are not covered by the official `lark-sheets` skill."
metadata:
  requires:
    bins: ["lark-cli"]
  cliHelp: "lark-cli sheets --help"
---

# lark-sheets-extra - Lark Sheets Extensions

Chinese translation: [SKILL.zh-CN.md](SKILL.zh-CN.md)

**Prerequisites:** install the official `larksuite/cli` skill pack first, then review the authentication, identity switching, and safety rules in the official `lark-shared` skill. If `lark-cli` is unavailable, use the local `lark-setup` skill to install or refresh the environment first.

This skill covers v2 sheet APIs not exposed by the official `lark-sheets` skill, mainly formatting and structure operations.
Keep using the official `lark-sheets` skill for built-in commands such as `+read`, `+write`, `+append`, `+find`, `+create`, `+info`, and `+export`.

## Use Cases

- Merge or unmerge cells.
- Set styles such as font weight, background color, alignment, and borders.
- Insert or delete rows and columns.

## Capability Summary

| Operation | API path | Notes |
|-----------|----------|-------|
| Merge cells | `POST .../merge_cells` | Merge a target range |
| Unmerge cells | `POST .../unmerge_cells` | Remove a merge from a range |
| Set style | `PUT .../style` | Bold, font size, color, border, alignment |
| Batch style update | `PUT .../style_batch_update` | Apply different styles to multiple ranges |
| Insert rows/columns | `POST .../insert_dimension_range` | Insert rows or columns at a position |
| Delete rows/columns | `DELETE .../dimension_range` | Delete a row or column range |
| Protected range | `POST .../protection` | Lock ranges or restrict edits |

All endpoints share the base path `/open-apis/sheets/v2/spreadsheets/{spreadsheet_token}`.

## Command Examples

The `scripts/` directory contains Python wrappers for common operations. They require only Python 3 and `lark-cli`.
All scripts support `--as user|bot`, `--format json|pretty|...`, and `--dry-run`.

### Merge and Unmerge

```bash
python scripts/sheets_merge.py merge <token> <sheet_id> A1:C1 --merge-type MERGE_ALL
python scripts/sheets_merge.py unmerge <token> <sheet_id> A1:C1
python scripts/sheets_merge.py test --title "Demo"
```

See [references/merge.md](references/merge.md).

### Cell Styling

```bash
python scripts/sheets_style.py <token> <sheet_id> A1:E1 --bold --bg-color "#4A90D9" --h-align CENTER
python scripts/sheets_style.py <token> <sheet_id> A1:D10 --border all --border-color "#000000"
```

See [references/style.md](references/style.md).

### Insert and Delete Rows or Columns

```bash
python scripts/sheets_dimension.py insert <token> <sheet_id> --major-dimension ROWS --start 2 --end 5
python scripts/sheets_dimension.py delete <token> <sheet_id> --major-dimension COLUMNS --start 3 --end 4
```

See [references/dimension.md](references/dimension.md).

## Direct `lark-cli api` Usage

If you do not want to use the helper scripts, call the raw API directly.

```bash
lark-cli api POST /open-apis/sheets/v2/spreadsheets/{token}/merge_cells \
  --data '{"range":"<sheet_id>!A1:C1","mergeType":"MERGE_ALL"}'

lark-cli api PUT /open-apis/sheets/v2/spreadsheets/{token}/style \
  --data '{"appendStyle":{"range":"<sheet_id>!A1:E1","style":{"font":{"bold":true}}}}'

lark-cli api POST /open-apis/sheets/v2/spreadsheets/{token}/insert_dimension_range \
  --data '{"dimension":{"sheetId":"<sheet_id>","majorDimension":"ROWS","startIndex":2,"endIndex":5}}'
```

## Range Format

All v2 APIs use the range format `<sheet_id>!<cell_range>`, for example `abc123!A1:C3`.

You can obtain `sheet_id` with `lark-cli sheets +info --spreadsheet-token <token>` or `lark-cli sheets +info --url <url>`.

## Permissions

| Operation | Required scope |
|-----------|----------------|
| merge / unmerge / style / dimension | `sheets:spreadsheet:write_only` |
| Read spreadsheet info | `sheets:spreadsheet:read` |

## References

- [Merge and unmerge cells](references/merge.md)
- [Cell styling](references/style.md)
- [Insert and delete rows or columns](references/dimension.md)
- Official `lark-sheets` skill
