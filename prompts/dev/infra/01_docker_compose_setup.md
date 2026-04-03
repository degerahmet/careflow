# Docker Compose Setup

Set up a Docker Compose environment for a full-stack web app with the following services:

## Services

### db
- Image: `postgres:16`
- Environment variables: `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD` (all from `.env`)
- Named volume: `postgres_data` mounted at `/var/lib/postgresql/data`
- Healthcheck using `pg_isready` so dependent services wait for the database to be ready

### backend
- Build from `./backend/Dockerfile`
- Python/Django app running on port `8000`
- Mount `./backend` as `/app` and `./prompts` as `/app/prompts` (for AI prompt files)
- Depends on `db` with a healthcheck condition
- Passes all env vars from `.env`: Django config, Postgres credentials, `ANTHROPIC_API_KEY`
- Command: `python manage.py runserver 0.0.0.0:8000`

### frontend
- Build from `./frontend/Dockerfile`
- Node/Vite dev server on port `5173`
- Mount `./frontend` as `/app` for hot reload
- Pass `VITE_API_BASE_URL` from `.env`
- Command: `npm run dev`

## Requirements
- Use `env_file: .env` for all services
- `postgres_data` should be declared as a named volume at the bottom
- Services should only expose the ports listed above
- Backend Dockerfile should use an `entrypoint.sh` that runs migrations before starting the server
