from langgraph.graph import StateGraph, START, END

from app.graph.state import WorkflowState
from app.graph.nodes import (
    classify_issue,
    generate_investigation_plan,
    analyze_prompt,
    collect_runtime_context
)

graph_builder = StateGraph(WorkflowState)

graph_builder.add_node(
    "classify_issue",
    classify_issue,
)

graph_builder.add_node(
    "generate_investigation_plan",
    generate_investigation_plan,
)

graph_builder.add_node(
    "collect_runtime_context",
    collect_runtime_context,
)

graph_builder.add_node(
    "analyze_prompt",
    analyze_prompt,
)

graph_builder.add_edge(
    START,
    "classify_issue",
)

graph_builder.add_edge(
    "classify_issue",
    "generate_investigation_plan",
)

graph_builder.add_edge(
    "generate_investigation_plan",
    "collect_runtime_context",
)

graph_builder.add_edge(
    "collect_runtime_context",
    "analyze_prompt",
)


graph_builder.add_edge(
    "analyze_prompt",
    END,
)

workflow_graph = graph_builder.compile()