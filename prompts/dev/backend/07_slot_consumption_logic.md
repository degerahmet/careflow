# Slot Consumption on Appointment Confirmation

When a provider confirms an appointment, the corresponding availability slot should be consumed. Appointments are 30 minutes long, so a single slot may need to be split.

## Behavior

When `PATCH /api/appointments/{id}/status/` sets `status = "confirmed"`:

1. Find the `ProviderAvailability` slot that contains `appointment.scheduled_at`
   - Match on `provider`, `date`, and `start_time <= scheduled_at.time() < end_time`
2. Delete the matched slot
3. If the slot starts before the appointment time, re-create a new slot from `slot.start_time` to `appointment.time`
4. If the slot ends after `appointment.time + 30 minutes`, re-create a new slot from `appointment.time + 30 min` to `slot.end_time`

This simulates consuming exactly 30 minutes from a larger availability window.

## Notes
- Wrap this logic in a helper function `consume_slot(appointment)` called inside the status update view
- Use `datetime.timedelta(minutes=30)` for the appointment duration
- If no matching slot is found, still confirm the appointment — don't block on missing availability (the slot may have been manually removed)
- All slot changes should happen atomically with the status update — wrap in `transaction.atomic()`
