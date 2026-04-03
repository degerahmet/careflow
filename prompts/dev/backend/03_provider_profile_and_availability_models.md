# Provider Profile and Availability Models

Add two models to the `providers` Django app for storing provider information and available time slots.

## Model: `ProviderProfile`

- `user` — `OneToOneField` to `AUTH_USER_MODEL`, `on_delete=CASCADE`
- `specialty` — `CharField` with choices:
  - `GEN` General Practice
  - `CARD` Cardiology
  - `DERMA` Dermatology
  - `ENDO` Endocrinology
  - `GAST` Gastroenterology
  - `NEUR` Neurology
  - `PED` Pediatrics
  - `PSY` Psychiatry
  - `RAD` Radiology
  - `SURG` Surgery
- `bio` — `TextField` (can be blank)
- `created_at` — auto timestamp

## Model: `ProviderAvailability`

- `provider` — `ForeignKey` to `ProviderProfile`, `on_delete=CASCADE`, `related_name="availability_slots"`
- `date` — `DateField`
- `start_time`, `end_time` — `TimeField`
- `created_at` — auto timestamp

### Constraints
- `UniqueConstraint` on `(provider, date, start_time, end_time)` — prevent duplicate slots
- Model-level validation: `start_time` must be strictly before `end_time` (raise `ValidationError` in `clean()`)

## Notes
- Register both models in the `providers` app admin
- Add `providers` to `INSTALLED_APPS`
- The signal in `users/models.py` that auto-creates `ProviderProfile` on provider registration should now reference this model
