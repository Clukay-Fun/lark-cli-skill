# Cell Styling

Chinese translation: [style.zh-CN.md](style.zh-CN.md)

## API

- `PUT /open-apis/sheets/v2/spreadsheets/{token}/style`
- `PUT /open-apis/sheets/v2/spreadsheets/{token}/style_batch_update`

## Script Usage

```bash
python scripts/sheets_style.py <token> <sheet_id> A1:E1 --bold --h-align CENTER
python scripts/sheets_style.py <token> <sheet_id> A1:D10 --border all --border-color "#000000"
```
