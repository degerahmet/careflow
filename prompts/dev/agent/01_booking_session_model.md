# Booking Session Model

Create a `BookingSession` model in a new `agent` Django app to persist the state of AI-driven booking conversations.

## Model: `BookingSession`

- `session_id` — `UUIDField`, `default=uuid.uuid4`, `db_index=True` (used as the public session identifier)
- `member` — `ForeignKey` to `AUTH_USER_MODEL`, `on_delete=CASCADE`
- `step` — `TextChoices` representing the current stage of the booking flow:
  - `collecting_intent` — waiting for specialty and reason
  - `provider_selection` — showing provider list, waiting for selection
  - `slot_selection` — showing slots, waiting for selection
  - `confirmation` — reviewing booking details, waiting for confirmation
  - `completed` — appointment booked
- `draft` — `JSONField`, default `{}` — stores in-progress booking data:
  - `specialty`, `reason`, `preferred_date`
  - `selected_provider_id`, `selected_slot_id`
  - `providers` (list), `slots` (list), `appointment` (final object)
- `messages` — `JSONField`, default `[]` — chat history as `[{role, text}]`
- `created_at`, `updated_at` — auto timestamps

## Notes
- Add `agent` to `INSTALLED_APPS`
- Default `step` is `"collecting_intent"`
- Register in admin with list display: `session_id`, `member`, `step`, `updated_at`
