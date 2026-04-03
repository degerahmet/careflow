# Vue Project Setup

Scaffold the frontend for the CareFlow booking app using Vue 3 + Vite + Nuxt UI.

## Stack
- Vue 3 (Composition API, `<script setup>`)
- Vite 5
- Vue Router 4
- Pinia 3
- `@nuxt/ui` — component library (UButton, UCard, UModal, UInput, USelect, UTextarea, etc.)
- TailwindCSS (included via Nuxt UI)

## Project Structure

```
frontend/src/
├── views/
│   ├── member/
│   └── provider/
├── components/
├── api/
├── stores/
├── constants/
├── router/
│   └── index.js
└── main.js
```

## Router Setup

Define routes in `src/router/index.js`:

| Path | Component | Notes |
|------|-----------|-------|
| `/` | redirect to `/member/login` | |
| `/member/login` | `MemberLoginView` | |
| `/member/signup` | `MemberSignupView` | |
| `/member/dashboard` | `MemberDashboardView` | |
| `/member/chat` | `MemberChatView` | |
| `/provider/login` | `ProviderLoginView` | |
| `/provider/signup` | `ProviderSignupView` | |
| `/provider/dashboard` | `ProviderDashboardView` | |
| `/provider/availability` | `ProviderAvailabilityView` | |

## Vite Proxy

In `vite.config.mjs`, proxy all `/api/*` requests to the Django backend:
```js
server: {
  proxy: {
    '/api': { target: 'http://backend:8000', changeOrigin: true }
  }
}
```

## Notes
- Use `createPinia()` and `createRouter()` in `main.js`
- Nuxt UI requires `@nuxt/ui` plugin registration and a wrapping `<UApp>` in `App.vue`
- All components use `<script setup>` — no Options API
