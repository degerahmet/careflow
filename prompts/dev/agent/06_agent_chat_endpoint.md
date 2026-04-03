# Agent Chat Endpoint

Expose the booking assistant via a REST API endpoint in `backend/agent/views.py`.

## Endpoints

### `POST /api/agent/chat/`

Request body:
```json
{
  "session_id": "optional-uuid-string",
  "message": "I need to see a cardiologist"
}
```

Behavior:
1. If `session_id` is provided, load the existing `BookingSession` for that ID and the authenticated member
2. If no `session_id`, create a new `BookingSession` with `step="collecting_intent"` and empty `draft`/`messages`
3. Call `handle_message(session, message)` from `agent/orchestrator.py`
4. Return the result dict

Response:
```json
{
  "session_id": "uuid",
  "reply": "...",
  "step": "provider_selection",
  "data": {
    "providers": [...],
    "slots": [],
    "appointment": null,
    "draft": {}
  }
}
```

### `GET /api/agent/session/?session_id=<uuid>`

- Load and return the full session state (messages, draft, step) for the given session_id
- Return `404` if not found or if the session doesn't belong to the authenticated user

## Permissions
- Both endpoints require `IsAuthenticated`
- Enforce that the session belongs to `request.user` — never allow cross-user session access

## Wiring
- Add `agent/urls.py` with both URL patterns
- Include in `backend/config/urls.py` under `api/agent/`
