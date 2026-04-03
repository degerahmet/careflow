# Environment Configuration

Create a `.env.example` file for a Django + Vue + PostgreSQL project running inside Docker.

## Required Variables

### Django
- `DJANGO_SECRET_KEY` — long random string, placeholder value is fine
- `DJANGO_DEBUG` — set to `True` for development

### PostgreSQL
- `POSTGRES_DB` — database name (`careflow`)
- `POSTGRES_USER` — db user (`careflow_user`)
- `POSTGRES_PASSWORD` — db password, use a placeholder

### AI
- `ANTHROPIC_API_KEY` — API key for Claude, placeholder `your-key-here`

### Frontend
- `VITE_API_BASE_URL` — base URL used by the frontend at build time (`http://localhost:8000`)

## Notes
- All Django settings should use `python-decouple` to read from environment variables — no hardcoded config in `settings.py`
- The actual `.env` file should be in `.gitignore`; only `.env.example` is committed
- The Vite proxy (`/api/*` → `http://backend:8000`) uses Docker's internal DNS, so `VITE_API_BASE_URL` is only needed for direct API calls, not proxied ones
