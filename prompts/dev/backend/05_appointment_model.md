# Appointment Model

Create the `Appointment` model in a new `appointments` Django app.

## Model: `Appointment`

- `member` — `ForeignKey` to `AUTH_USER_MODEL`, `on_delete=CASCADE`, `related_name="appointments"`
- `provider` — `ForeignKey` to `ProviderProfile`, `on_delete=CASCADE`, `related_name="appointments"`
- `scheduled_at` — `DateTimeField` (the confirmed date/time of the appointment)
- `reason` — `TextField` (member's stated reason for the visit)
- `status` — `TextChoices`:
  - `pending` — default, waiting for provider action
  - `confirmed` — provider accepted
  - `rejected` — provider declined
  - `cancelled` — member cancelled
  - `completed` — visit completed
- `ai_summary` — `TextField`, `blank=True`, `null=True` (populated by AI later)
- `created_at`, `updated_at` — auto timestamps

## Notes
- Default `status` is `"pending"`
- Add `appointments` to `INSTALLED_APPS`
- Register in Django admin with:
  - List display: member name, provider name, scheduled_at, status
  - Filters: status, provider
  - A collapsed "AI" fieldset for `ai_summary`
