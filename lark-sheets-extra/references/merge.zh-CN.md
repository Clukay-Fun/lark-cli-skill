# 合并 / 取消合并单元格

英文原版: [merge.md](merge.md)

## API

- `POST /open-apis/sheets/v2/spreadsheets/{token}/merge_cells`
- `POST /open-apis/sheets/v2/spreadsheets/{token}/unmerge_cells`

## 脚本用法

```bash
python scripts/sheets_merge.py merge <token> <sheet_id> A1:C1
python scripts/sheets_merge.py unmerge <token> <sheet_id> A1:C1
```
