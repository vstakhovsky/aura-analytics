# Reporting Orchestrator — SDD Requirement

## User Story
I can trigger `/api/run?upload_id=...`. Agents read `data/uploads/<upload_id>` and produce a **report**.

## Acceptance Criteria
- Response must conform to `report.schema.json`
- Minimum content: ≥2 insights, ≥1 hypothesis per agent
- Executive summary required

## Output Structure
Executive Summary → Figures/Calculations → Hypotheses/PRD/Next Steps

## Validation
- JSON Schema validation as "external judge"
- Evidence links present for insights (sql/figs/metrics)
