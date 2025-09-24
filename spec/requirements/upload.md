# Upload Service — SDD Requirement

## User Story
As a user, I drop CSV/Excel/JSON files and get an `upload_id` to run agents.

## Acceptance Criteria
- POST `/upload/` (single) and `/upload/batch` (multi) -> returns `{ upload_id, saved[] }`
- Files stored under `data/uploads/<upload_id>/`
- Max size 10 MB per file (initial), extensible later

## Contract
- See `spec/kit.yaml` and `spec/contracts/*` for report contracts.

## Non-Functional
- Deterministic upload_id for batch when provided
- Safe file names, no traversal
