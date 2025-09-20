from typing import Tuple, List
from api.models import Insight, Hypothesis, Metric, Figure, Complexity

def run() -> Tuple[List[Insight], List[Hypothesis]]:
    i = Insight(
        id="prd-ins-1",
        domain="product",
        title="Activation rate improved",
        summary="Activation +3.2pp WoW after new onboarding.",
        confidence=0.7,
        impact="Improved early retention expected.",
        metrics=[Metric(name="activation_delta_pp", value=3.2, unit="pp")],
        figures=[Figure(caption="Activation trend", path="figs/activation.png")],
        methodology="Cohort activation D7",
        evidence="sql/activation.sql",
    )
    h = Hypothesis(
        id="prd-hyp-1",
        title="Personalize step 2 CTA",
        problem="Reduce drop at step 2",
        domain="product",
        metrics=[{"name": "step2_ctr", "method": "rate"}],
        complexity=Complexity(dev_weeks=2),
        summary="A/B test context CTA on step 2.",
    )
    return [i], [h]
