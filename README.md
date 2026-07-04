# OmniTrace – Ultimate Ethical OSINT SaaS

> Powerful, AI-enhanced Open Source Intelligence platform. Search names, IPs, domains, phones, usernames — aggregate public data from Shodan, VirusTotal, and more with parallel processing, caching, and intelligent AI summaries.

## Features

| Feature | Details |
|---|---|
| 🔍 **Universal search** | Auto-detects IP, domain, email, hash, phone, username |
| ⚡ **Parallel async** | All integrations fire simultaneously via `asyncio.gather` |
| 🌐 **Shodan** | Open ports, vulns, hostnames, ISP, geolocation |
| 🦠 **VirusTotal** | Malware/reputation analysis for IPs, domains, hashes |
| 📡 **DNS** | A, AAAA, MX, NS, TXT, CNAME via Cloudflare DoH |
| 📋 **WHOIS** | Registrar, creation date, name servers |
| 🔓 **HIBP** | Email breach history (HaveIBeenPwned) |
| 🧠 **AI Summary** | LiteLLM — works with OpenAI, Anthropic, Ollama, etc. |
| ⚡ **Redis cache** | 1-hour TTL, graceful fallback if Redis unavailable |
| 🚦 **Rate limiting** | 60 req/min per IP via SlowAPI |
| 🎨 **Next.js UI** | Dark dashboard with Recharts visualizations |
| 🐳 **Docker** | One-command `docker compose up --build` |
| 🚀 **Railway** | Ready-to-deploy `railway.toml` |
| 🔁 **CI/CD** | GitHub Actions — lint, type-check, build |

## Quick Start

```bash
# 1. Clone and copy env
git clone https://github.com/your-org/omnitrace
cd omnitrace
cp .env.example .env
# Edit .env and add your API keys

# 2. Start everything
docker compose up --build
```

Open **http://localhost:3000** for the dashboard, **http://localhost:8000/docs** for the API.

## API Keys

| Service | Env Var | Required? | Free tier |
|---|---|---|---|
| Shodan | `SHODAN_API_KEY` | Optional | $49/mo (free demo available) |
| VirusTotal | `VIRUSTOTAL_API_KEY` | Optional | Yes — 4 req/min |
| HIBP | `HIBP_API_KEY` | Optional | ~$3.50/mo |
| LiteLLM | `LITELLM_API_KEY` | Optional | Depends on provider |

All integrations degrade gracefully — missing keys simply skip that source.

## API Usage

```bash
# Search any query — type is auto-detected
curl -X POST http://localhost:8000/api/search \
  -H "Content-Type: application/json" \
  -d '{"query": "8.8.8.8"}'

# Force a specific type
curl -X POST http://localhost:8000/api/search \
  -H "Content-Type: application/json" \
  -d '{"query": "example.com", "force_type": "domain"}'
```

## Project Structure

```
.
├── backend/          # FastAPI Python backend
│   ├── app/
│   │   ├── integrations/   # Shodan, VirusTotal, DNS, WHOIS, HIBP
│   │   ├── config.py       # Settings (pydantic-settings)
│   │   ├── detector.py     # Query type auto-detection
│   │   ├── cache.py        # Redis async cache
│   │   ├── ai.py           # LiteLLM AI summary
│   │   └── router.py       # FastAPI routes
│   └── main.py
├── frontend/         # Next.js 14 TypeScript dashboard
│   ├── app/
│   └── components/
├── docker-compose.yml
├── railway.toml
└── .github/workflows/ci.yml
```

## Deploy

See [DEPLOY.md](./DEPLOY.md) for full deployment instructions (Docker, Railway, manual).

## Legal

OmniTrace queries **publicly available data only**. You are responsible for complying with the terms of service of each integrated data source and applicable laws in your jurisdiction. Use responsibly and ethically.
