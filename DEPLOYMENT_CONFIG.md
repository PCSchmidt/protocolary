# DEPLOYMENT_CONFIG.md — Transcelerate | Environment Configuration
# POC scope: local Docker Compose only. Cloud deployment is post-POC.

## Services

| Service | Image | Port (local) | Purpose |
|---|---|---|---|
| MongoDB | `mongo:7` | 27017 | Primary datastore for USDM study definitions |
| MongoDB (test) | `mongo:7` | 27018 | Isolated test database (test Docker profile) |
| Redis | `redis:7-alpine` | 6379 | Celery broker (Gate 3+, async transform jobs) |
| FastAPI | local build | 8000 | REST API |
| Streamlit | local build | 8501 | Demo dashboard (Gate 4) |

## Environment Variables

Create `.env` in the `python/` directory (`.env` is in `.gitignore` — never commit it).
Copy `.env.example` and fill in values.

```bash
# MongoDB
MONGO_URL=mongodb://localhost:27017
MONGO_DB_NAME=transcelerate

# MongoDB (test)
MONGO_TEST_URL=mongodb://localhost:27018
MONGO_TEST_DB_NAME=transcelerate_test

# Redis (Gate 3+)
REDIS_URL=redis://localhost:6379

# CDISC Terminology API (required by usdm package)
# Request a key at: https://www.cdisc.org/cdisc-api
CDISC_API_KEY=your_key_here

# REDCap (Gate 3+)
# Obtain from your REDCap sandbox instance
REDCAP_URL=https://your-redcap-instance.org
REDCAP_API_TOKEN=your_token_here
REDCAP_PROJECT_ID=your_project_id

# FastAPI
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=true
```

## Docker Compose Quick Start

```bash
# Start dev environment (MongoDB + Redis + API)
docker compose up -d

# Start with test database included
docker compose --profile test up -d

# Run tests
pytest python/tests/

# View API docs
open http://localhost:8000/docs

# View Streamlit dashboard (Gate 4+)
streamlit run python/streamlit_app.py
```

## Common Failure Modes

| Symptom | Cause | Fix |
|---|---|---|
| `motor.errors.ServerSelectionTimeoutError` | MongoDB not running | `docker compose up -d mongo` |
| `KeyError: CDISC_API_KEY` | Missing env var | Add to `.env`; restart API container |
| REDCap 403 | Invalid API token | Verify token in REDCap sandbox settings |
| `usdm` ImportError | Wrong Python version | Requires Python >= 3.12 |
| Port 8000 in use | Another process on port | `lsof -i :8000` → kill or change `API_PORT` |

## REDCap Sandbox Setup

1. Request a sandbox account at https://projectredcap.org (free for research/testing)
2. Create a new project (use "Practice / Just for fun" type)
3. Enable API access: Project Setup → API → Enable
4. Generate API token: API → Generate Token
5. Copy token to `.env` as `REDCAP_API_TOKEN`
6. Note project ID from the URL (`?pid=XXXXX`) → `REDCAP_PROJECT_ID`

Sandbox provisioning typically takes 1–2 business days.

## CDISC API Key Setup

1. Register at https://www.cdisc.org (free account)
2. Request API key from the CDISC Library API section
3. Copy key to `.env` as `CDISC_API_KEY`

This key is needed by the `usdm` package for terminology code validation.
