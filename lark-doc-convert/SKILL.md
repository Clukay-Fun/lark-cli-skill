---
name: lark-doc-convert
version: 1.0.0
description: "Unified guide for importing local files into Lark docs and exporting Lark docs into local formats such as PDF, DOCX, XLSX, CSV, and Markdown."
metadata:
  requires:
    bins: ["lark-cli"]
---

# lark-doc-convert - Lark Document Import and Export

Chinese translation: [SKILL.zh-CN.md](SKILL.zh-CN.md)

**Prerequisites:** install the official `larksuite/cli` skill pack first, then review the authentication and safety rules in the official `lark-shared` skill.

This skill acts as a unified entry point for import and export flows that otherwise span the official `lark-doc` and `lark-drive` skills.

## Use Cases

- Import local Word, Excel, CSV, Markdown, or HTML files into Lark.
- Export Lark docs, sheets, and bitables into local files.
- Fetch a Lark doc as Markdown, or create a new Lark doc directly from Markdown.

## Quick Decision Table

| User intent | Command | Notes |
|-------------|---------|-------|
| Local file -> Lark doc | `drive +import` | Word / Excel / CSV / Markdown / HTML -> docx / sheet / bitable |
| Lark doc -> local PDF / DOCX / XLSX / CSV | `drive +export` | Asynchronous export task |
| Lark doc content -> Markdown text | `docs +fetch` | Returns Markdown directly without export workflow |
| Markdown text -> Lark doc | `docs +create --markdown` | Creates the doc directly without import workflow |
| Download a Drive file | `drive +download` | Downloads binary content directly |

## Import: Local File -> Lark Doc

### Supported Formats

| Local file | Target type | Size limit |
|------------|-------------|------------|
| `.docx`, `.doc` | `docx` | 600MB |
| `.txt`, `.md`, `.html` | `docx` | 20MB |
| `.xlsx` | `sheet` or `bitable` | 800MB |
| `.csv` | `sheet` or `bitable` | 20MB to 100MB |
| `.xls` | `sheet` | 20MB |

### Commands

```bash
lark-cli drive +import --file ./README.md --type docx
lark-cli drive +import --file ./data.xlsx --type sheet
lark-cli drive +import --file ./data.csv --type bitable \
  --folder-token <FOLDER_TOKEN> --name "Imported Data Table"
```

### Timeout Handling

If `+import` times out while the task is still running:

```bash
lark-cli drive +task_result --scenario import --ticket <TICKET>
```

## Export: Lark Doc -> Local File

### Supported Formats

| Source type | Export formats |
|-------------|----------------|
| `docx` | `pdf`, `docx`, `markdown` |
| `doc` (legacy) | `docx` |
| `sheet` | `xlsx`, `csv` |
| `bitable` | `xlsx`, `csv` |

> `markdown` export is supported only for `docx` source documents.

### Step 1: Resolve the Doc Token and Type

Extract them from the URL:
- `/docx/doxcnXXX` -> token=`doxcnXXX`, doc-type=`docx`
- `/sheets/shtcnXXX` -> token=`shtcnXXX`, doc-type=`sheet`
- `/base/bascnXXX` -> token=`bascnXXX`, doc-type=`bitable`

Wiki links require an additional lookup:

```bash
lark-cli wiki spaces get_node --params '{"token":"wikcnXXX"}'
```

### Step 2: Export

```bash
lark-cli drive +export --token <TOKEN> --doc-type docx --file-extension pdf
lark-cli drive +export --token <TOKEN> --doc-type docx --file-extension markdown
lark-cli drive +export --token <TOKEN> --doc-type sheet --file-extension xlsx
lark-cli drive +export --token <TOKEN> --doc-type sheet --file-extension csv \
  --sub-id <SHEET_ID>
lark-cli drive +export --token <TOKEN> --doc-type docx --file-extension pdf \
  --output-dir ./exports --overwrite
```

### Step 3: Timeout Handling

If `+export` times out without failing:

```bash
lark-cli drive +task_result --scenario export \
  --ticket <TICKET> --file-token <TOKEN>

lark-cli drive +export-download \
  --file-token <EXPORTED_FILE_TOKEN> --output-dir ./exports
```

## Fast Path: Markdown Round Trips

If you only need the document content as Markdown:

```bash
lark-cli docs +fetch --doc <TOKEN_OR_URL>
```

If you already have Markdown text and want to create a doc directly:

```bash
lark-cli docs +create --title "Title" --markdown "# Hello\n\nContent here"
```

## Permissions

| Operation | Required scope |
|-----------|----------------|
| Import | `drive:file:upload` |
| Export | `drive:file:download`, `docs:document:export` |
| Read doc content | `docx:document:readonly` |
| Create docs | `docx:document:create` |
| Resolve wiki nodes | `wiki:node:read` |

## References

- Official `lark-drive` skill
- Official `lark-doc` skill
