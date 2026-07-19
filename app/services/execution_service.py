from datetime import UTC, datetime
from decimal import Decimal
from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.orm import Session

from opentelemetry.trace import Status
from opentelemetry.trace.status import StatusCode

from app.enums.workflow import WorkflowStatus
from app.graph.workflow_graph import workflow_graph
from app.repositories.workflow_repository import WorkflowRepository
from app.telemetry.tracer import tracer


class ExecutionService:
    def __init__(self, db: Session):
        self.repository = WorkflowRepository(db)

    def run_workflow(self, workflow_id: UUID):

        with tracer.start_as_current_span("workflow_execution") as span:

            workflow = self.repository.get_by_id(workflow_id)

            if workflow is None:
                raise HTTPException(
                    status_code=404,
                    detail=f"Workflow with ID {workflow_id} not found.",
                )

            workflow.trace_id = format(
                span.get_span_context().trace_id,
                "032x",
            )

            span.set_attribute("workflow.trace_id", workflow.trace_id)
            span.set_attribute("workflow.id", str(workflow.id))
            span.set_attribute("workflow.name", workflow.name)
            span.set_attribute("workflow.status", workflow.status.value)

            # Mark workflow as running
            workflow.status = WorkflowStatus.RUNNING
            self.repository.update(workflow)

            span.set_attribute("workflow.status", workflow.status.value)

            try:

                result = workflow_graph.invoke(
                    {
                        "prompt": workflow.user_prompt,
                        "category": "",
                        "investigation_plan": "",
                        "system_metrics": {},
                        "application_metrics": {},
                        "analysis": "",
                        "final_report": "",
                    }
                )

                workflow.analysis = result["analysis"]

                span.set_attribute(
                    "workflow.category",
                    result["category"],
                )

                workflow.status = WorkflowStatus.COMPLETED
                workflow.completed_at = datetime.now(UTC)

                workflow.duration = (
                    workflow.completed_at - workflow.started_at
                ).total_seconds()

                workflow.total_tokens = 250
                workflow.total_cost = Decimal("0.0015")

                span.set_attribute(
                    "workflow.status",
                    workflow.status.value,
                )

                span.set_attribute(
                    "workflow.final_status",
                    "COMPLETED",
                )

                span.set_attribute(
                    "workflow.duration_seconds",
                    workflow.duration,
                )

                span.set_attribute(
                    "workflow.total_tokens",
                    workflow.total_tokens,
                )

                span.set_attribute(
                    "workflow.total_cost",
                    float(workflow.total_cost),
                )

                span.set_status(
                    Status(StatusCode.OK)
                )

                self.repository.update(workflow)

                return workflow

            except Exception as e:

                span.record_exception(e)
                span.set_status(
                    Status(StatusCode.ERROR)
                )

                workflow.status = WorkflowStatus.FAILED
                workflow.completed_at = datetime.now(UTC)

                workflow.duration = (
                    workflow.completed_at - workflow.started_at
                ).total_seconds()

                workflow.analysis = str(e)
                workflow.error_message = str(e)

                span.set_attribute(
                    "workflow.status",
                    workflow.status.value,
                )

                span.set_attribute(
                    "workflow.final_status",
                    "FAILED",
                )

                span.set_attribute(
                    "workflow.duration_seconds",
                    workflow.duration,
                )

                self.repository.update(workflow)

                raise