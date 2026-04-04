# Insert and Delete Rows or Columns

Chinese translation: [dimension.zh-CN.md](dimension.zh-CN.md)

## API

- `POST /open-apis/sheets/v2/spreadsheets/{token}/insert_dimension_range`
- `DELETE /open-apis/sheets/v2/spreadsheets/{token}/dimension_range`

## Script Usage

```bash
python scripts/sheets_dimension.py insert <token> <sheet_id> --major-dimension ROWS --start 2 --end 5
python scripts/sheets_dimension.py delete <token> <sheet_id> --major-dimension COLUMNS --start 3 --end 5
```
