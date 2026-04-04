# lark-doc-convert - 云文档导入导出

英文原版: [SKILL.md](SKILL.md)

本文是中文翻译版，供阅读参考。默认 skill 入口和规范内容以英文版 `SKILL.md` 为准；若两者有差异，请以英文版为准。

**前置条件：** 先安装官方 `larksuite/cli` skill 包，并阅读官方 `lark-shared` skill 中的认证和安全规则。

这个 skill 把原本分散在官方 `lark-doc` 和 `lark-drive` skill 里的导入导出流程整理成一个统一入口。

## 适用场景

- 把本地 Word、Excel、CSV、Markdown、HTML 文件导入到飞书。
- 把飞书文档、电子表格、多维表格导出成本地文件。
- 直接把飞书文档读取成 Markdown，或把 Markdown 直接创建为新文档。

## 快速决策

| 用户意图 | 命令 | 说明 |
|---------|------|------|
| 本地文件 -> 飞书文档 | `drive +import` | Word / Excel / CSV / Markdown / HTML -> docx / sheet / bitable |
| 飞书文档 -> 本地文件 | `drive +export` | 异步导出任务 |
| 飞书文档内容 -> Markdown 文本 | `docs +fetch` | 不走导出任务，直接返回 Markdown |
| Markdown 文本 -> 飞书文档 | `docs +create --markdown` | 不走导入任务，直接创建文档 |
| 下载云盘文件 | `drive +download` | 直接下载二进制内容 |

## 导入：本地文件 -> 飞书文档

### 支持格式

| 本地文件 | 目标类型 | 大小限制 |
|---------|---------|---------|
| `.docx`, `.doc` | `docx` | 600MB |
| `.txt`, `.md`, `.html` | `docx` | 20MB |
| `.xlsx` | `sheet` 或 `bitable` | 800MB |
| `.csv` | `sheet` 或 `bitable` | 20MB 到 100MB |
| `.xls` | `sheet` | 20MB |

### 命令

```bash
lark-cli drive +import --file ./README.md --type docx
lark-cli drive +import --file ./data.xlsx --type sheet
lark-cli drive +import --file ./data.csv --type bitable \
  --folder-token <FOLDER_TOKEN> --name "导入数据表"
```

### 超时处理

如果 `+import` 的轮询超时，但任务仍在运行：

```bash
lark-cli drive +task_result --scenario import --ticket <TICKET>
```

## 导出：飞书文档 -> 本地文件

### 支持格式

| 源文档类型 | 可导出格式 |
|-----------|-----------|
| `docx` | `pdf`, `docx`, `markdown` |
| `doc`（旧版） | `docx` |
| `sheet` | `xlsx`, `csv` |
| `bitable` | `xlsx`, `csv` |

> `markdown` 导出仅支持 `docx` 类型源文档。

### Step 1: 解析文档 token 和类型

可以从 URL 中提取：
- `/docx/doxcnXXX` -> token=`doxcnXXX`, doc-type=`docx`
- `/sheets/shtcnXXX` -> token=`shtcnXXX`, doc-type=`sheet`
- `/base/bascnXXX` -> token=`bascnXXX`, doc-type=`bitable`

Wiki 链接需要额外解析：

```bash
lark-cli wiki spaces get_node --params '{"token":"wikcnXXX"}'
```

### Step 2: 导出

```bash
lark-cli drive +export --token <TOKEN> --doc-type docx --file-extension pdf
lark-cli drive +export --token <TOKEN> --doc-type docx --file-extension markdown
lark-cli drive +export --token <TOKEN> --doc-type sheet --file-extension xlsx
lark-cli drive +export --token <TOKEN> --doc-type sheet --file-extension csv \
  --sub-id <SHEET_ID>
lark-cli drive +export --token <TOKEN> --doc-type docx --file-extension pdf \
  --output-dir ./exports --overwrite
```

### Step 3: 超时处理

如果 `+export` 超时但没有失败：

```bash
lark-cli drive +task_result --scenario export \
  --ticket <TICKET> --file-token <TOKEN>

lark-cli drive +export-download \
  --file-token <EXPORTED_FILE_TOKEN> --output-dir ./exports
```

## 快捷路径：Markdown 往返

如果只需要把文档读取成 Markdown：

```bash
lark-cli docs +fetch --doc <TOKEN_OR_URL>
```

如果已经有 Markdown 文本，想直接创建文档：

```bash
lark-cli docs +create --title "标题" --markdown "# Hello\n\nContent here"
```

## 权限

| 操作 | 所需 scope |
|------|-----------|
| 导入 | `drive:file:upload` |
| 导出 | `drive:file:download`, `docs:document:export` |
| 读取文档 | `docx:document:readonly` |
| 创建文档 | `docx:document:create` |
| 查询 Wiki 节点 | `wiki:node:read` |

## 参考

- 官方 `lark-drive` skill
- 官方 `lark-doc` skill
