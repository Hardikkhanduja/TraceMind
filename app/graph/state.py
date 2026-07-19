from typing import TypedDict, Any

class WorkflowState(TypedDict):
    # User prompt
    prompt: str

    # Classification
    category: str
    investigation_plan: str

    # Collecteed Evidence
    system_metrics: dict[str, object]
    application_metrics: dict[str, object]

    # AI Output
    analysis: str
    final_report: str