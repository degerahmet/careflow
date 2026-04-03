# Provider Dashboard

Build `ProviderDashboardView.vue` — the main page providers see after logging in.

## Layout

- Left sidebar (`ProviderSidebar` component) with navigation links and logout
- Main content area showing the provider's incoming appointments

## Sidebar Links
- Dashboard → `/provider/dashboard`
- Manage Availability → `/provider/availability`
- Logout

## Appointment List

Fetch from `GET /api/appointments/provider/` on mount.

Each appointment card should display:
- Member's full name
- Reason for visit
- Scheduled date/time
- Status badge (same color mapping as member dashboard)
- Action buttons for `pending` appointments:
  - "Confirm" → calls `PATCH /api/appointments/{id}/status/` with `{ status: "confirmed" }`
  - "Reject" → calls `PATCH /api/appointments/{id}/status/` with `{ status: "rejected" }`
  - After either action, refresh the list

## Tabs (optional)
Optionally segment the list by status: "Pending", "Upcoming" (confirmed), "Past" (completed/rejected/cancelled).

## Onboarding Guard

If the provider's profile is missing `specialty` or `bio`, show the `ProviderOnboardingModal` immediately on mount and block the rest of the UI until it's completed.

Check profile completeness by calling `GET /api/provider/profile` in `onMounted`.

## Notes
- Use `UCard`, `UBadge`, `UButton` from Nuxt UI
- `loading` and `error` states should be handled gracefully
- Confirm/Reject buttons should show a loading state while the API call is in-flight
