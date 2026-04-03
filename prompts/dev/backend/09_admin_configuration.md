# Django Admin Configuration

Customize the Django admin interface for all models in the CareFlow project.

## Users App

`UserAdmin`:
- List display: `email`, `first_name`, `last_name`, `role`, `is_active`, `created_at`
- Search: `email`, `first_name`, `last_name`
- Filters: `role`, `is_active`

## Providers App

`ProviderAvailabilityInline` (TabularInline):
- Model: `ProviderAvailability`
- Extra: 1 blank row
- Fields: `date`, `start_time`, `end_time`

`ProviderProfileAdmin`:
- List display: provider's full name, `specialty`, `created_at`
- Include `ProviderAvailabilityInline`
- Search: provider user's email and name
- Filter: `specialty`

## Appointments App

`AppointmentAdmin`:
- List display: member name, provider name, `scheduled_at`, `status`, `created_at`
- Filters: `status`, `provider`
- Search: member email, provider email
- Fieldsets:
  - Default: `member`, `provider`, `scheduled_at`, `reason`, `status`
  - Collapsible "AI" section: `ai_summary`

## Notes
- Use `readonly_fields` for timestamp fields (`created_at`, `updated_at`)
- The inline styles should use CSS custom properties (`var(--body-fg)`, `var(--body-bg)`) for light/dark theme compatibility in the Django admin — do not hardcode hex colors
