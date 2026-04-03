# Appointment Endpoints

Add REST endpoints so members can book appointments and providers can view and manage them.

## Endpoints

### Member
- `POST /api/appointments/` — create a new appointment (member only)
  - Body: `{ provider_id, scheduled_at, reason }`
  - Sets `member` from the authenticated user, `status` defaults to `"pending"`
- `GET /api/appointments/member/` — list all of the authenticated member's appointments
  - Include provider name, specialty, scheduled_at, status

### Provider
- `GET /api/appointments/provider/` — list all appointments for the authenticated provider
  - Include member name, reason, scheduled_at, status
- `PATCH /api/appointments/{id}/status/` — update appointment status (provider only)
  - Allowed transitions: `pending → confirmed`, `pending → rejected`
  - Return `400` if the transition is invalid or the appointment doesn't belong to this provider

## Permissions
- Use the `IsMember` and `IsProvider` custom permission classes from `providers/permissions.py`
- All endpoints require `IsAuthenticated`

## Serializers
- `AppointmentCreateSerializer` — for `POST`, validates `provider_id` exists
- `AppointmentReadSerializer` — for `GET`, nested provider/member info, includes status display label
- `AppointmentStatusSerializer` — for `PATCH /status/`, validates allowed status values

## Router
Register `AppointmentViewSet` on the `DefaultRouter` in `backend/config/urls.py`.
Use custom actions (`@action`) for the member/provider list views and the status update.
