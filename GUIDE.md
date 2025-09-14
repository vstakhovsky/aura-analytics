# GUIDE — AURA Analytics (RU/EN)

> **Goal (Цель):** ship a working, demo‑ready analytics service using **Spec‑Driven Development (SDD)**. We’ll follow a step‑by‑step workflow (spec → plan → tasks → implement), keeping the repo bilingual and interview‑ready.

---

## 1) Quickstart / Быстрый старт

**Local (Docker):**
```bash
docker compose up --build
# API: http://localhost:8000/docs  (FastAPI OpenAPI UI)
```

**Create GitHub repo / Создать репозиторий GitHub:**
```bash
# replace YOUR_GH with your account/org
gh repo create YOUR_GH/aura-analytics --public --source . --remote origin --push
# or the classic way:
git init
git add .
git commit -m "chore: AURA Analytics SDD starter"
git branch -M main
git remote add origin git@github.com:YOUR_GH/aura-analytics.git
git push -u origin main
```

---

## 2) SDD Process / Процесс SDD
- **Spec** — problem, users, data contracts, metric registry, APIs, non‑functional.
- **Plan** — architecture, modules, integration surfaces, observability, privacy.
- **Tasks** — atomic tickets autogen from spec; routes, models, tests, UI stubs.
- **Implement** — code to spec; run tests; ship a demo.

All living in `/spec/*.yaml` and `/docs/*` with PRD/ARD‑style rigor.

---

## 3) MVP Scope / Объём MVP
- File & event ingest → Postgres
- Metric Registry v1 (adoption, usage, ai‑coverage, provisioning success, collaboration sessions)
- Insights rules (trends/anomalies; actionable summaries)
- REST API: `/health`, `/ingest`, `/analyze`, `/insights`, `/report`
- Minimal demo pages (TBD in `/ui`) and Markdown/PDF export

---

## 4) Roadmap (v2/v3) / Дорожная карта
- **v2:** MCP connectors (e.g., Databricks, Snowflake), Experiment Registry, BI exports
- **v3:** privacy hardening (residency/masking/TTL), anomaly/drift service, SSO/RBAC, custom metrics DSL

---

## 5) Pricing (Stripe AI framework) / Монетизация
- **Value sold (ценность):** validated, customizable insights that improve developer effectiveness & learning adoption.
- **Charge metric:** per seat; per insight run; hybrid (subscription + usage credits).
- **Packaging:** Starter / Pro (MCP + Experiments) / Enterprise (SSO, residency).
- **Guardrails:** usage limits & budget dashboard; iterate with unit economics.

---

## 6) Working with the tutorial / Как идти по видео‑туториалу
We’ll map the tutorial steps to SDD artifacts:
- Create/maintain `/spec/spec.yaml`, `/spec/plan.yaml`, `/spec/tasks.yaml`
- Keep ARD & Metric Registry in `/docs/*`
- Commit in small, reviewable chunks; each change must sync Spec ↔ Plan ↔ Tasks

Send me each step you complete — I’ll provide the next edits, diffs, and docs to append.
