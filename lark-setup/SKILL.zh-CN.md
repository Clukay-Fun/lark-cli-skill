# lark-setup - 安装与维护 Lark CLI 环境

英文原版: [SKILL.md](SKILL.md)

本文是中文翻译版，供阅读参考。默认 skill 入口和规范内容以英文版 `SKILL.md` 为准；若两者有差异，请以英文版为准。

这是当前仓库的环境入口 skill。
当用户希望安装 `lark-cli`、升级 `lark-cli`、安装官方 `larksuite/cli` skill 包，或把本仓库扩展 skill 复制到当前 AI CLI 环境时，都应优先使用它。

## 适用场景

- 首次安装，例如“帮我安装 lark-cli”或“把飞书 CLI 环境配好”。
- 安装官方 `larksuite/cli` skill 包。
- 安装或刷新当前仓库提供的扩展 skill。
- 检查 `lark-cli` 是否已经安装、是否在 `PATH` 中、是否已认证。
- 更新 `lark-cli` 或重新安装 skill 包。

## 环境检测

按以下顺序检测当前 CLI 环境：

| 优先级 | 检测方式 | 环境 | Skill 目录 |
|--------|----------|------|------------|
| 1 | `CLAUDE_CODE=1` | Claude Code | `~/.claude/skills/` |
| 2 | 存在 `CODEX_THREAD_ID` | Codex | `$CODEX_HOME/skills/` |
| 3 | 存在 `~/.config/opencode/opencode.json` | OpenCode | `~/.config/opencode/skills/` |
| 4 | 存在 `~/.gemini/settings.json` | Gemini CLI | `~/.gemini/skills/` |
| 5 | 都不匹配 | 未知环境 | 让用户手动提供目标目录 |

如果多个检测条件同时命中，按表中的优先级取第一个结果。
对 Codex，仅在 `$CODEX_HOME` 已定义时优先使用 `$CODEX_HOME/skills/`。如果该变量不存在，应让用户确认 Codex 的 skill 目录。不要默认写入项目内的 `.codex/skills/`，除非用户明确要求这样做。

## 安装流程

按顺序执行以下检查；已满足的步骤自动跳过。

### Step 1：检查前置依赖

```bash
node --version
npm --version
```

- 要求 Node.js 16 及以上版本。
- 如果 Node.js 不存在或版本过低，停止执行，并提示用户先安装或升级 Node.js。

### Step 2：检查或安装 `lark-cli`

```bash
which lark-cli
lark-cli --version
```

如果 `lark-cli` 不存在：

```bash
npm install -g @anthropic-ai/lark-cli
lark-cli --version
```

不要自动加 `sudo`。如果全局安装因权限失败，应解释原因，并引导用户查看排障文档。

### Step 3：安装或刷新官方 Skill 包

```bash
npx skills add larksuite/cli -g -y
```

### Step 4：安装或刷新本仓库扩展 Skill

当前仓库的扩展 skill 都是本地目录。最稳妥的默认假设是：`lark-setup` 在仓库根目录中运行。

如目标目录不存在，先创建；然后复制这些目录：

```bash
mkdir -p <SKILLS_DIR>
cp -R lark-setup/ <SKILLS_DIR>/lark-setup/
cp -R lark-sheets-extra/ <SKILLS_DIR>/lark-sheets-extra/
cp -R lark-base-batch/ <SKILLS_DIR>/lark-base-batch/
cp -R lark-im-card/ <SKILLS_DIR>/lark-im-card/
cp -R lark-workflow-meeting/ <SKILLS_DIR>/lark-workflow-meeting/
cp -R lark-doc-convert/ <SKILLS_DIR>/lark-doc-convert/
```

如果当前工作目录下找不到这些仓库目录，应停止，并要求用户从仓库根目录运行，或提供本地 checkout 路径。除非用户明确要求，否则不要静默地自行克隆或下载另一份仓库。

### Step 5：验证

```bash
lark-cli --version
ls <SKILLS_DIR>
```

确认目标 skill 已存在，并向用户报告最终安装目录。

## 更新流程

当用户要求更新环境时，执行：

```bash
npm update -g @anthropic-ai/lark-cli
npx skills add larksuite/cli -g -y
mkdir -p <SKILLS_DIR>
cp -R lark-setup/ <SKILLS_DIR>/lark-setup/
cp -R lark-sheets-extra/ <SKILLS_DIR>/lark-sheets-extra/
cp -R lark-base-batch/ <SKILLS_DIR>/lark-base-batch/
cp -R lark-im-card/ <SKILLS_DIR>/lark-im-card/
cp -R lark-workflow-meeting/ <SKILLS_DIR>/lark-workflow-meeting/
cp -R lark-doc-convert/ <SKILLS_DIR>/lark-doc-convert/
lark-cli --version
```

## 认证检查

安装或更新完成后，检查：

```bash
lark-cli auth status
```

- 如果已经认证，报告当前身份或状态。
- 如果尚未认证，提示用户执行 `!lark-cli auth login`，并在交互步骤完成后重新检查状态。
- 不要承诺完全无交互完成登录，因为浏览器跳转、扫码或凭据输入可能仍需要用户参与。

## 安全规则

- 用户明确表达“安装”“更新”“检查 Lark CLI 环境”时，即视为授权执行这些 setup 步骤。
- 不要自动使用 `sudo`。
- 除复制 skill 目录外，不修改用户现有的个性化 skill 配置文件。
- 如果无法识别 skill 安装目录，或虽识别出 Codex 但拿不到 `$CODEX_HOME`，都不要静默猜测，应向用户确认。

## 排障

参见 [references/troubleshooting.zh-CN.md](references/troubleshooting.zh-CN.md)。

## 参考

- [常见问题排查](references/troubleshooting.zh-CN.md)
- 官方 `lark-shared` skill
- 官方 `larksuite/cli` skill 包
