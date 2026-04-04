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
Use it when the user wants to install `lark-cli`, update it, install the official `larksuite/cli` skill pack, or install these extra skills into the active AI CLI environment.

## Core Principles

1. Detect the current environment first.
2. Detect installation capability separately from environment detection.
3. Use a three-level fallback strategy: official install command -> local directory copy -> manual guidance.
4. Require an explicit success check after each installation path. "No error" is not enough.

## Use Cases

- First-time setup such as "install lark-cli" or "set up the Lark CLI environment".
- Install the official `larksuite/cli` skill pack.
- Install or refresh this repository's extra skills.
- Check whether `lark-cli` is installed, available on `PATH`, or authenticated.
- Update `lark-cli` or reinstall the skill packs.

## Environment and Install Strategy Matrix

Detect the active CLI environment in this order:

| Priority | Environment | Detection | Preferred install | Fallback | Discovery strategy | Verification |
|----------|-------------|-----------|-------------------|----------|--------------------|--------------|
| 1 | Claude Code | `CLAUDE_CODE=1` | Copy to `~/.claude/skills/` | None | Fixed path | `ls` plus a later skill-trigger check |
| 2 | Codex | `CODEX_THREAD_ID` exists | Copy to `$CODEX_HOME/skills/` | Ask the user if `$CODEX_HOME` is unavailable | Environment variable | `ls` plus confirm that `$CODEX_HOME` resolves correctly |
| 3 | OpenCode | `~/.config/opencode/opencode.json` exists | Copy to `~/.config/opencode/skills/` | None | Config presence | `ls` plus inspect the installed skill path or symlink |
| 4 | Gemini CLI | `~/.gemini/settings.json` exists | Copy to `~/.gemini/skills/` | None | Config presence | `ls` plus a later skill-trigger check |
| 5 | Registry-based CLI | Per-CLI detection | Use the CLI's official registry install command | Copy to a discovered install path, experimental | Find existing installed skills and infer the store path | Must confirm the CLI recognizes the skill, not just that files exist |
| 6 | Unknown | None matched | None | Ask the user for details | None | Stop and request more information |

If more than one signal matches, use the first match in the table.

For Codex, use `$CODEX_HOME/skills/` only when `$CODEX_HOME` is defined. If it is not set, ask the user to confirm the target directory. Do not default to a project-local `.codex/skills/` path unless the user explicitly requests that layout.

## Installation Capability Detection

After the environment is detected, determine how that environment expects skills to be installed.

Use these concepts:

- `preferred_install_method`: for example `registry` or `copy`
- `preferred_install_target` or `preferred_install_command`
- `fallback_install_method`
- `discovery_strategy`
- `verification`

Examples:

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

### Step 4: Detect the Environment

Apply the priority matrix above and resolve the current CLI environment.

### Step 5: Detect Installation Capability

Read the environment's preferred installation strategy.

- If an official registry install command is available, choose Level 1.
- Otherwise, if a writable local skill directory can be resolved, choose Level 2.
- Otherwise, stop at Level 3 and ask the user for guidance.

### Step 6: Install the Extra Skills

This repository contains the extra skills locally. The safest default assumption is that `lark-setup` is being run from the repository root.

If the repository folders are not present in the current working directory, stop and ask the user to run the setup from the repository root or provide a local checkout path. Do not silently clone or download another copy unless the user explicitly asks for that behavior.

#### Level 1: Official Registry Install

Use the environment's official skill installation command when available and when the package has been published there.

Examples:

```bash
npx skills add <package> -g -y
<cli> skills install <slug>
```

#### Level 2: Local Directory Copy

If the environment supports direct local installation, copy the skills into the resolved target directory:

```bash
mkdir -p <SKILLS_DIR>
cp -R lark-setup/ <SKILLS_DIR>/lark-setup/
cp -R lark-sheets-extra/ <SKILLS_DIR>/lark-sheets-extra/
cp -R lark-base-batch/ <SKILLS_DIR>/lark-base-batch/
cp -R lark-im-card/ <SKILLS_DIR>/lark-im-card/
cp -R lark-workflow-meeting/ <SKILLS_DIR>/lark-workflow-meeting/
cp -R lark-doc-convert/ <SKILLS_DIR>/lark-doc-convert/
```

For registry-based CLIs, you may also try copying into a discovered install path only as an experimental fallback after identifying that path from existing installed skills or platform configuration.

#### Level 3: Manual Guidance

If neither an official install command nor a writable local path is available, stop and explain the blocker.

Example report:

> This CLI environment does not expose a confirmed local skill install path, and no supported registry install command is available for this package. You can either provide the skill directory path, or publish the skill to the environment's registry first.

## Load Verification

Do not treat file copy or command success as the final result. Verify that the environment can actually see the skill.

- Open directory environments: verify files with `ls`, then use a later skill-trigger check when possible.
- Registry environments: prefer commands such as `<cli> skills list` to confirm the skill appears in the registry-managed list.
- Experimental copy-to-discovered-path fallback: explicitly tell the user that the files were copied, but recognition is not guaranteed.

Use wording like this for experimental fallback:

> Skill files were copied to the discovered path `<path>`, but this path was inferred from existing installed skills rather than documented as the official install location. Please restart the CLI and confirm that the skill is recognized. If it is not, the platform may require indexing, cache refresh, registration, or another platform-specific step.

## Update Flow

When the user asks to update the environment:

```bash
npm update -g @anthropic-ai/lark-cli
npx skills add larksuite/cli -g -y
```

Then repeat:

1. environment detection
2. installation capability detection
3. the appropriate Level 1 / Level 2 / Level 3 path
4. load verification

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
- Do not modify existing user-specific skill configuration files beyond installing or copying the skill directories.
- Do not guess an unknown skill directory silently.
- Do not present an experimental discovered-path copy as a fully supported install path.

## Troubleshooting

See [references/troubleshooting.md](references/troubleshooting.md).

## References

- [Troubleshooting](references/troubleshooting.md)
- Official `lark-shared` skill
- Official `larksuite/cli` skill pack
