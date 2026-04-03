# Custom User Model

Create a custom Django user model for a healthcare booking app that supports two user roles.

## Requirements

### Model: `User`
- Extend `AbstractBaseUser` and `PermissionsMixin`
- Use `email` as the unique identifier instead of `username` — remove the `username` field entirely
- Fields:
  - `email` (unique)
  - `first_name`, `last_name`
  - `role` — `TextChoices` with values: `"member"` and `"provider"` (admin users are handled via `is_staff`)
  - `is_active`, `is_staff` — standard Django flags
  - `created_at` — auto-set on creation

### Manager: `CustomUserManager`
- Override `create_user(email, password, **extra_fields)`
- Override `create_superuser(...)` — sets `is_staff=True`, `is_superuser=True`
- Normalize email before saving

### Settings
- Register as `AUTH_USER_MODEL = "users.User"` in `settings.py`
- Add `users` to `INSTALLED_APPS`

### Signal
- When a new user with `role="provider"` is created, automatically create a linked `ProviderProfile` via a `post_save` signal (stub — ProviderProfile model will be added later)

## App
Place in a Django app called `users` inside `backend/`.
