from typing import Tuple, List
from api.models import Insight, Hypothesis, Metric, Figure, Complexity

def run() -> Tuple[List[Insight], List[Hypothesis]]:
    i = Insight(
        id="dq-ins-1",
        domain="data_quality",
        title="Null ratio remains stable",
        summary="Share of NULLs in key columns < 0.5% WoW.",
        confidence=0.8,
        impact="Trust in downstream analytics sustained.",
        metrics=[Metric(name="null_rate_pct", value=0.4, unit="%")],
        figures=[Figure(caption="NULL rate trend", path="figs/null_rate.png")],
        methodology="Daily null scan across fact tables",
        evidence="sql/check_nulls.sql",
    )
    h = Hypothesis(
        id="dq-hyp-1",
        title="Introduce stricter ingestion checks",
        problem="Prevent anomalies in upstream ingestion",
        domain="data_quality",
        metrics=[{"name": "alerts_count", "method": "count"}],
        complexity=Complexity(dev_weeks=1),
        summary="Enable column-level constraints on raw layer.",
    )
    return [i], [h]
