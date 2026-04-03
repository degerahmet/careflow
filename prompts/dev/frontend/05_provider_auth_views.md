# Provider Auth Views

Build the login and signup pages for providers. These mirror the member auth views in layout but route to the provider dashboard and have a different signup flow.

## `ProviderLoginView.vue`

- Same centered card layout as member login
- Form fields: `Email`, `Password`
- On success: call `authStore.login(...)` then navigate to `/provider/dashboard`
- Link: "Don't have an account? Sign up" → `/provider/signup`
- Link: "Are you a member? Log in here" → `/member/login`

## `ProviderSignupView.vue`

- Form fields: `First Name`, `Last Name`, `Email`, `Password`
- On success: auto-login and navigate to `/provider/dashboard`
- Note: providers complete their profile (specialty + bio) via a modal on the dashboard — no specialty field here

## Post-Login Behavior

After provider login or signup:
- Check if the provider's profile is complete (has `specialty` and `bio`)
- If incomplete, trigger the `ProviderOnboardingModal` (which is rendered in `ProviderDashboardView`)
- The dashboard should guard against rendering appointment data until onboarding is complete

## Style Notes
- Reuse the same card/form pattern from member auth views
- The provider auth pages should clearly indicate they're for healthcare providers (subtitle text or label)
