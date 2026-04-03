# Member Auth Views

Build the login and signup pages for members using Vue 3 + Nuxt UI.

## `MemberLoginView.vue`

- Centered card layout with "CareFlow" branding
- Form fields: `Email`, `Password`
- Submit button: "Sign In"
- On success: call `authStore.login(...)` then navigate to `/member/dashboard`
- Show error message if credentials are invalid
- Link at the bottom: "Don't have an account? Sign up" → `/member/signup`
- Link to provider login: "Are you a provider? Log in here" → `/provider/login`

## `MemberSignupView.vue`

- Same card layout
- Form fields: `First Name`, `Last Name`, `Email`, `Password`
- Submit button: "Create Account"
- On success: auto-login (use the tokens returned from signup) and navigate to `/member/dashboard`
- Show field-level or general error on failure
- Link: "Already have an account? Log in" → `/member/login`

## Style Notes
- Use `UCard`, `UInput`, `UButton` from Nuxt UI
- Card should be max-width ~400px, centered on the page with a full-height flex container
- Use `UAlert` or a simple `<p>` with a red text color for error display
- Inputs should have clear labels above them, not just placeholder text
