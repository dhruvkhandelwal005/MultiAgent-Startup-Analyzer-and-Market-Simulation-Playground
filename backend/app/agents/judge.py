from app.llm.gateway import get_llm
from app.schemas import DecisionEvaluation
from app.middleware.logging import log_agent_call
from app.llm.retry import invoke_with_fallback

JUDGE_SYSTEM_PROMPT = """You are an impartial evaluator judging a CEO agent's business decision in a simulated market.
Score the decision on strategic soundness, financial prudence, and risk management.
Be objective and critical. Provide brief, specific feedback."""


@log_agent_call("judge")
def run_judge_evaluation(context: str) -> DecisionEvaluation:
    prompt = f"{JUDGE_SYSTEM_PROMPT}\n\nDecision context:\n{context}\n\nEvaluate this decision."
    return invoke_with_fallback("judge", DecisionEvaluation, prompt)