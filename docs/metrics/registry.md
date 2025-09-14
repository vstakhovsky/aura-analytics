# Metric Registry (v1)

| Key | Name | Definition | Owner | Unit | Notes |
|-----|------|------------|-------|------|-------|
| AS | Active Seats | Unique active users per day/week | Analytics | count | Derived from session or license usage |
| ARp | Adoption Rate (per feature/plugin) | Active users using feature / Active users | Analytics | % | Segmentable by team/project |
| AIcov | AI Usage Coverage | Share of IDE sessions with AI features used | Analytics | % | Requires ai_features_usage ingest |
| CWS | Collaboration Sessions | Count/duration of collaboration sessions | Analytics | count/min | From collaboration_sessions |
| ProvOK | Provisioning Success | Successful provisions / total | Analytics | % | From ide_provisioning events |

All metric SQL must be versioned; breaking changes require Change Log updates.
