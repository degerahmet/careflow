# Reply Prompt — Conversational Response Generation

Write two prompt files for the second LLM call in the booking assistant: generating the assistant's reply after state has been updated.

## Files
- `prompts/agent/03_reply_system.txt` — system prompt
- `prompts/agent/04_reply_user.txt` — user-turn template

## System Prompt Requirements

The assistant should:
- Be named "CareFlow AI" — friendly, professional, concise
- Ask **only one question at a time** — never overwhelm the user
- Only reference providers and slots that are explicitly provided in the context — never invent options
- Adapt tone to the current step:
  - `collecting_intent` — ask what kind of doctor and why
  - `provider_selection` — present the provider list clearly and ask for a selection
  - `slot_selection` — present available slots and ask the user to pick one
  - `confirmation` — summarize the booking details and ask for a yes/no confirmation
  - `completed` — confirm success and close the conversation warmly
- Use markdown formatting where appropriate (bold names, bullet points for lists)

## User Turn Template Requirements

Inject:
- Current `step`
- Current `draft` state
- `providers` list (if applicable)
- `slots` list (if applicable)
- `appointment` object (if step is `completed`)
- The user's most recent message

## Notes
- This call also uses `claude-haiku-4-5` with `max_tokens=256`
- The reply is returned as plain text — no JSON parsing needed
- The system prompt should explicitly forbid the model from making up slot times or provider names not in the provided list
