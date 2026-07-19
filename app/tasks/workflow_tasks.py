from uuid import UUID
from app.database.session import SessionLocal
from app.services.execution_service import ExecutionService
from app.worker.celery_app import celery_app
 

from app.telemetry.context import(
    attach_trace_context,
    detach_trace_context,
)

@celery_app.task(
    name="execute_workflow",
)
def execute_workflow(
    workflow_id: str,
    trace_context: dict,
):
    token = attach_trace_context(trace_context)
    db = SessionLocal()
    
    try:
        execution_service = ExecutionService(db)
        execution_service.run_workflow(
            UUID(workflow_id),
        )
    finally:
        db.close()
        detach_trace_context(token)