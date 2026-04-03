# OpenAPI Schema Setup

Set up `drf-spectacular` to auto-generate OpenAPI docs from the existing DRF viewsets.

## Requirements

### Installation
- Add `drf-spectacular` to `requirements.txt`
- Add `drf_spectacular` to `INSTALLED_APPS`

### Settings
Add the `SPECTACULAR_SETTINGS` block to `settings.py`:
```python
SPECTACULAR_SETTINGS = {
    "TITLE": "CareFlow API",
    "DESCRIPTION": "AI-powered appointment booking system",
    "VERSION": "1.0.0",
}
```

### URL Routes (in `config/urls.py`)
- `GET /api/schema/` — raw OpenAPI YAML/JSON
- `GET /api/docs/` — Swagger UI
- `GET /api/redoc/` — ReDoc

### DRF Default Renderer
Add to `REST_FRAMEWORK` settings:
```python
"DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
```

### Validation
Run `python manage.py spectacular --validate` to confirm no schema errors after wiring up viewsets.
Use `@extend_schema` from `drf_spectacular.utils` on any viewset action that needs a custom request/response description.
