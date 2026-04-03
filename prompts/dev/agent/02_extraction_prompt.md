# Extraction Prompt — Intent Parsing

Write two prompt files for the first LLM call in the booking assistant pipeline: extracting structured intent from a user's natural language message.

## Files
- `prompts/agent/01_extraction_system.txt` — system prompt
- `prompts/agent/02_extraction_user.txt` — user-turn template (uses placeholders)

## System Prompt Requirements

The model should:
- Return a **single JSON object only** — no prose, no explanation
- Extract the following fields from the user's message (all optional, use `null` if not present):
  - `specialty` — one of the valid specialty codes (GEN, CARD, DERMA, ENDO, GAST, NEUR, PED, PSY, RAD, SURG)
  - `reason` — the patient's stated reason for the appointment
  - `preferred_date` — in `YYYY-MM-DD` format if mentioned
  - `selected_provider_id` — integer ID if the user selected a provider
  - `selected_slot_id` — integer ID if the user selected a slot
  - `confirmed` — boolean, `true` only if the user explicitly confirms the booking

## User Turn Template Requirements

The template should inject:
- Today's date (for resolving relative dates like "next Monday")
- Current `draft` state (so the model knows what's already collected)
- Available `providers` list (if in provider_selection step)
- Available `slots` list (if in slot_selection step)
- The user's message

Format the output as a clean prompt — not raw JSON dumps. Label each section clearly.

## Notes
- These files are loaded at runtime by `backend/agent/prompts.py` using `Path(__file__).parent / "prompts" / filename`
- The extraction call uses `claude-haiku-4-5` with `max_tokens=256`
- The response is parsed with `json.loads()` — malformed output should be caught and default to an empty dict
