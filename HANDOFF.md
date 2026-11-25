# Handoff — Deploy CONNECT. (Vercel + LiveKit Cloud)

**Owner:** Lucky John Faderon, AI Solutions Architect · **Repo:** github.com/dudezki/contact-center-demo (`main`)
**State at handoff:** MVP works locally (web :5199, API :8000, agent worker registered with LiveKit Cloud).
Read `README.md` (setup, security) and `PROGRESS.md` (what is verified) first.

## 1. Goal
Publicly reachable site where a visitor presses **Start a conversation** and talks to the AI agent,
with secrets server-side and free-tier costs bounded (60 s calls, rate limits).

## 2. Target architecture
| Part | Where | Why |
|---|---|---|
| `web/` (Vue static build) | **Vercel project A** (root `web`) | static + CDN |
| `backend/app` (FastAPI `/api/token`) | **Vercel project B** (root `backend`), Python function | short request/response — fits serverless |
| `backend/agent` (LiveKit worker) | **LiveKit Cloud Agents** (`lk agent create`) — or Render/Fly/Railway | long-lived WebSocket process; **cannot run on Vercel** |

Browser → `https://<site>/api/token` (rewrite to project B, same origin, no CORS) → LiveKit Cloud ← agent.

## 3. Blockers to fix before deploying (do these in order)
1. **Split Python dependencies.** `backend/pyproject.toml` installs `livekit-agents` + Silero/turn-detector
   models for both services. That will exceed Vercel's Python function size limit (~250 MB unzipped).
   Give the API its own minimal deps (`fastapi`, `pydantic-settings`, `livekit-api`) — e.g. a
   `backend/requirements.txt` used by Vercel, keep `pyproject.toml` for the agent. Confirm the current limit
   in Vercel docs.
2. **Vercel FastAPI entrypoint.** `app/main.py` exposes a factory (`create_app`). Vercel needs a module-level
   ASGI `app`. Add `backend/api/index.py` (or the entry path Vercel's current FastAPI docs require):
   `from app.main import create_app; app = create_app()`. Check Vercel's FastAPI docs for current
   zero-config detection rules and the Python runtime version (project uses 3.12/3.13).
3. **Rate limiting is in-memory** (`app/ratelimit.py`) — on serverless each instance has its own memory, so
   limits become ineffective. Replace with a shared store (Upstash Redis via Vercel Marketplace) behind the
   same `check(key) -> wait_seconds` interface; keep the existing tests passing with an in-memory fake.
4. **Client IP:** on Vercel set `TRUST_PROXY_HEADERS=true` (Vercel sets `x-forwarded-for`). Only on Vercel.
5. **SPA/API routing:** add `web/vercel.json`, e.g.
   `{"rewrites":[{"source":"/api/(.*)","destination":"https://<api-project>.vercel.app/api/$1"}]}`
   so the browser stays same-origin (frontend already calls relative `/api`). Alternatively set
   `VITE_API_BASE` and add the site origin to `ALLOWED_ORIGINS`.
6. **Agent hosting:** `backend/agent` needs a Dockerfile (Python 3.13, `uv sync`, `python -m agent.worker download-files`
   at build, `CMD python -m agent.worker start`). Deploy with the LiveKit CLI (`lk cloud auth`, `lk agent create`)
   — check LiveKit's current agent-deployment docs and free-tier limits first.

## 4. Environment variables
| Var | Project B (API) | Agent host | Project A (web) |
|---|---|---|---|
| `LIVEKIT_URL`, `LIVEKIT_API_KEY`, `LIVEKIT_API_SECRET` | ✓ | ✓ | ✗ never |
| `ALLOWED_ORIGINS` (prod site URL) | ✓ | | |
| `TRUST_PROXY_HEADERS=true`, `RATE_LIMIT_PER_MINUTE`, `GLOBAL_RATE_LIMIT_PER_MINUTE` | ✓ | | |
| Redis URL/token (after blocker 3) | ✓ | | |
| `AGENT_NAME`, `STT_MODEL`, `LLM_MODEL`, `TTS_MODEL`, `MAX_CALL_SECONDS=60` | `AGENT_NAME` | ✓ | |
| `VITE_CALL_LIMIT_SECONDS=60` (only if not 60), `VITE_API_BASE` (only if not using rewrites) | | | ✓ |

Set secrets in the Vercel / LiveKit dashboards — never commit `.env`. Consider **rotating the LiveKit key**
once production keys are in use, since the dev key lived in a local file.

## 5. Definition of done
- [ ] `uv run pytest` passes (plus new limiter tests); `npm run build` passes.
- [ ] `curl -X POST https://<site>/api/token` → 200 with token; 6th call within a minute → 429 **across instances**.
- [ ] Agent shows "registered worker" in LiveKit Cloud; a production call rings, agent greets
      ("…this is a one-minute demo only…"), captions appear, call ends at 60 s and the panel fades out.
- [ ] Response contains no secrets; browser bundle contains no `LIVEKIT_API_SECRET`.
- [ ] Test Chrome + Safari desktop and one phone (mic permission, autoplay of ring/agent audio).
- [ ] Update `README.md` (deploy section) and `PROGRESS.md` with what was actually verified.

## 6. Known gaps / notes
- Hero uses a procedural SVG backdrop; optional licensed photo at `web/public/images/hero.jpg`.
- Contact email `hello@connect.example` is a placeholder.
- Unexplained `net::ERR_CONNECTION_REFUSED` seen once in the dev console; not reproduced as a call failure.
- Commit author email on the first commit is a local machine address; set `git config --global user.email`
  to a GitHub-linked email for future commits.
- Inference (STT/LLM/TTS) is billed via LiveKit Cloud after free-tier allowances — keep the 60 s cap.
