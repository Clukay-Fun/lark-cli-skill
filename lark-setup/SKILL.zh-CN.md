# lark-setup - 安装与维护 Lark CLI 环境

英文原版: [SKILL.md](SKILL.md)

本文是中文翻译版，供阅读参考。默认 skill 入口和规范内容以英文版 `SKILL.md` 为准；若两者有差异，请以英文版为准。

这是当前仓库的环境入口 skill。
当用户希望安装 `lark-cli`、升级 `lark-cli`、安装官方 `larksuite/cli` skill 包，或把本仓库扩展 skill 安装到当前 AI CLI 环境时，都应优先使用它。

## 核心原则

1. 先识别当前环境。
2. 将安装能力识别与环境识别拆开处理。
3. 使用分层降级策略：官方命令 -> GitHub Release 压缩包下载 -> 本地目录复制 -> 手动引导。
4. 每一步都必须有明确成功判据，不能只看“命令没报错”。

## 适用场景

- 首次安装，例如“帮我安装 lark-cli”或“把飞书 CLI 环境配好”。
- 安装官方 `larksuite/cli` skill 包。
- 安装或刷新当前仓库提供的扩展 skill。
- 检查 `lark-cli` 是否已经安装、是否在 `PATH` 中、是否已认证。
- 更新 `lark-cli` 或重新安装 skill 包。

## 环境与安装策略矩阵

按以下顺序检测当前 CLI 环境：

| 优先级 | 环境 | 检测方式 | 优先安装方式 | 降级方式 | 发现策略 | 验证 |
|--------|------|----------|--------------|----------|----------|------|
| 1 | Claude Code | `CLAUDE_CODE=1` | 复制到 `~/.claude/skills/`，或把 GitHub Release 压缩包解压到该目录 | 无 | 固定路径 | `ls` 加后续触发 skill 检查 |
| 2 | Codex | 存在 `CODEX_THREAD_ID` | 复制到 `$CODEX_HOME/skills/`，或把 GitHub Release 压缩包解压到该目录 | `$CODEX_HOME` 不存在时询问用户 | 环境变量 | `ls` 并确认 `$CODEX_HOME` 解析有效 |
| 3 | OpenCode | 存在 `~/.config/opencode/opencode.json` | 复制到 `~/.config/opencode/skills/`，或把 GitHub Release 压缩包解压到该目录 | 无 | 配置文件存在性 | `ls` 并检查 skill 路径或 symlink |
| 4 | Gemini CLI | 存在 `~/.gemini/settings.json` | 复制到 `~/.gemini/skills/`，或把 GitHub Release 压缩包解压到该目录 | 无 | 配置文件存在性 | `ls` 加后续触发 skill 检查 |
| 5 | Registry 型 CLI | 按 CLI 单独扩展 | 使用 CLI 官方 registry 安装命令 | 下载 GitHub Release 压缩包，或复制到探测出的落盘路径，实验性 | 查找已安装 skill 反推存储路径 | 必须验证 CLI 实际识别了 skill，不能只看文件存在 |
| 6 | 未知 | 以上都不匹配 | 无 | 询问用户 | 无 | 停下并请求更多信息 |

如果多个检测条件同时命中，按表中优先级取第一个结果。

对 Codex，仅在 `$CODEX_HOME` 已定义时使用 `$CODEX_HOME/skills/`。如果该变量不存在，应让用户确认目标目录。不要默认写入项目内的 `.codex/skills/`，除非用户明确要求这样做。

## 安装能力识别

识别出环境后，再判断该环境如何安装 skill。

可使用这些字段来描述每个环境：

- `preferred_install_method`：例如 `registry` 或 `copy`
- `preferred_install_target` 或 `preferred_install_command`
- `fallback_install_method`
- `discovery_strategy`
- `verification`

示例：

```text
environment: "Claude Code"
detection: "$CLAUDE_CODE=1"
preferred_install_method: "copy"
preferred_install_target: "~/.claude/skills/"
fallback_install_method: null
discovery_strategy: "fixed_path"
verification: "ls + skill trigger check"
```

```text
environment: "Registry-based CLI"
detection: "per-cli detection"
preferred_install_method: "registry"
preferred_install_command: "<cli> skills install <slug>"
fallback_install_method: "copy_to_discovered_path"
fallback_confidence: "experimental"
discovery_strategy: "find existing skills -> infer store path"
verification: "must confirm CLI recognizes skill, not just file exists"
```

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

### Step 4：识别环境

按上面的优先级矩阵，识别当前 CLI 环境。

### Step 5：识别安装能力

读取该环境的优先安装策略。

- 如果存在官方 registry 安装命令，走 Level 1。
- 否则，如果 GitHub Release 压缩包可访问，且目标目录明确，走 Level 1.5。
- 否则，如果本地仓库内容已存在且能解析出可写的本地 skill 目录，走 Level 2。
- 否则停在 Level 3，请求用户提供更多信息。

### Step 6：安装扩展 Skill

当前仓库的扩展 skill 都是本地目录。最稳妥的默认假设是：`lark-setup` 在仓库根目录中运行。

如果当前工作目录下找不到这些仓库目录，应停止，并要求用户从仓库根目录运行，或提供本地 checkout 路径。除非用户明确要求，否则不要静默地自行克隆或下载另一份仓库。

#### Level 1：官方 Registry 安装

如果该环境存在官方 skill 安装命令，并且对应包已发布到该平台，优先使用官方命令。

示例：

```bash
npx skills add <package> -g -y
<cli> skills install <slug>
```

#### Level 1.5：GitHub Release 压缩包

如果本地并没有现成的仓库 checkout，优先从 GitHub Release 下载标准压缩包，再直接解压到目标 skill 目录。

示例：

```bash
curl -L https://github.com/<user>/lark-cli-extra-skills/releases/latest/download/lark-cli-extra-skills.tar.gz \
  | tar xz -C <SKILLS_DIR>
```

```bash
curl -L -o /tmp/lark-cli-extra-skills.zip \
  https://github.com/<user>/lark-cli-extra-skills/releases/latest/download/lark-cli-extra-skills.zip
unzip /tmp/lark-cli-extra-skills.zip -d <SKILLS_DIR>
```

适用条件：

- 当前环境接受目录式 skill 安装
- 当前机器上还没有本仓库的本地副本
- 当前环境可以访问 GitHub

#### Level 2：本地目录复制

如果该环境支持本地目录安装，则复制 skill 到解析出的目标目录：

```bash
mkdir -p <SKILLS_DIR>
cp -R lark-setup/ <SKILLS_DIR>/lark-setup/
cp -R lark-sheets-extra/ <SKILLS_DIR>/lark-sheets-extra/
cp -R lark-base-batch/ <SKILLS_DIR>/lark-base-batch/
cp -R lark-im-card/ <SKILLS_DIR>/lark-im-card/
cp -R lark-workflow-meeting/ <SKILLS_DIR>/lark-workflow-meeting/
cp -R lark-doc-convert/ <SKILLS_DIR>/lark-doc-convert/
```

对于 Registry 型 CLI，也可以在确认落盘路径后，尝试复制到探测出的安装目录，但这只能视为实验性降级路径。

#### Level 3：手动引导

如果既没有官方安装命令，也没有可用的 GitHub Release 下载路径，也没有可确认的本地可写路径，应停止并明确报告阻塞点。

示例说明：

> 当前 CLI 环境没有可确认的本地 skill 安装路径，且此 skill 包也没有可用的官方 registry 安装命令或 GitHub Release 安装路径。你可以提供 skill 目录路径、先将该 skill 发布到对应 registry，或手动下载 release 压缩包。

## 加载验证

不要把“文件已复制”或“命令执行成功”当作最终结果。必须尽可能验证 CLI 实际识别了 skill。

- 开放目录型环境：先用 `ls` 确认文件存在，再在后续对话中尽量触发一次 skill 检查。
- 通过 GitHub Release 压缩包安装：先用 `ls` 确认解压结果，再确认目标 CLI 能看到解压后的 skill 目录。
- Registry 型环境：优先使用 `<cli> skills list` 之类的命令，确认 skill 真的出现在 CLI 的已安装列表中。
- 实验性“探测目录后复制”路径：必须明确告诉用户，文件虽已复制，但平台未必已经识别。

实验性降级路径建议使用类似这样的说明：

> Skill 文件已复制到探测到的路径 `<path>`，但该路径是通过分析已有已安装 skill 推断出来的，并非官方文档声明的安装位置。请重启 CLI 后确认 skill 是否被识别。如果未识别，平台可能还需要索引注册、缓存刷新或其他特定步骤。

## 更新流程

当用户要求更新环境时，先执行：

```bash
npm update -g @anthropic-ai/lark-cli
npx skills add larksuite/cli -g -y
```

然后重复以下步骤：

1. 识别环境
2. 识别安装能力
3. 走对应的 Level 1 / Level 2 / Level 3 安装路径
4. 执行加载验证

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
- 除安装或复制 skill 目录外，不修改用户现有的个性化 skill 配置文件。
- 如果无法确认 skill 安装目录，不要静默猜测。
- 不要把实验性“探测落盘路径后复制”描述成完全受支持的官方安装方式。

## 排障

参见 [references/troubleshooting.zh-CN.md](references/troubleshooting.zh-CN.md)。

## 参考

- [常见问题排查](references/troubleshooting.zh-CN.md)
- 官方 `lark-shared` skill
- 官方 `larksuite/cli` skill 包
