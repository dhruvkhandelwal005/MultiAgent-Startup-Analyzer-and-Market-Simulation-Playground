"""
LangGraph workflow: event -> relevant agents -> CEO decision.
"""

import asyncio
from langgraph.graph import StateGraph, END

from app.graph.state import SimulationState
from app.graph.tools_bridge import fetch_simulation_context, format_context_as_text
from app.agents.finance import run_finance_analysis
from app.agents.product import run_product_analysis
from app.agents.developer import run_developer_estimate
from app.agents.marketing import run_marketing_decision
from app.agents.ceo import run_ceo_decision


def finance_node(state: SimulationState) -> dict:
    context = asyncio.run(fetch_simulation_context(state["simulation_id"]))
    text = format_context_as_text(context, state["current_event"])
    decision = run_finance_analysis(text)
    return {"finance_analysis": decision.model_dump()}


def product_node(state: SimulationState) -> dict:
    context = asyncio.run(fetch_simulation_context(state["simulation_id"]))
    text = format_context_as_text(context, state["current_event"])
    result = run_product_analysis(text)
    return {"product_analysis": result.model_dump()}


def developer_node(state: SimulationState) -> dict:
    product = state.get("product_analysis", {})
    text = f"Proposed feature: {product.get('feature')} - {product.get('description')}\nEvent: {state['current_event']}"
    result = run_developer_estimate(text)
    return {"developer_analysis": result.model_dump()}


def marketing_node(state: SimulationState) -> dict:
    context = asyncio.run(fetch_simulation_context(state["simulation_id"]))
    text = format_context_as_text(context, state["current_event"])
    result = run_marketing_decision(text)
    return {"marketing_analysis": result.model_dump()}


def ceo_node(state: SimulationState) -> dict:
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
"""
    decision = run_ceo_decision(summary)
    return {
        "ceo_decision": decision.model_dump(),
        "requires_approval": decision.requires_approval,
    }


def build_graph():
    graph = StateGraph(SimulationState)

    graph.add_node("finance", finance_node)
    graph.add_node("product", product_node)
    graph.add_node("developer", developer_node)
    graph.add_node("marketing", marketing_node)
    graph.add_node("ceo", ceo_node)

    graph.set_entry_point("finance")
    graph.add_edge("finance", "product")
    graph.add_edge("product", "developer")
    graph.add_edge("developer", "marketing")
    graph.add_edge("marketing", "ceo")
    graph.add_edge("ceo", END)

    return graph.compile()