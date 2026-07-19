from fastapi import APIRouter, Depends 
from sqlalchemy.orm import Session
from app.database.dependencies import get_db
from app.schemas.workflow import WorkflowCreate, WorkflowResponse, WorkflowUpdate
from app.services.workflow_service import WorkflowService
from app.telemetry.context import inject_trace_context

from uuid import UUID

from app.tasks.workflow_tasks import execute_workflow

router = APIRouter(
    prefix ="/workflows",
    tags=["Workflows"],
)

@router.post(
    "/",
    response_model = WorkflowResponse,
    status_code = 201
)

def create_workflow(
    workflow: WorkflowCreate,
    db: Session = Depends(get_db),
):
    service = WorkflowService(db)
    db_workflow = service.create_workflow(workflow)
    trace_context = inject_trace_context()
    execute_workflow.delay(
        workflow_id = str(db_workflow.id),
        trace_context = trace_context,
    )

    return db_workflow

@router.get(
    "/{workflow_id}",
    response_model = WorkflowResponse,
)

def get_workflow(
    workflow_id: UUID,
    db: Session = Depends(get_db),
): 
    service = WorkflowService(db)
    return service.get_workflow_by_id(workflow_id)

@router.patch(
    "/{workflow_id}",
    response_model = WorkflowResponse,
)

def update_workflow(
    workflow_id: UUID,
    update: WorkflowUpdate,
    db: Session = Depends(get_db)
):
    service = WorkflowService(db)

    return service.update_workflow(
        workflow_id,
        update,
    )

@router.get(
    "/",
    response_model = list[WorkflowResponse],
)

def get_all_workflows(
    db: Session = Depends(get_db)
):
    service = WorkflowService(db)
    return service.get_all_workflows()

@router.delete(
    "/{workflow_id}",
    status_code = 204
)
def delete_workflow(
    workflow_id: UUID,
    db: Session = Depends(get_db)
):
    service = WorkflowService(db)
    service.delete_workflow(workflow_id)