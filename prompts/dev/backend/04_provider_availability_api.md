# Provider Availability API

Expose API endpoints so providers can manage their availability slots and members can view a provider's open slots.

## Endpoints

### Provider-facing (authenticated, role=provider)
- `GET /api/availability/` — list the authenticated provider's own slots
- `POST /api/availability/` — create a new availability slot
- `DELETE /api/availability/{id}/` — delete a slot (only if it belongs to the authenticated provider)

### Public / Member-facing
- `GET /api/providers/` — list all providers (id, name, specialty, bio)
- `GET /api/providers/{id}/` — detail for a single provider
- `GET /api/providers/{id}/availability/` — list open availability slots for a given provider

## Permissions

Create two custom permission classes in `backend/providers/permissions.py`:
- `IsMember` — allows access only if `request.user.role == "member"`
- `IsProvider` — allows access only if `request.user.role == "provider"`

Use `IsProvider` for slot management endpoints and `IsAuthenticated | AllowAny` for read-only provider listing.

## Serializers
- `ProviderProfileSerializer` — includes `user` name fields, `specialty`, `bio`
- `ProviderAvailabilitySerializer` — includes `id`, `date`, `start_time`, `end_time`

## Router
Register `ProviderViewSet` and `AvailabilityViewSet` on the `DefaultRouter` in `backend/config/urls.py`.
The availability viewset should use `basename="availability"`.
