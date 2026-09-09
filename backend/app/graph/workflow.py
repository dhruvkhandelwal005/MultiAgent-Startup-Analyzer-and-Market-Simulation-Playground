"""
LangGraph workflow: event -> relevant agents (conditional) -> CEO decision.
Fully async. Includes persistent memory (fetch history, save decision).
Publishes SSE events at each node for live agent activity streaming.
"""

from langgraph.graph import StateGraph, END
from app.simulation.engine import run_simulation_tick
from app.graph.state import SimulationState
from app.graph.tools_bridge import fetch_simulation_context, format_context_as_text
from app.agents.finance import run_finance_analysis
from app.agents.product import run_product_analysis
from app.agents.developer import run_developer_estimate
from app.agents.marketing import run_marketing_decision
from app.agents.ceo import run_ceo_decision
from app.events import publish
from app.agents.judge import run_judge_evaluation
from app.graph.memory import save_decision, get_recent_history_text, save_evaluation


async def _emit(state: SimulationState, message: str):
    request_id = state.get("request_id")
    if request_id is not None:
        await publish(request_id, {"message": message})


async def load_history_node(state: SimulationState) -> dict:
    await _emit(state, "Loading agent memory/history...")
    history = await get_recent_history_text(state["simulation_id"])
    return {"history_text": history}


async def finance_node(state: SimulationState) -> dict:
    await _emit(state, "Finance agent analyzing budget...")
    context = await fetch_simulation_context(state["simulation_id"])
    text = format_context_as_text(context, state["current_event"]) + f"\n\n{state.get('history_text', '')}"
    decision = run_finance_analysis(text)
    await _emit(state, f"Finance decision: {decision.action}")
    return {"finance_analysis": decision.model_dump()}


async def product_node(state: SimulationState) -> dict:
    await _emit(state, "Product agent analyzing feature strategy...")
    context = await fetch_simulation_context(state["simulation_id"])
    text = format_context_as_text(context, state["current_event"]) + f"\n\n{state.get('history_text', '')}"
    result = run_product_analysis(text)
    await _emit(state, f"Product proposal: {result.feature}")
    return {"product_analysis": result.model_dump()}


async def developer_node(state: SimulationState) -> dict:
    await _emit(state, "Developer agent estimating feasibility...")
    product = state.get("product_analysis", {})
    text = f"Proposed feature: {product.get('feature')} - {product.get('description')}\nEvent: {state['current_event']}"
    result = run_developer_estimate(text)
    await _emit(state, f"Developer estimate: cost {result.development_cost}, {result.development_time_days} days")
    return {"developer_analysis": result.model_dump()}


async def marketing_node(state: SimulationState) -> dict:
    await _emit(state, "Marketing agent designing campaign...")
    context = await fetch_simulation_context(state["simulation_id"])
    text = format_context_as_text(context, state["current_event"]) + f"\n\n{state.get('history_text', '')}"
    result = run_marketing_decision(text)
    await _emit(state, f"Marketing proposal: {result.campaign_name}")
    return {"marketing_analysis": result.model_dump()}


async def ceo_node(state: SimulationState) -> dict:
    await _emit(state, "CEO reviewing all recommendations...")
    finance = state.get("finance_analysis", {})
    product = state.get("product_analysis", {})
    developer = state.get("developer_analysis", {})
    marketing = state.get("marketing_analysis", {})

    summary = f"""
Event: {state['current_event']}

Finance recommendation: {finance.get('action')} (cost: {finance.get('estimated_cost')}, confidence: {finance.get('confidence')})

Product proposal: {product.get('feature')} - {product.get('description')}

Developer estimate: cost {developer.get('development_cost')}, time {developer.get('development_time_days')} days

Marketing proposal: {marketing.get('campaign_name')} targeting {marketing.get('target_segment')}, budget {marketing.get('budget')}, expected reach {marketing.get('expected_reach')}

{state.get('history_text', '')}
"""
    decision = run_ceo_decision(summary)

    from app.guardrails import check_budget_constraint
    budget_check = await check_budget_constraint(state["simulation_id"], decision.estimated_cost)
    if not budget_check["passed"]:
        decision.action = f"[REJECTED - {budget_check['reason']}] {decision.action}"
        decision.requires_approval = True
        await _emit(state, f"Guardrail rejected: {budget_check['reason']}")

    decision_id = await save_decision(
        simulation_id=state["simulation_id"],
        agent_role="ceo",
        action=decision.action,
        reason=decision.reason,
        estimated_cost=decision.estimated_cost,
        requires_approval=decision.requires_approval,
    )

    result = decision.model_dump()
    result["decision_id"] = decision_id

    if decision.requires_approval:
        from app.hitl import create_pending_approval
        approval_id = await create_pending_approval(decision_id)
        result["approval_id"] = approval_id
        await _emit(state, "Decision pending human approval.")
    else:
        await _emit(state, f"CEO decision: {decision.action}")

    eval_context = f"""
Event: {state['current_event']}
Decision: {decision.action}
Reason: {decision.reason}
Estimated cost: {decision.estimated_cost}
Expected impact: {decision.expected_impact}
"""
    evaluation = run_judge_evaluation(eval_context)
    await save_evaluation(
        decision_id=decision_id,
        strategic_score=evaluation.strategic_score,
        financial_score=evaluation.financial_score,
        risk_score=evaluation.risk_score,
        overall_score=evaluation.overall_score,
        feedback=evaluation.feedback,
    )
    result["evaluation"] = evaluation.model_dump()
    await _emit(state, f"Judge score: {evaluation.overall_score}/100")

    cost_applied = decision.estimated_cost if budget_check["passed"] else 0.0
    new_metrics = await run_simulation_tick(state["simulation_id"], decision_cost=cost_applied)
    if new_metrics:
        result["metrics"] = new_metrics
        await _emit(
            state,
            f"Metrics updated: {new_metrics['active_users']} active users, "
            f"₹{new_metrics['cash_remaining']} cash remaining.",
        )

    return {
        "ceo_decision": result,
        "requires_approval": decision.requires_approval,
    }


def route_after_history(state: SimulationState) -> str:
    """
    Conditional routing: decide which agents to trigger based on event_type.
    """
    event_type = state.get("event_type", "general")

    if event_type == "revenue_drop":
        return "finance"
    elif event_type == "adoption_drop":
        return "product"
    else:
        return "finance"  # default: full chain starting from finance


def build_graph():
    graph = StateGraph(SimulationState)

    graph.add_node("load_history", load_history_node)
    graph.add_node("finance", finance_node)
    graph.add_node("product", product_node)
    graph.add_node("developer", developer_node)
    graph.add_node("marketing", marketing_node)
    graph.add_node("ceo", ceo_node)

    graph.set_entry_point("load_history")

    graph.add_conditional_edges(
        "load_history",
        route_after_history,
        {"finance": "finance", "product": "product"},
    )

    def route_after_finance(state: SimulationState) -> str:
        if state.get("event_type") == "revenue_drop":
            return "ceo"
        return "product"

    def route_after_product(state: SimulationState) -> str:
        if state.get("event_type") == "adoption_drop":
            return "marketing"
        return "developer"

    graph.add_conditional_edges("finance", route_after_finance, {"ceo": "ceo", "product": "product"})
    graph.add_conditional_edges("product", route_after_product, {"marketing": "marketing", "developer": "developer"})
    graph.add_edge("developer", "marketing")
    graph.add_edge("marketing", "ceo")
    graph.add_edge("ceo", END)

    return graph.compile()