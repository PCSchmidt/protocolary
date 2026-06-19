# DEPLOYMENT_CONFIG.md — Transcelerate | Environment Configuration
# POC scope: local Docker Compose only. Cloud deployment is post-POC.

## Services

| Service | Image | Port (local) | Purpose |
|---|---|---|---|
| MongoDB | `mongo:7` | 27017 | Primary datastore for USDM study definitions |
| MongoDB (test) | `mongo:7` | 27018 | Isolated test database (test Docker profile) |
| FastAPI | local build | 8000 | REST API |
| Streamlit | local build | 8501 | Demo dashboard (Gate 4) |

Redis/Celery are not currently required. Add them only if measured transformation time justifies
background jobs; deterministic Gate 3A transformations should remain synchronous for the POC.

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

# CDISC Library API (optional for this POC; COSMoS data is sourced from GitHub)
CDISC_API_KEY=your_key_here

# Pinned local COSMoS snapshot/export used by Gate 3A
COSMOS_DATA_PATH=app/data/cosmos
COSMOS_SOURCE_COMMIT=fc11c9dbdc12aae709653b45c4c9db7f58824cf5

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
# Start dev environment (MongoDB + API)
docker compose up -d

# Start with test database included
docker compose --profile test up -d

# Run tests from python/
cd python
python -m pytest -v

# View API docs
open http://localhost:8000/docs

# View Streamlit dashboard (Gate 4+)
streamlit run python/streamlit_app.py
```

## Common Failure Modes

| Symptom | Cause | Fix |
|---|---|---|
| `motor.errors.ServerSelectionTimeoutError` | MongoDB not running | `docker compose up -d mongo` |
| COSMoS lookup unavailable | Snapshot missing or path incorrect | Refresh/pin the approved snapshot; tests must not fetch live data |
| REDCap 403 | Invalid API token | Verify token in REDCap sandbox settings |
| `usdm` ImportError | Wrong Python version | Requires Python >= 3.12 |
| Port 8000 in use | Another process on port | `lsof -i :8000` → kill or change `API_PORT` |
| Settings validation fails for `DEBUG` | Host environment contains a non-boolean `DEBUG` value | Run with `DEBUG=false` or use a project-specific environment variable |

## REDCap Sandbox Setup

1. Request a sandbox account at https://projectredcap.org (free for research/testing)
2. Create a new project (use "Practice / Just for fun" type)
3. Enable API access: Project Setup → API → Enable
4. Generate API token: API → Generate Token
5. Copy token to `.env` as `REDCAP_API_TOKEN`
6. Note project ID from the URL (`?pid=XXXXX`) → `REDCAP_PROJECT_ID`

REDCap availability and API-token provisioning are institution-specific. The project is currently
awaiting JHU ICTR access. This blocks Gate 3B only.

## CDISC API Key Setup

1. Register at https://www.cdisc.org (free account)
2. Request API key from the CDISC Library API section
3. Copy key to `.env` as `CDISC_API_KEY`

The free developer-portal key does not grant access to members-only COSMoS data. Gate 3A uses a
version-pinned snapshot from [cdisc-org/COSMoS](https://github.com/cdisc-org/COSMoS), so the key is
optional for the POC's normal build and test path.

## Protocol Explorer Fixture Refresh

Protocol Explorer currently provides public per-protocol JSON downloads rather than a documented
bulk API. Fixture refresh must therefore be an explicit, reviewable operation:

1. Select the protocol in the browser.
2. Download its JSON and associated CORE report.
3. Record provenance and checksum in the fixture manifest.
4. Validate with the pinned `usdm` package.
5. Commit only the deliberately selected fixture or a minimized derivative with attribution.

Do not download fixtures dynamically during application startup or test execution.
