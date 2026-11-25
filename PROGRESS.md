# CONNECT. — Development progress

Legend: ✅ done & verified · 🟡 built, not verified end-to-end · ⛔ blocked

| Milestone | Status | Evidence / notes |
|---|---|---|
| M1 Foundation & design system | ✅ | Vite 8 + Vue 3 + TS, Tailwind v4 tokens (`web/src/style.css`), shadcn-style `Button` (cva + cn), design system rationale in `design-system/MASTER.md` |
| M2 Homepage & responsive | 🟡 | All sections built; browser check of 375/768/1440 widths: see "Verification log" |
| M3 GSAP + SVG | 🟡 | Hero line reveal, parallax, scroll-drawn connector, Lenis; reduced-motion path via `gsap.matchMedia` |
| M4 Token service | ✅ | `POST /api/token`, per-IP + global rate limit, scoped JWT; 5 pytest tests pass |
| M5 Voice agent | ⛔ → 🟡 | Worker written against livekit-agents 1.8.13 and imports cleanly; **needs LiveKit credentials to run** |
| M6 Call UI & transcript | 🟡 | Dock, mute, timer, waveform, captions, error/reconnect states built; needs live room to verify |
| M7 Test, optimise, docs | in progress | See README |

## Verification log
- `uv run pytest`: 5 passed. `npm run build`: passes. API smoke test via uvicorn: token issued, 429 after 5/min.
- Browser pane: desktop + 375px render OK, no overflow, no console errors; mic-denied error path works.
- Live LiveKit call: **not run** (no credentials). Lighthouse and a11y audit: not run.

## Simulated vs real
- **Real:** token minting, LiveKit room/agent dispatch code, WebRTC client, transcription stream handling.
- **Not yet exercised:** a live call. No LiveKit credentials existed in the workspace, so no real-time conversation has been verified.
- **Placeholder:** hero photo (procedural SVG backdrop until a licensed photo is added), contact email.

## Deployment — 2026-11-25
- Vercel production: home 200, `/api/health` 200, `/api/token` 200 with room-scoped token, 6th rapid call → 429,
  LiveKit secret not present in built JS. Env vars stored as sensitive in Vercel.
- LiveKit Cloud agent (ap-south): status Running; test dispatch received ("received job request").
- Not yet verified: a full spoken call against production (needs a real browser + microphone).
