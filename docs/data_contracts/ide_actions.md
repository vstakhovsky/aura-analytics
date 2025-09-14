# Data Contract — ide_actions

- `ts` (timestamp, UTC)
- `user_hash` (string)
- `action_type` (string; enum: edit, navigate, refactor, build, test, etc.)
- `filetype` (string; e.g., .java, .py)
- `duration_ms` (int; optional)

SLA: latency < 1h; completeness ≥ 98%; PII: none.
