from sqlalchemy.orm import Session

from app.models.workflow import Workflow
from app.schemas.workflow import WorkflowCreate

from uuid import UUID
from sqlalchemy import select

class WorkflowRepository:
    def __init__(self, db: Session):  # Constructor
        self.db = db

    def create(self, workflow: WorkflowCreate) -> Workflow:
        db_workflow = Workflow(
            name = workflow.name,
            user_prompt = workflow.user_prompt,
        )

        self.db.add(db_workflow)
        self.db.commit()  # Without commit nothing is stored permanently in the database
        self.db.refresh(db_workflow)

        return db_workflow 

    def get_by_id(self, workflow_id: UUID) -> Workflow | None:
        statement = select(Workflow).where(Workflow.id == workflow_id) 
        result = self.db.execute(statement)
        return result.scalar_one_or_none()

    def update(self, workflow: Workflow) -> Workflow:
        self.db.commit()
        self.db.refresh(workflow)
        return workflow

    def get_all(self) -> list[Workflow]:
        statement = (
            select(Workflow).order_by(Workflow.started_at.desc())
        )

        result = self.db.execute(statement)
        return list(result.scalars().all())
    
    def delete(self, workflow: Workflow) -> None:
        self.db.delete(workflow)
        self.db.commit()    