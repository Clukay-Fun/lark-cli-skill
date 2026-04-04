# lark-im-card - 飞书消息卡片构建

英文原版: [SKILL.md](SKILL.md)

本文是中文翻译版，供阅读参考。默认 skill 入口和规范内容以英文版 `SKILL.md` 为准；若两者有差异，请以英文版为准。

**前置条件：** 先安装官方 `larksuite/cli` skill 包，并阅读官方 `lark-shared` skill 中的认证和安全规则。如果当前环境还没有 `lark-cli`，优先使用本仓库的 `lark-setup` skill 完成安装或刷新。

飞书消息卡片，也就是 `interactive` 消息，比纯文本或 post 消息更丰富，支持标题、多栏布局、按钮、链接和 Markdown。
这个 skill 用来指导 AI 正确构造卡片 JSON，并通过官方 `lark-im` skill 发送。

## 适用场景

- 需要发送比纯文本更丰富的通知消息。
- 需要在聊天中展示结构化数据、按钮或更精致的布局。
- 需要给其他 workflow skill 提供可复用的卡片模板。

## 发送方式

```bash
lark-cli im +messages-send \
  --chat-id oc_xxx \
  --msg-type interactive \
  --content '<card JSON>'
```

如果要发给个人，可以把 `--chat-id` 换成 `--user-id ou_xxx`。

## 卡片 JSON 顶层结构

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

| 字段 | 必填 | 说明 |
|------|------|------|
| config | 否 | `wide_screen_mode: true` 表示宽屏布局 |
| header | 否 | 卡片标题和主题色 |
| elements | 是 | 卡片内容元素数组 |

### `header.template` 颜色

`blue` `wathet` `turquoise` `green` `yellow` `orange` `red` `carmine` `violet` `purple` `indigo` `grey`

## 常用元素类型

参见 [references/card-elements.zh-CN.md](references/card-elements.zh-CN.md)。

| 元素 | 用途 |
|------|------|
| `markdown` | Markdown 文本 |
| `div` | 文本块，可配合 `fields` 做多栏 |
| `column_set` + `column` | 多列布局 |
| `action` | 按钮组 |
| `hr` | 分割线 |
| `note` | 底部备注 |
| `img` | 图片 |

## 快速示例

### 最简卡片

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

### 带按钮的通知

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

更多模板见 [references/card-templates.zh-CN.md](references/card-templates.zh-CN.md)。

## 常见错误

| 错误 | 原因 | 修正 |
|------|------|------|
| `invalid card` | JSON 格式错误 | 检查 JSON 语法，确保 `elements` 是数组 |
| `tag is required` | 元素缺少 `tag` 字段 | 每个元素都必须带 `tag` |
| `content` 未渲染 | 用了 `text` 而不是 `content` | `markdown` 元素必须用 `content` |
| 按钮不显示 | 按钮没有包在 `action` 容器内 | 按钮必须放在 `{"tag":"action","actions":[...]}` 里 |

## 调试

```bash
lark-cli im +messages-send --chat-id oc_xxx --msg-type interactive \
  --content '{"config":{"wide_screen_mode":true},"elements":[{"tag":"markdown","content":"test"}]}' \
  --dry-run
```

## 参考

- [卡片元素速查](references/card-elements.zh-CN.md)
- [卡片模板](references/card-templates.zh-CN.md)
- 官方 `lark-im` skill
