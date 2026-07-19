from sqlalchemy.orm import Session

from app.repositories.workflow_repository import WorkflowRepository
from uuid import UUID

from app.schemas.workflow import WorkflowCreate
from app.models.workflow import Workflow

from datetime import UTC, datetime
from fastapi import HTTPException

from app.enums.workflow import WorkflowStatus
from app.schemas.workflow import WorkflowUpdate


class WorkflowService:
    def __init__(self, db: Session):
        self.repository = WorkflowRepository(db)

    def create_workflow(self, workflow: WorkflowCreate) -> Workflow:
        return self.repository.create(workflow)
    
    def get_workflow_by_id(
            self,
            workflow_id: UUID,
    ) -> Workflow:
        workflow =  self.repository.get_by_id(workflow_id)

        if workflow is None:
            raise HTTPException(
                status_code = 404,
                detail=  f"Workflow {workflow_id} not found"
            )
        return workflow
    
    def update_workflow(
        self,
        workflow_id: UUID,
        update: WorkflowUpdate
    ) -> Workflow:
        workflow = self.get_workflow_by_id(workflow_id)
        
        if update.status is not None:
            workflow.status = update.status

            if update.status in(
                WorkflowStatus.COMPLETED,
                WorkflowStatus.FAILED,
            ):
                workflow.completed_at = datetime.now(UTC)

        return self.repository.update(workflow)

    def get_all_workflows(self) -> list[Workflow]:
        return self.repository.get_all()    
    
    def delete_workflow(
        self,
        workflow_id: UUID,
    ):
        workflow = self.get_workflow_by_id(workflow_id)
        self.repository.delete(workflow)