# PROCESS

**SDD lifecycle:** Spec → Plan → Tasks → Implement → Validate → Report → Iterate

1. Update `/spec/spec.yaml` (problem, users, data contracts, metrics, APIs).
2. Update `/spec/plan.yaml` (architecture, components, privacy, observability).
3. Generate or edit `/spec/tasks.yaml` (atomic tasks with acceptance).
4. Implement code under `/backend` (API) and `/ui` (demo).
5. Validate with tests & golden datasets; export a one‑pager/six‑pager under `/reports`.
6. Keep `/docs/metrics/registry.md` and `/docs/data_contracts/*` in sync.
