# FARKINDA AI v2.0 — Living Home Intelligence

A working **local demonstration** of cross-domain household awareness: pet meal trends, inventory depletion, food-expiry signals and explainable action plans.

## Quick start (Python 3.10+; no pip dependencies)

```powershell
python app.py
```

Open http://127.0.0.1:8765 . Data is stored in `home.db` in the project directory. Remove this file to reset sample data. Set `FARKINDA_PORT` to change the port.

## Test

```powershell
python -m unittest discover -p 'test_*.py' -v
```

## HTTP endpoints

- `GET /api/health` — truthful capabilities
- `GET /api/status` — inventory, pet trends and evidence
- `GET /api/forecast` — stock depletion and expiry forecast
- `GET /api/plan?away=1` — combined plan
- `POST /api/simulate` — deterministic English intent simulator
- `POST /api/event` — manual confirmed stock consumption/restock
- `GET /api/history` — event/action audit trail
- `POST /api/meal` — confirmed meal record
- `POST /api/action` — confirmed **local-only** approval
- `POST /mcp` — limited JSON-RPC MCP-style tools (not externally certified Alexa integration)

Example stock event:
```json
{"kind":"consume","subject":"Süt","quantity":100,"confirmed":true}
```

Optional `FARKINDA_WRITE_TOKEN` environment variable protects write operations using the `X-Farkinda-Token` header. If enabled, the demo UI needs this header added for writes. Do **not** expose this development server publicly. It has no multi-user accounts, rate limiting, TLS, or complete MCP session/transport conformance.

## Competition readiness

- Working: local web UI, sample SQLite data, deterministic cross-domain planning, inventory forecast, explicit confirmations, event journal, MCP-style tool dispatch, tests.
- Not implemented: Amazon Alexa+ device connection, remote HTTPS deployment, live sensor integration, AI model, real orders, automatic notifications, Devpost submission, public GitHub repository, demo video.
- Pet meal deviations are **not** a medical diagnosis. Date warnings are not a guarantee of food safety.

## Demo flow (2–3 minutes)

1. Open the dashboard and explain the three evidence sources.
2. Ask: “Nobody will be home tomorrow. What should I take care of?”
3. Show the combined pet-care, inventory and food-waste action plan.
4. Record a confirmed stock consumption event; refresh the forecast.
5. Approve one local demo action and explain that no purchase was made.
6. Show `tools/list` via the MCP-style endpoint and discuss limitations accurately.
