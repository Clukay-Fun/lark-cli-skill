# lark-cli 扩展 Skill 集

补充官方 `larksuite/cli` skill 未覆盖的功能。

English original: [README.md](README.md)

## 语言说明

- `README.md`、各目录下的 `SKILL.md` 以及默认的 `references/*.md` 都是规范英文原版。
- 工具和 skill 入口默认应读取英文文件，尤其是 `SKILL.md`。
- 对应的 `*.zh-CN.md` 是给中文读者使用的翻译版。
- 如果中英文内容暂时不一致，以英文版为准，中文版随后同步。

## Skills

| Skill | 类型 | 说明 |
|-------|------|------|
| `lark-setup` | 环境管理 | 安装、更新、校验并检查 Lark CLI 环境与 skill 包状态 |
| `lark-sheets-extra` | 领域扩展 | 电子表格 v2 API：合并单元格、样式、行列操作 |
| `lark-base-batch` | 领域扩展 | 多维表格批量记录：`batch_create` / `batch_update` / `batch_delete` |
| `lark-im-card` | 领域扩展 | 消息卡片构建指南：JSON 结构和可复用模板 |
| `lark-workflow-meeting` | 工作流 | 创建会议并通知参会人：忙闲查询 -> 建会 -> 发通知 |
| `lark-doc-convert` | 工作流 | 云文档导入导出：本地文件与飞书文档之间的统一入口 |

## 安装

在与你的 AI CLI 代理对话时，可以直接说：

```text
帮我安装 lark-cli 和这些扩展 skill。
```

推荐把 `lark-setup` 作为统一入口。它会检测当前 CLI 环境，安装或更新 `lark-cli`，安装官方 `larksuite/cli` skill 包，并把当前仓库的扩展 skill 复制到正确的 skill 目录。

## `lark-setup` 示例对话

### 首次安装

用户：

```text
帮我安装 lark-cli 和这些扩展 skill。
```

Agent 行为：

- 检查 `node`、`npm` 和 `lark-cli`
- 如果缺失则安装 `lark-cli`
- 安装官方 `larksuite/cli` skill 包
- 检测当前 AI CLI 环境
- 把 `lark-setup` 和扩展 skill 复制到识别出的 skill 目录
- 检查 `lark-cli auth status`

### 更新现有环境

用户：

```text
帮我更新 Lark CLI 环境。
```

Agent 行为：

- 执行 `npm update -g @anthropic-ai/lark-cli`
- 刷新官方 `larksuite/cli` skill 包
- 重新复制扩展 skill 到检测出的 skill 目录
- 校验版本和 skill 是否存在

### 仅检查状态

用户：

```text
看看 lark-cli 有没有装好，认证好了没有。
```

Agent 行为：

- 检查 `lark-cli` 是否在 `PATH` 中
- 报告当前安装版本
- 执行 `lark-cli auth status`
- 告知用户是否还需要继续登录

### 认证补全

用户：

```text
把 Lark CLI 的认证也处理一下。
```

Agent 行为：

- 执行 `lark-cli auth status`
- 如果尚未登录，提示用户运行 `!lark-cli auth login`
- 等用户完成交互步骤后，再次检查认证状态

如果需要，也可以手动安装：

```bash
npx skills add larksuite/cli -g -y
cp -r lark-setup/ ~/.claude/skills/lark-setup/
cp -r lark-sheets-extra/ ~/.claude/skills/lark-sheets-extra/
cp -r lark-base-batch/ ~/.claude/skills/lark-base-batch/
cp -r lark-im-card/ ~/.claude/skills/lark-im-card/
cp -r lark-workflow-meeting/ ~/.claude/skills/lark-workflow-meeting/
cp -r lark-doc-convert/ ~/.claude/skills/lark-doc-convert/
```

不同 CLI 环境的手动目标目录不同：

- Claude Code：`~/.claude/skills/`
- Codex：`$CODEX_HOME/skills/`
- OpenCode：`~/.config/opencode/skills/`
- Gemini CLI：`~/.gemini/skills/`

对 Codex，只在 `$CODEX_HOME` 已定义时使用 `$CODEX_HOME/skills/`。如果该变量不存在，应先确认目标目录，不要直接猜测。

这些扩展 skill 依赖官方 `larksuite/cli` skill 包提供的基础能力。当前仓库只包含补充说明和辅助脚本，不包含 `lark-shared`、`lark-base`、`lark-im`、`lark-calendar`、`lark-drive` 等官方 skill 的内容。

## 依赖

- `PATH` 中可用的 `lark-cli`
- `scripts/` 下脚本所需的 Python 3
- 负责认证和安全规则的官方 `lark-shared` skill
- 每个扩展 skill 所依赖的官方领域 skill，例如 `lark-base`、`lark-im`、`lark-calendar`

## 文档约定

- 每个 `SKILL.md` 大体按“前置条件 -> 适用场景/能力概览 -> 命令示例或工作流 -> 权限 -> 参考”的顺序组织。
- 命令示例统一使用 `bash` 代码块，占位参数使用 `<TOKEN>`、`<ID>`、`<URL>` 等形式。
- 对官方外部 skill 的引用统一写成纯文本说明，避免仓库内断链。
- 中文翻译文件统一与英文原版放在同目录，并使用 `.zh-CN.md` 后缀，避免影响默认入口文件名。
