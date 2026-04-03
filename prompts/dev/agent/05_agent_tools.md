# Agent Tools

Implement the tool functions used by the booking orchestrator in `backend/agent/tools.py`.

These are deterministic database operations — no LLM calls. The orchestrator calls them at specific state transitions.

## `search_providers(specialty: str) -> list[dict]`

- Query `ProviderProfile.objects.filter(specialty=specialty)`
- Return a list of dicts:
  ```json
  [{ "id": 1, "first_name": "Jane", "last_name": "Smith", "specialty": "CARD", "bio": "..." }]
  ```
- Return an empty list if no providers found

## `get_available_slots(provider_id: int, preferred_date: str | None = None) -> list[dict]`

- Query `ProviderAvailability.objects.filter(provider_id=provider_id)`
- If `preferred_date` is provided (as `YYYY-MM-DD` string), filter to that date only
- Otherwise return all future slots (date >= today)
- Return a list of dicts:
  ```json
  [{ "id": 12, "date": "2025-02-14", "start_time": "09:00", "end_time": "12:00" }]
  ```

## `create_appointment(member, provider_id: int, slot_id: int, reason: str) -> dict`

- Fetch the `ProviderAvailability` slot by `slot_id`
- Create an `Appointment` with:
  - `member` = the authenticated user passed in
  - `provider_id` = provider_id
  - `scheduled_at` = datetime combining `slot.date` + `slot.start_time`
  - `reason` = reason
  - `status` = `"pending"`
- Return a summary dict:
  ```json
  { "id": 5, "scheduled_at": "2025-02-14T09:00:00", "provider_name": "Dr. Jane Smith", "status": "pending" }
  ```

## Notes
- All functions should raise `ValueError` with a clear message if a required record is not found
- Time/date formatting should use `.isoformat()` or `strftime("%H:%M")` for consistent string output
