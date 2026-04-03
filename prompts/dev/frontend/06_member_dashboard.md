# Member Dashboard

Build `MemberDashboardView.vue` — the main page members see after logging in.

## Layout

- Top bar with "CareFlow" branding, member's name, and a Logout button
- "Book Appointment" CTA button (routes to `/member/chat`)
- List of the member's past and upcoming appointments

## Appointment List

Fetch from `GET /api/appointments/member/` on mount.

Each appointment card should display:
- Provider name and specialty
- Scheduled date and time (formatted, e.g. "Mon, Feb 14 · 9:00 AM")
- Appointment reason (truncated if long)
- Status badge — color-coded:
  - `pending` → yellow/warning
  - `confirmed` → green/success
  - `rejected` → red/error
  - `cancelled` → gray
  - `completed` → blue/info

## Empty State

If no appointments, show:
> "No appointments yet. Book your first one!"
> [Book Appointment button]

## Member Actions

- Members can cancel a `pending` appointment — show a "Cancel" button only for pending ones
- Cancellation calls `PATCH /api/appointments/{id}/status/` with `{ status: "cancelled" }` and refreshes the list

## Notes
- Use `UCard`, `UBadge`, `UButton` from Nuxt UI
- Fetch appointments in `onMounted`, use a `ref([])` for the list and a `loading` boolean
- Status badge colors should map from a `constants/` file (`STATUS_COLORS`) — keep the mapping out of the component
