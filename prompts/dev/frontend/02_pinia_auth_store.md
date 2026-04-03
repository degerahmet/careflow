# Pinia Auth Store

Implement a Pinia store in `src/stores/auth.js` to manage authentication state across the app.

## State

```js
{
  accessToken: null,   // JWT access token (string | null)
  refreshToken: null,  // JWT refresh token (string | null)
  user: null           // { id, email, first_name, last_name, role }
}
```

## Actions

- `login(accessToken, refreshToken, user)` — set all three state fields and persist to `localStorage`
- `logout()` — clear state and `localStorage`, redirect to the appropriate login page based on prior role
- `loadFromStorage()` — on app init, rehydrate state from `localStorage` if tokens exist

## Getters

- `isAuthenticated` — `true` if `accessToken` is non-null
- `isProvider` — `true` if `user?.role === "provider"`
- `isMember` — `true` if `user?.role === "member"`

## localStorage Keys
- `"access_token"`, `"refresh_token"`, `"user"` (JSON stringified)

## Notes
- Call `loadFromStorage()` in `App.vue` or `main.js` on startup
- The API client (`src/api/client.js`) should import this store to read `accessToken` for the `Authorization` header — do not duplicate token storage
- No token refresh logic needed for now — expired tokens redirect to login
