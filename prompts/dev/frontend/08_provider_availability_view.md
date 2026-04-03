# Provider Availability View

Build `ProviderAvailabilityView.vue` so providers can manage their available time slots.

## Layout

- Left sidebar (reuse `ProviderSidebar`)
- Main area with two sections:
  1. "Add Availability" form
  2. "Your Availability" list

## Add Availability Form

Fields:
- `Date` — date picker input (`type="date"`)
- `Start Time` — time input (`type="time"`)
- `End Time` — time input (`type="time"`)
- Submit button: "Add Slot"

On submit:
- Call `createAvailabilitySlot(date, startTime, endTime)` from `src/api/availability.js`
- On success: clear the form and refresh the slot list
- Show an error if `start_time >= end_time` (validate client-side before submitting)

## Availability List

Fetch from `GET /api/availability/` on mount.

Each slot row displays:
- Date (formatted)
- Start time → End time (e.g., "09:00 → 12:00")
- Delete button (trash icon or "Remove")

On delete: call `deleteAvailabilitySlot(id)`, then refresh the list.

## Empty State

If no slots: "You haven't added any availability yet."

## Notes
- Use `UCard`, `UInput`, `UButton`, `UTable` or a simple list from Nuxt UI
- List should be sorted by date ascending
- No pagination needed — providers typically have a small number of slots
