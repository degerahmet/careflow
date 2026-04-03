# JWT Auth Endpoints

Add authentication endpoints for the CareFlow booking app. Members and providers have separate login/signup flows.

## Endpoints

### Member
- `POST /api/auth/member/register/` — create a new member account
- `POST /api/auth/member/login/` — login and return JWT tokens

### Provider
- `POST /api/auth/provider/register/` — create a new provider account
- `POST /api/auth/provider/login/` — login and return JWT tokens

### Shared
- `GET /api/auth/me/` — return the authenticated user's profile (requires Bearer token)

## Implementation Notes

- Use `djangorestframework-simplejwt` for token generation
- Register/login views are plain `APIView` subclasses, not viewsets
- JWT config in `settings.py`:
  - Access token lifetime: 1 hour
  - Refresh token lifetime: 7 days
- Register/login return both `access` and `refresh` tokens plus the user object (`id`, `email`, `first_name`, `last_name`, `role`)
- `/api/auth/me/` uses `IsAuthenticated` permission and returns the same user fields
- Wire all auth URLs through `backend/users/urls.py` and include in `backend/config/urls.py` under `api/auth/`

## Serializers
- `UserRegistrationSerializer` — validates email uniqueness, hashes password
- `UserLoginSerializer` — validates credentials, returns tokens + user data
- `UserSerializer` — read-only, used for `/me/`
