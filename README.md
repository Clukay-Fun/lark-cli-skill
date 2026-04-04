# lark-cli Extra Skills

Extra skills that cover workflows and API surfaces not included in the official `larksuite/cli` skill set.

Chinese translation: [README.zh-CN.md](README.zh-CN.md)

## Language Policy

- `README.md`, each `SKILL.md`, and each default `references/*.md` file are the canonical English sources.
- Tooling should read the English files by default, especially `SKILL.md`.
- Matching `*.zh-CN.md` files are Chinese translations for human readers.
- When content diverges, treat the English version as the source of truth and update translations afterward.

## Skills

| Skill | Type | Description |
|-------|------|-------------|
| `lark-setup` | Environment management | Install, update, verify, and authenticate the Lark CLI environment and skill packs |
| `lark-sheets-extra` | Domain extension | Sheets v2 helpers for merge cells, styling, and row/column operations |
| `lark-base-batch` | Domain extension | Bitable batch record operations: `batch_create` / `batch_update` / `batch_delete` |
| `lark-im-card` | Domain extension | Interactive card authoring guide with JSON structure and reusable templates |
| `lark-workflow-meeting` | Workflow | Schedule a meeting and notify attendees: availability lookup -> event creation -> message send |
| `lark-doc-convert` | Workflow | Unified entry for importing to and exporting from Lark docs |

## Installation

In a conversation with your AI CLI agent, say:

```text
Install lark-cli and the extra Lark skills for me.
```

The `lark-setup` skill is the preferred entry point. It can detect the active CLI environment, install or update `lark-cli`, install the official `larksuite/cli` skill pack, and copy this repository's extra skills into the resolved skill directory.

## Example Setup Conversations

### First-Time Setup

User:

```text
Install lark-cli and the extra Lark skills for me.
```

Agent behavior:

- Checks `node`, `npm`, and `lark-cli`
- Installs `lark-cli` if needed
- Installs the official `larksuite/cli` skill pack
- Detects the current AI CLI environment
- Copies `lark-setup` and the extra skills into the resolved skill directory
- Checks `lark-cli auth status`

### Update an Existing Environment

User:

```text
Update my Lark CLI environment.
```

Agent behavior:

- Runs `npm update -g @anthropic-ai/lark-cli`
- Refreshes the official `larksuite/cli` skill pack
- Re-copies the extra skills into the detected skill directory
- Verifies the installed version and skill presence

### Verify Installation Only

User:

```text
Is lark-cli installed and authenticated?
```

Agent behavior:

- Checks whether `lark-cli` is on `PATH`
- Prints or reports the installed version
- Runs `lark-cli auth status`
- Tells the user whether follow-up login is still required

### Authentication Follow-Up

User:

```text
Finish setting up Lark CLI auth.
```

Agent behavior:

- Runs `lark-cli auth status`
- If login is still required, tells the user to run `!lark-cli auth login`
- Re-checks auth state after the user completes the interactive step

Manual installation is still available:

```bash
npx skills add larksuite/cli -g -y
cp -r lark-setup/ ~/.claude/skills/lark-setup/
cp -r lark-sheets-extra/ ~/.claude/skills/lark-sheets-extra/
cp -r lark-base-batch/ ~/.claude/skills/lark-base-batch/
cp -r lark-im-card/ ~/.claude/skills/lark-im-card/
cp -r lark-workflow-meeting/ ~/.claude/skills/lark-workflow-meeting/
cp -r lark-doc-convert/ ~/.claude/skills/lark-doc-convert/
```

Manual target directories vary by CLI environment:

- Claude Code: `~/.claude/skills/`
- Codex: `$CODEX_HOME/skills/`
- OpenCode: `~/.config/opencode/skills/`
- Gemini CLI: `~/.gemini/skills/`

For Codex, use `$CODEX_HOME/skills/` only when `$CODEX_HOME` is defined. If it is not set, confirm the target directory instead of guessing.

These extra skills depend on capabilities provided by the official `larksuite/cli` skill pack. This repository only contains supplemental documentation and helper scripts; it does not vendor official skills such as `lark-shared`, `lark-base`, `lark-im`, `lark-calendar`, or `lark-drive`.

## Requirements

- `lark-cli` available on `PATH`
- Python 3 for files under `scripts/`
- The official `lark-shared` skill for authentication and safety rules
- The official domain skills required by each extension skill, such as `lark-base`, `lark-im`, and `lark-calendar`

## Documentation Conventions

- Every `SKILL.md` follows the same rough order: prerequisites -> use cases / capabilities -> commands or workflow -> permissions -> references.
- Command examples use `bash` fences and placeholder names such as `<TOKEN>`, `<ID>`, and `<URL>`.
- References to official external skills are written as plain text instead of repo-local links, to avoid broken links in this repository.
- Chinese translations are kept next to the English originals with the `.zh-CN.md` suffix so the default entrypoints remain stable for tools.
