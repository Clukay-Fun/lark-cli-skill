# lark-sheets-extra - 飞书电子表格扩展

英文原版: [SKILL.md](SKILL.md)

本文是中文翻译版，供阅读参考。默认 skill 入口和规范内容以英文版 `SKILL.md` 为准；若两者有差异，请以英文版为准。

**前置条件：** 先安装官方 `larksuite/cli` skill 包，并阅读官方 `lark-shared` skill 中的认证、身份切换和安全规则。

这个 skill 用来补齐官方 `lark-sheets` skill 没有直接暴露的 v2 API，重点是格式和结构操作。
像 `+read`、`+write`、`+append`、`+find`、`+create`、`+info`、`+export` 这些已有能力，仍然应使用官方 `lark-sheets` skill。

## 适用场景

- 合并或取消合并单元格。
- 设置单元格样式，例如字体、背景色、对齐和边框。
- 插入或删除行列。

## 能力概览

| 操作 | API 路径 | 说明 |
|------|---------|------|
| 合并单元格 | `POST .../merge_cells` | 合并指定区域 |
| 取消合并 | `POST .../unmerge_cells` | 取消合并 |
| 设置样式 | `PUT .../style` | 加粗、字号、颜色、边框、对齐 |
| 批量样式 | `PUT .../style_batch_update` | 对多个区域分别设置样式 |
| 插入行列 | `POST .../insert_dimension_range` | 在指定位置插入行或列 |
| 删除行列 | `DELETE .../dimension_range` | 删除指定范围的行或列 |
| 保护区域 | `POST .../protection` | 锁定区域或限制编辑 |

所有接口都基于 `/open-apis/sheets/v2/spreadsheets/{spreadsheet_token}`。

## 命令示例

`scripts/` 目录里的 Python 脚本封装了常见操作，只依赖 Python 3 和 `lark-cli`。
所有脚本都支持 `--as user|bot`、`--format json|pretty|...` 和 `--dry-run`。

### 合并 / 取消合并

```bash
python scripts/sheets_merge.py merge <token> <sheet_id> A1:C1 --merge-type MERGE_ALL
python scripts/sheets_merge.py unmerge <token> <sheet_id> A1:C1
python scripts/sheets_merge.py test --title "Demo"
```

参见 [references/merge.zh-CN.md](references/merge.zh-CN.md)。

### 单元格样式

```bash
python scripts/sheets_style.py <token> <sheet_id> A1:E1 --bold --bg-color "#4A90D9" --h-align CENTER
python scripts/sheets_style.py <token> <sheet_id> A1:D10 --border all --border-color "#000000"
```

参见 [references/style.zh-CN.md](references/style.zh-CN.md)。

### 插入 / 删除行列

```bash
python scripts/sheets_dimension.py insert <token> <sheet_id> --major-dimension ROWS --start 2 --end 5
python scripts/sheets_dimension.py delete <token> <sheet_id> --major-dimension COLUMNS --start 3 --end 4
```

参见 [references/dimension.zh-CN.md](references/dimension.zh-CN.md)。

## 直接使用 `lark-cli api`

如果不使用脚本，也可以直接调用原始 API。

## Range 格式

所有 v2 API 的 range 格式都是 `<sheet_id>!<cell_range>`，例如 `abc123!A1:C3`。

## 权限

| 操作 | 所需 scope |
|------|-----------|
| merge / unmerge / style / dimension | `sheets:spreadsheet:write_only` |
| 读取表格信息 | `sheets:spreadsheet:read` |

## 参考

- [合并 / 取消合并单元格](references/merge.zh-CN.md)
- [单元格样式](references/style.zh-CN.md)
- [插入 / 删除行列](references/dimension.zh-CN.md)
- 官方 `lark-sheets` skill
