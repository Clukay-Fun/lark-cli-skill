# Troubleshooting

Chinese translation: [troubleshooting.zh-CN.md](troubleshooting.zh-CN.md)

## Node.js Missing

- Symptom: `node --version` or `npm --version` fails.
- Action: ask the user to install Node.js 16 or later first.
- Reference: [Node.js Downloads](https://nodejs.org/en/download)

## npm Permission Denied

- Symptom: `npm install -g` or `npm update -g` fails with permission errors.
- Action: do not add `sudo` automatically.
- Suggestion: let the user choose between fixing npm global prefix settings or rerunning with elevated privileges on their own.

## Network Timeout

- Symptom: `npm install`, `npm update`, or `npx skills add` times out.
- Action: suggest checking proxy settings, retrying later, or switching npm registry mirrors if the user's environment requires it.

## `lark-cli` Installed but Not on `PATH`

- Symptom: installation succeeds, but `lark-cli --version` still fails.
- Action: inspect the npm global bin path and explain how to add it to `PATH`.

## Skill Directory Missing

- Symptom: the resolved skill directory does not exist.
- Action: create it with `mkdir -p <SKILLS_DIR>` before copying files.

## Repository Folders Not Found

- Symptom: the current working directory does not contain `lark-setup/`, `lark-sheets-extra/`, and the other expected folders.
- Action: ask the user to run the setup from the repository root or provide the local checkout path.

## Unknown CLI Environment

- Symptom: none of the known environment checks match.
- Action: ask the user to provide the target skill directory instead of guessing.
