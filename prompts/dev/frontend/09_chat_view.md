# Member Chat View (AI Booking Assistant)

Build `MemberChatView.vue` — the conversational interface for booking appointments with the AI assistant.

## Layout

- Full-height chat UI (no sidebar)
- Header: "CareFlow AI" + back button to dashboard
- Scrollable message list (takes remaining height)
- Fixed input area at the bottom: textarea + send button

## Message Display

Each message in the conversation should display:
- **User messages**: right-aligned, light background bubble
- **Assistant messages**: left-aligned, slightly darker background — rendered as markdown via `MarkdownMessage` component

## Session Persistence

On mount:
- Check `localStorage` for a `"chat_session_id"` key
- If found, call `getSession(sessionId)` and restore previous messages
- If not found, start fresh (no session ID until first message is sent)

On first send:
- The API returns a `session_id` — store it in `localStorage` as `"chat_session_id"`

## Sending a Message

1. Append the user's message immediately to the local message list (optimistic)
2. Show a loading indicator in the assistant bubble
3. Call `sendMessage(sessionId, message)`
4. Replace the loading indicator with the actual reply
5. Auto-scroll to the bottom after each message

## Input Behavior
- Textarea supports multi-line input
- `Enter` submits, `Shift+Enter` adds a newline
- Disable input while a response is loading

## Initial Greeting

On mount (new session), show an initial assistant message:
> "Hi! I'm CareFlow AI. I can help you book an appointment. What kind of doctor are you looking for?"

## Notes
- Do not store messages in Pinia — chat state is local to this view
- When the step reaches `"completed"`, show a "Back to Dashboard" button and disable the input
