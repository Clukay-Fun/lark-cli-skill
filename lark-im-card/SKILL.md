---
name: lark-im-card
version: 1.0.0
description: "Guide for building Lark interactive cards. Use this skill when an AI agent needs to craft rich message cards with structured JSON and reusable templates."
metadata:
  requires:
    bins: ["lark-cli"]
---

# lark-im-card - Lark Interactive Card Authoring

Chinese translation: [SKILL.zh-CN.md](SKILL.zh-CN.md)

**Prerequisites:** install the official `larksuite/cli` skill pack first, then review the authentication and safety rules in the official `lark-shared` skill. If `lark-cli` is unavailable, use the local `lark-setup` skill to install or refresh the environment first.

Lark interactive cards (`interactive` messages) are richer than plain text or post messages and support titles, multi-column layouts, buttons, links, and Markdown.
This skill teaches the agent how to build valid card JSON and send it through the official `lark-im` skill.

## Use Cases

- Send richer notifications than plain text can support.
- Present structured data, buttons, or polished layouts in chat.
- Reuse templates from this skill inside other workflow skills.

## Sending

```bash
lark-cli im +messages-send \
  --chat-id oc_xxx \
  --msg-type interactive \
  --content '<card JSON>'
```

You can also send to a user by using `--user-id ou_xxx` instead of `--chat-id`.

## Top-Level Card JSON

```json
{
  "config": { "wide_screen_mode": true },
  "header": {
    "title": { "tag": "plain_text", "content": "卡片标题" },
    "template": "blue"
  },
  "elements": [
    ...
  ]
}
```

| Field | Required | Notes |
|------|----------|-------|
| config | No | `wide_screen_mode: true` enables wide layout |
| header | No | Card title and theme color |
| elements | Yes | Array of card elements |

### `header.template` Colors

`blue` `wathet` `turquoise` `green` `yellow` `orange` `red` `carmine` `violet` `purple` `indigo` `grey`

## Common Element Types

See [references/card-elements.md](references/card-elements.md).

| Element | Purpose |
|---------|---------|
| `markdown` | Markdown text |
| `div` | Text block, optionally with `fields` |
| `column_set` + `column` | Multi-column layout |
| `action` | Button group |
| `hr` | Divider |
| `note` | Footer note |
| `img` | Image |

## Quick Examples

### Minimal Card

```json
{
  "config": { "wide_screen_mode": true },
  "header": {
    "title": { "tag": "plain_text", "content": "通知" },
    "template": "blue"
  },
  "elements": [
    { "tag": "markdown", "content": "**项目更新**\n\n进度已更新，请查看。" }
  ]
}
```

### Notification with a Button

```json
{
  "config": { "wide_screen_mode": true },
  "header": {
    "title": { "tag": "plain_text", "content": "部署完成" },
    "template": "green"
  },
  "elements": [
    { "tag": "markdown", "content": "**服务**: user-api\n**环境**: production\n**版本**: v2.3.1" },
    { "tag": "hr" },
    {
      "tag": "action",
      "actions": [
        {
          "tag": "button",
          "text": { "tag": "plain_text", "content": "查看详情" },
          "url": "https://example.com/deploy/123",
          "type": "primary"
        }
      ]
    }
  ]
}
```

More templates are available in [references/card-templates.md](references/card-templates.md).

## Common Errors

| Error | Cause | Fix |
|------|-------|-----|
| `invalid card` | Invalid JSON | Validate the JSON and ensure `elements` is an array |
| `tag is required` | Missing `tag` on an element | Every element must contain a `tag` field |
| `content` not rendered | Used `text` instead of `content` | `markdown` elements must use `content` |
| Buttons missing | Buttons are not wrapped in an `action` container | Buttons must be inside `{"tag":"action","actions":[...]}` |

## Debugging

```bash
# Preview with --dry-run first
lark-cli im +messages-send --chat-id oc_xxx --msg-type interactive \
  --content '{"config":{"wide_screen_mode":true},"elements":[{"tag":"markdown","content":"test"}]}' \
  --dry-run
```

## References

- [Card element quick reference](references/card-elements.md)
- [Card templates](references/card-templates.md)
- Official `lark-im` skill
