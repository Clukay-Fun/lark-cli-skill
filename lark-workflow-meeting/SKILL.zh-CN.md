# lark-workflow-meeting - 创建会议并通知参会人

英文原版: [SKILL.md](SKILL.md)

本文是中文翻译版，供阅读参考。默认 skill 入口和规范内容以英文版 `SKILL.md` 为准；若两者有差异，请以英文版为准。

**前置条件：** 先安装官方 `larksuite/cli` skill 包，并阅读官方 `lark-shared` skill 中的认证和安全规则。

这个工作流会编排 calendar、contact 和 im 三个领域，从“找时间”一直走到“发通知”。
如果只需要处理日程，使用官方 `lark-calendar` skill；如果只需要发消息，使用官方 `lark-im` skill。

## 适用场景

- 用户说“帮我约个会”“安排一个会议”“建个会议并通知大家”之类的话。
- 用户提供了参会人和大致时间，希望代理自动处理忙闲查询、建会和通知。

## 工作流

`用户请求 -> 确定参会人 -> 查询忙闲 -> 用户确认时间 -> 创建日程 -> 发送通知`

### Step 1: 确定参会人

如果用户给的是姓名而不是 `open_id`，先搜索：

```bash
lark-cli contact +search-user --query "张三"
```

从结果中提取 `open_id`（`ou_xxx`）。
如果有多个同名用户，列出候选项让用户选择。

### Step 2: 查询忙闲或推荐时段

**给了明确时间点**：

```bash
lark-cli calendar +freebusy \
  --start "2026-03-25T14:00:00+08:00" \
  --end "2026-03-25T15:00:00+08:00" \
  --user-ids "ou_aaa,ou_bbb"
```

如果有冲突，就告诉用户并询问是否保留该时间或改期。

**给了时间范围**：

```bash
lark-cli calendar +suggestion \
  --start "2026-03-25T00:00:00+08:00" \
  --end "2026-03-25T23:59:59+08:00" \
  --attendee-ids "ou_aaa,ou_bbb" \
  --duration-minutes 30
```

展示建议时段，等待用户选择。

**没有给时间信息：**
可以先推断一个近期窗口，例如今天或接下来两天，再走 `+suggestion`。

> 涉及“明天”“后天下午”这类相对时间时，建议用系统命令 `date` 计算，不要心算。

### Step 3: 让用户确认时间

**在用户明确确认时间之前，不要创建日程。**

向用户确认：
- 会议标题
- 开始和结束时间
- 参会人列表
- 会议描述（如果有）

### Step 4: 创建日程

```bash
lark-cli calendar +create \
  --summary "产品需求评审" \
  --start "2026-03-25T14:00:00+08:00" \
  --end "2026-03-25T15:00:00+08:00" \
  --attendee-ids "ou_aaa,ou_bbb,ou_ccc" \
  --description "议题：Q2 需求优先级排序"
```

`+create` 会自动：
- 设置 `free_busy_status: busy`
- 添加会前 5 分钟提醒
- 邀请所有 `attendee-ids`，包括 `ou_` 用户、`oc_` 群组、`omm_` 会议室
- 如果添加参会人失败，则回滚删除空日程

### Step 5: 发送通知消息

建会后，Lark 会自动发送日历邀请。
如果用户还希望在群里补发一条带议题或背景材料的消息，可以再用 im 发送。

卡片构建细节参见 [../lark-im-card/SKILL.zh-CN.md](../lark-im-card/SKILL.zh-CN.md)。

### Step 6: 向用户反馈

向用户汇总：
- 日程已创建，附带 `event_id`
- 参会人列表
- 消息发到了哪个群或个人

## 所需权限

```bash
lark-cli auth login --domain calendar,contact,im
```

| 操作 | 所需 scope |
|------|-----------|
| 搜索用户 | `contact:user:search` |
| 查询忙闲 | `calendar:calendar.free_busy:read` |
| 推荐时段 | `calendar:calendar.free_busy:read`, `calendar:calendar.event:read` |
| 创建日程 | `calendar:calendar.event:create`, `calendar:calendar.event:update` |
| 发送消息 | `im:message` 或 `im:message:send_as_bot` |

## 参考

- 官方 `lark-calendar` skill
- 官方 `lark-im` skill
- [本仓库的 `lark-im-card` skill](../lark-im-card/SKILL.zh-CN.md)
- 官方 `lark-contact` skill
