# Orchestrator — State Machine Logic

Implement the core booking assistant orchestrator in `backend/agent/orchestrator.py`.

## Function Signature

```python
def handle_message(session: BookingSession, message: str) -> dict:
    ...
```

Returns:
```json
{
  "session_id": "<uuid>",
  "reply": "<assistant message>",
  "step": "<current step>",
  "data": {
    "providers": [],
    "slots": [],
    "appointment": null,
    "draft": {}
  }
}
```

## State Machine Flow

1. **Extract** — call `_llm_extract(session, message)` to get structured fields from the user's message
2. **Merge** — update `session.draft` with any non-null extracted fields
3. **Transition** — check the current step and advance if conditions are met:
   - `collecting_intent` → if `draft.specialty` is set: call `search_providers(specialty)`, store results in `draft.providers`, advance to `provider_selection`
   - `provider_selection` → if `draft.selected_provider_id` is set: call `get_available_slots(provider_id, preferred_date)`, store in `draft.slots`, advance to `slot_selection`
   - `slot_selection` → if `draft.selected_slot_id` is set: advance to `confirmation`
   - `confirmation` → if `draft.confirmed == True`: call `create_appointment(...)`, store result in `draft.appointment`, advance to `completed`
4. **Reply** — call `_llm_reply(session, message)` to generate the assistant's response
5. **Persist** — append `{role: "user", text: message}` and `{role: "assistant", text: reply}` to `session.messages`, save draft + step
6. **Return** — the response dict

## Notes
- Import `search_providers`, `get_available_slots`, `create_appointment` from `agent/tools.py`
- Import `_llm_extract`, `_llm_reply` as private helpers defined in the same file
- Each LLM helper loads its prompts from `agent/prompts.py` which reads `.txt` files at startup
- Use `anthropic.Anthropic()` client initialized from `ANTHROPIC_API_KEY` env var
