# 单元格样式

英文原版: [style.md](style.md)

## API

- `PUT /open-apis/sheets/v2/spreadsheets/{token}/style`
- `PUT /open-apis/sheets/v2/spreadsheets/{token}/style_batch_update`

## 脚本用法

```bash
python scripts/sheets_style.py <token> <sheet_id> A1:E1 --bold --h-align CENTER
python scripts/sheets_style.py <token> <sheet_id> A1:D10 --border all --border-color "#000000"
```
