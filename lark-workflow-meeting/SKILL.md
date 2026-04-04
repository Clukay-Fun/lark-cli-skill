---
name: lark-workflow-meeting
version: 1.0.0
description: "Workflow for creating a meeting and notifying attendees. Use this skill when a user wants help finding time, creating an event, and sending meeting notifications."
metadata:
  requires:
    bins: ["lark-cli"]
---

# lark-workflow-meeting - Create a Meeting and Notify Attendees

Chinese translation: [SKILL.zh-CN.md](SKILL.zh-CN.md)

**Prerequisites:** install the official `larksuite/cli` skill pack first, then review the authentication and safety rules in the official `lark-shared` skill.

This workflow orchestrates the calendar, contact, and im domains to complete the full flow from time selection to attendee notification.
For standalone calendar operations, use the official `lark-calendar` skill. For standalone messaging, use the official `lark-im` skill.

## Use Cases

- The user says things like "schedule a meeting", "set up a meeting", or "create a meeting and notify everyone".
- The user provides attendees and a rough time window and expects the agent to handle availability lookup, event creation, and follow-up messaging.

## Workflow

`User request -> identify attendees -> check availability -> confirm the time -> create the event -> send notifications`

### Step 1: Identify Attendees

If the user provides names instead of `open_id`, search first:

```bash
lark-cli contact +search-user --query "Alice"
```

Extract the attendee `open_id` values (`ou_xxx`) from the results.
If multiple users share the same name, show the options and let the user choose.

### Step 2: Check Availability or Suggest Time Slots

Choose the strategy based on how specific the user is about time.

**Specific time provided**:

```bash
# Check attendee availability for an exact window
lark-cli calendar +freebusy \
  --start "2026-03-25T14:00:00+08:00" \
  --end "2026-03-25T15:00:00+08:00" \
  --user-ids "ou_aaa,ou_bbb"
```

If there is a conflict, report it and ask whether to keep the time or choose a different slot.

**A broader time range provided**:

```bash
# Suggest time slots for the attendees
lark-cli calendar +suggestion \
  --start "2026-03-25T00:00:00+08:00" \
  --end "2026-03-25T23:59:59+08:00" \
  --attendee-ids "ou_aaa,ou_bbb" \
  --duration-minutes 30
```

Show the suggested slots and wait for the user to choose one.

**No time information provided:**
infer a near-term window such as today or the next two days, then use `+suggestion`.

> **Date calculation:** when resolving relative times such as "tomorrow", use a system command like `date` instead of mental math.

### Step 3: Confirm the Time with the User

**Do not create the event until the user explicitly confirms the time.**

Show the user:
- Meeting title
- Start and end time
- Attendee list
- Meeting description, if present

### Step 4: Create the Event

```bash
lark-cli calendar +create \
  --summary "Product Requirements Review" \
  --start "2026-03-25T14:00:00+08:00" \
  --end "2026-03-25T15:00:00+08:00" \
  --attendee-ids "ou_aaa,ou_bbb,ou_ccc" \
  --description "Agenda: prioritize Q2 requirements"
```

`+create` automatically:
- Sets `free_busy_status: busy`
- Adds a 5-minute reminder
- Invites all `attendee-ids`, including `ou_` users, `oc_` groups, and `omm_` meeting rooms
- Rolls back the empty event if attendee creation fails

### Step 5: Send Notification Messages

After the event is created, Lark automatically sends calendar invitations.
If the user also wants a follow-up chat notification with agenda or context, send it through im.

**Markdown notification:**

```bash
lark-cli im +messages-send --chat-id oc_xxx --markdown $'## Meeting Notice\n\n**Topic**: Product Requirements Review\n**Time**: 03-25 14:00-15:00\n**Attendees**: Alice, Bob, Carol\n\n**Agenda**:\n1. Prioritize Q2 requirements\n2. Confirm the technical plan\n3. Align the schedule\n\nPlease join on time.'
```

**Card notification:**

```bash
lark-cli im +messages-send --chat-id oc_xxx --msg-type interactive --content '{
  "config": { "wide_screen_mode": true },
  "header": {
    "title": { "tag": "plain_text", "content": "Meeting Notice" },
    "template": "violet"
  },
  "elements": [
    { "tag": "markdown", "content": "**Product Requirements Review**" },
    {
      "tag": "div",
      "fields": [
        { "is_short": true, "text": { "tag": "lark_md", "content": "**Time**\n03-25 14:00-15:00" } },
        { "is_short": true, "text": { "tag": "lark_md", "content": "**Organizer**\nCarol" } }
      ]
    },
    { "tag": "markdown", "content": "**Agenda**\n1. Prioritize Q2 requirements\n2. Confirm the technical plan\n3. Align the schedule" },
    { "tag": "hr" },
    { "tag": "note", "elements": [{ "tag": "plain_text", "content": "Please join on time" }] }
  ]
}'
```

For card construction details, see [../lark-im-card/SKILL.md](../lark-im-card/SKILL.md).

### Step 6: Report Back

Summarize the outcome for the user:
- Event created, including `event_id`
- Attendee list
- Which chat or user received the notification

## Required Permissions

```bash
lark-cli auth login --domain calendar,contact,im
```

| Operation | Required scope |
|-----------|----------------|
| Search users | `contact:user:search` |
| Read free/busy | `calendar:calendar.free_busy:read` |
| Suggest time slots | `calendar:calendar.free_busy:read`, `calendar:calendar.event:read` |
| Create calendar events | `calendar:calendar.event:create`, `calendar:calendar.event:update` |
| Send messages | `im:message` or `im:message:send_as_bot` |

## References

- Official `lark-calendar` skill
- Official `lark-im` skill
- [This repo's `lark-im-card` skill](../lark-im-card/SKILL.md)
- Official `lark-contact` skill
