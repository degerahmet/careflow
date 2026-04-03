# Provider Onboarding Modal

Create `src/components/ProviderOnboardingModal.vue` — a forced onboarding flow shown to providers who have not yet completed their profile.

## Trigger

The modal is shown from `ProviderDashboardView` when `getMyProfile()` returns a profile with an empty `specialty` or `bio`.

It should be non-dismissable — the provider cannot close it without completing the form.

## Form Fields

- `Specialty` — dropdown (`USelect`) with the full list of specialties:
  - General Practice, Cardiology, Dermatology, Endocrinology, Gastroenterology, Neurology, Pediatrics, Psychiatry, Radiology, Surgery
  - Values should be the backend codes (GEN, CARD, etc.) from a `constants/specialties.js` file
- `Bio` — textarea, minimum 20 characters, describes the provider's background

## Submission

On submit:
- Call `updateMyProfile({ specialty, bio })` (PATCH to `/api/provider/profile`)
- On success: emit `"completed"` event to the parent, which then hides the modal and loads the dashboard
- Show error if submission fails

## UI
- Use `UModal` from Nuxt UI with `:prevent-close="true"` to block dismissal
- Title: "Complete Your Profile"
- Subtitle: "Before you can start seeing appointments, we need a few more details."
- Submit button: "Save and Continue"

## Notes
- Specialty options should be imported from `src/constants/specialties.js` — not hardcoded in the component
- Keep modal width reasonable (~500px max) — it's a simple two-field form
- After the modal is completed, the parent should re-fetch the profile to confirm the update before hiding the modal
