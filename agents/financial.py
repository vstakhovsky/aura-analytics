from typing import Tuple, List
from api.models import Insight, Hypothesis, Metric, Figure, Complexity

def run() -> Tuple[List[Insight], List[Hypothesis]]:
    i = Insight(
        id="fin-ins-1",
        domain="financial",
        title="ARPPU +5% WoW",
        summary="Gross ARPPU increased; mix shift to high tiers.",
        confidence=0.6,
        impact="Potential monthly revenue +2-3%.",
        metrics=[Metric(name="arppu_delta_pct", value=5, unit="%")],
        figures=[Figure(caption="ARPPU trend", path="figs/arppu.png")],
        methodology="Week-over-week",
        evidence="sql/arppu_wow.sql",
    )
    h = Hypothesis(
        id="fin-hyp-1",
        title="Price ladder test",
        problem="Capture higher WTP segments",
        domain="financial",
        metrics=[{"name": "gross_revenue", "method": "sum"}],
        complexity=Complexity(dev_weeks=2),
        summary="Run multivariate price ladder on top SKUs.",
    )
    return [i], [h]
