---
name: lark-setup
version: 1.0.0
description: "Install, update, and verify lark-cli and the official or extra skill packs. Use this skill when lark-cli is missing, outdated, unauthenticated, or when the user wants a ready-to-use Lark CLI environment."
metadata:
  requires:
    bins: ["node", "npm"]
---

# lark-setup - Install and Maintain the Lark CLI Environment

Chinese translation: [SKILL.zh-CN.md](SKILL.zh-CN.md)

This is the environment-entry skill for this repository.
Use it when the user wants to install `lark-cli`, update it, install the official `larksuite/cli` skill pack, or copy these extra skills into the active AI CLI environment.

## Use Cases

- First-time setup such as "install lark-cli" or "set up the Lark CLI environment".
- Install the official `larksuite/cli` skill pack.
- Install or refresh this repository's extra skills.
- Check whether `lark-cli` is installed, available on `PATH`, or authenticated.
- Update `lark-cli` or reinstall the skill packs.

## Environment Detection

Detect the active CLI environment in this order:

| Priority | Detection | Environment | Skill directory |
|----------|-----------|-------------|-----------------|
| 1 | `CLAUDE_CODE=1` | Claude Code | `~/.claude/skills/` |
| 2 | `CODEX_THREAD_ID` exists | Codex | `$CODEX_HOME/skills/` |
| 3 | `~/.config/opencode/opencode.json` exists | OpenCode | `~/.config/opencode/skills/` |
| 4 | `~/.gemini/settings.json` exists | Gemini CLI | `~/.gemini/skills/` |
| 5 | none matched | Unknown | ask the user to provide a target directory |

If more than one signal matches, use the first match in the table.
For Codex, prefer `$CODEX_HOME/skills/` only when `$CODEX_HOME` is defined. If it is not set, ask the user to confirm the Codex skill directory. Do not default to a project-local `.codex/skills/` path unless the user explicitly asks for that layout.

## Installation Flow

Run the following checks in order. Skip steps that are already satisfied.

### Step 1: Check Prerequisites

```bash
node --version
npm --version
```

- Require Node.js 16 or later.
- If Node.js is missing or too old, stop and tell the user to install or upgrade Node.js first.

### Step 2: Check or Install `lark-cli`

```bash
which lark-cli
lark-cli --version
```

If `lark-cli` is missing:

```bash
npm install -g @anthropic-ai/lark-cli
lark-cli --version
```

Do not automatically add `sudo`. If the global install fails because of permissions, explain the issue and point the user to the troubleshooting reference.

### Step 3: Install or Refresh the Official Skill Pack

```bash
npx skills add larksuite/cli -g -y
```

### Step 4: Install or Refresh These Extra Skills

This repository contains the extra skills locally. The safest default assumption is that `lark-setup` is being run from the repository root.

Create the target directory if needed, then copy these folders into it:

```bash
mkdir -p <SKILLS_DIR>
cp -R lark-setup/ <SKILLS_DIR>/lark-setup/
cp -R lark-sheets-extra/ <SKILLS_DIR>/lark-sheets-extra/
cp -R lark-base-batch/ <SKILLS_DIR>/lark-base-batch/
cp -R lark-im-card/ <SKILLS_DIR>/lark-im-card/
cp -R lark-workflow-meeting/ <SKILLS_DIR>/lark-workflow-meeting/
cp -R lark-doc-convert/ <SKILLS_DIR>/lark-doc-convert/
```

If the repository folders are not present in the current working directory, stop and ask the user to run the setup from the repository root or provide a local checkout path. Do not silently clone or download another copy unless the user explicitly asks for that behavior.

### Step 5: Verify

```bash
lark-cli --version
ls <SKILLS_DIR>
```

Confirm that the expected skills are present and report the resolved installation directory.

## Update Flow

When the user asks to update the environment:

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

## Authentication Check

After installation or update, check:

```bash
lark-cli auth status
```

- If already authenticated, report the current identity or status.
- If authentication is required, ask the user to run `!lark-cli auth login`, then re-check status after the interactive step.
- Do not promise a fully non-interactive login flow; browser or credential prompts may require user action.

## Safety Rules

- The user's request to install, update, or verify the Lark CLI environment counts as permission to run the setup steps.
- Do not use `sudo` automatically.
- Do not modify existing user-specific skill configuration files beyond copying these skill directories.
- Do not guess an unknown skill directory silently. Ask the user when environment detection fails or when the Codex environment is detected but `$CODEX_HOME` is unavailable.

## Troubleshooting

See [references/troubleshooting.md](references/troubleshooting.md).

## References

- [Troubleshooting](references/troubleshooting.md)
- Official `lark-shared` skill
- Official `larksuite/cli` skill pack
