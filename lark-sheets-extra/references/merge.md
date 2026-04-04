# Merge and Unmerge Cells

Chinese translation: [merge.zh-CN.md](merge.zh-CN.md)

## API

- `POST /open-apis/sheets/v2/spreadsheets/{token}/merge_cells`
- `POST /open-apis/sheets/v2/spreadsheets/{token}/unmerge_cells`

## Script Usage

```bash
python scripts/sheets_merge.py merge <token> <sheet_id> A1:C1
python scripts/sheets_merge.py unmerge <token> <sheet_id> A1:C1
```
