# API Client

Create a base HTTP client in `src/api/client.js` and separate module files for each domain.

## Base Client (`src/api/client.js`)

- Wraps the native `fetch` API
- Automatically injects `Authorization: Bearer <token>` header from the Pinia auth store
- Sets `Content-Type: application/json` for all requests
- Base URL: `/api` (relies on Vite proxy for dev, or `VITE_API_BASE_URL` for prod builds)
- On `401` response: call `authStore.logout()` and redirect to login
- Export a single function: `request(method, path, body?)` → parsed JSON response

## Domain Modules

### `src/api/auth.js`
- `memberLogin(email, password)`
- `memberSignup(email, password, firstName, lastName)`
- `providerLogin(email, password)`
- `providerSignup(email, password, firstName, lastName)`
- `getMe()`

### `src/api/appointments.js`
- `getMemberAppointments()`
- `getProviderAppointments()`
- `updateAppointmentStatus(id, status)`

### `src/api/provider.js`
- `getMyProfile()`
- `updateMyProfile(data)` — PATCH with `{ specialty, bio }`

### `src/api/availability.js`
- `getMyAvailability()`
- `createAvailabilitySlot(date, startTime, endTime)`
- `deleteAvailabilitySlot(id)`

### `src/api/agent.js`
- `sendMessage(sessionId, message)` — POST to `/api/agent/chat/`
- `getSession(sessionId)` — GET `/api/agent/session/?session_id=...`

## Notes
- Each domain module imports and calls `request()` from `client.js`
- No axios — use native `fetch` only
- All functions return the parsed JSON body directly (not the Response object)
