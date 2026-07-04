# Deployment Guide

## Docker Compose (recommended)

```bash
cp .env.example .env
# Fill in API keys and change POSTGRES_PASSWORD / GRAFANA_PASSWORD in .env
docker compose up --build -d
```

Services:
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API docs**: http://localhost:8000/docs
- **PostgreSQL**: localhost:5432 (direct) / localhost:6432 (via PgBouncer)
- **Redis**: localhost:6379
- **Grafana dashboards**: http://localhost:3001  (default login: admin / admin)
- **Loki** (log ingestion): localhost:3100

---

## Railway

1. Push this repo to GitHub.
2. Create a new Railway project → "Deploy from GitHub Repo".
3. Add a **Redis** service (Railway provides one).
4. Set environment variables in the Railway dashboard (copy from `.env.example`).
5. Railway auto-detects `railway.toml` — the backend will deploy automatically.
6. For the frontend, add a second service pointing to the `frontend/` directory.

---

## Manual (without Docker)

### Backend

```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# Copy and edit env
cp ../.env.example .env

# Start Redis (or set REDIS_URL to an external instance)
redis-server &

# Run API
uvicorn main:app --reload
```

### Frontend

```bash
cd frontend
npm install --legacy-peer-deps
NEXT_PUBLIC_API_URL=http://localhost:8000 npm run dev
```

---

## Environment Variables

| Variable | Description | Default |
|---|---|---|
| `SHODAN_API_KEY` | Shodan API key | — |
| `VIRUSTOTAL_API_KEY` | VirusTotal API key | — |
| `HIBP_API_KEY` | HaveIBeenPwned API key | — |
| `LITELLM_API_KEY` | AI provider API key | — |
| `AI_MODEL` | LiteLLM model string | `gpt-4o-mini` |
| `REDIS_URL` | Redis connection URL | `redis://localhost:6379` |
| `CACHE_TTL` | Cache TTL in seconds | `3600` |
| `CORS_ORIGINS` | Comma-separated allowed origins | `http://localhost:3000` |

---

## Health Check

```bash
curl http://localhost:8000/health
# {"status": "ok"}
```
