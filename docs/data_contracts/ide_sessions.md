# Data Contract — ide_sessions

- `ts` (timestamp, UTC)
- `user_hash` (string; SHA‑256 pseudonymized)
- `ide` (string; product ID)
- `ide_version` (string)
- `os` (string)
- `project_hash` (string; optional)
- `duration_ms` (int; optional)

SLA: latency < 1h; completeness ≥ 98%; PII: none (pseudonymized).
