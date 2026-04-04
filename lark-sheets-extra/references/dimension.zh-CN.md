# 插入 / 删除行列

英文原版: [dimension.md](dimension.md)

## API

- `POST /open-apis/sheets/v2/spreadsheets/{token}/insert_dimension_range`
- `DELETE /open-apis/sheets/v2/spreadsheets/{token}/dimension_range`

## 脚本用法

```bash
python scripts/sheets_dimension.py insert <token> <sheet_id> --major-dimension ROWS --start 2 --end 5
python scripts/sheets_dimension.py delete <token> <sheet_id> --major-dimension COLUMNS --start 3 --end 5
```
