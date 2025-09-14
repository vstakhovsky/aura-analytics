# Data Contract — ai_features_usage

- `ts` (timestamp)
- `provider` (string)  # logical name only
- `feature` (string)   # e.g., code_assist, inline_suggest
- `tokens` (int) OR `calls` (int) OR `seconds` (int)
- `outcome` (string; optional)

SLA: near‑real‑time; guardrails for cost attribution.
