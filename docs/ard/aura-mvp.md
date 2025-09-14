# ARD — AURA Analytics MVP

## Problem
Enterprises need privacy‑first insights into developer productivity & continuous learning trends with customizable reporting.

## Goals
- Ingest IDE/events and files into a unified store
- Compute Metrics v1 (adoption, usage, ai‑coverage, provisioning success, collaboration)
- Generate actionable insights and export reports
- Ship an on‑prem‑friendly API and demo UI

## Non‑Goals (MVP)
- No advanced ML models (simple rules/trends only)
- No SSO/RBAC (stub roles)
- No MCP connectors (planned v2)

## Target Users
- DPE/Engineering Managers, Team Leads, Security/Compliance

## Scope (in)
Ingest → Metrics → Insights → API → Minimal UI/Report

## Data Sources & Contracts
See `/docs/data_contracts/*.md`

## Metrics
See `/docs/metrics/registry.md`

## Privacy/Compliance
Pseudonymize user_id; no raw PII stored; residency/TTL configurable.

## API / Reporting
REST: `/health`, `/ingest`, `/analyze`, `/insights`, `/report`

## Acceptance Criteria
- Upload sample files and compute Metrics v1
- At least 3 insights with evidence & confidence
- Report export (Markdown)

## Validation Plan
Golden datasets; unit tests for metric math; manual spot checks in API docs.

## Rollout & Monitoring
Docker compose; OpenAPI docs; basic request logging.

## Assumptions
Synthetic/anon data for demo; controlled environment.

## Change Log
- v0.1: initial MVP scope
