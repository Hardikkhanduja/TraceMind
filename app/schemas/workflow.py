from datetime import datetime
from decimal import Decimal 
from uuid import UUID 

from pydantic import BaseModel, ConfigDict
from app.enums.workflow import WorkflowStatus

class WorkflowCreate(BaseModel):
    name: str
    user_prompt: str

class WorkflowResponse(BaseModel):
    id: UUID
    name: str
    user_prompt: str
    status: WorkflowStatus
    analysis: str | None = None
    
    duration: float | None = None

    trace_id: str | None = None

    total_tokens: int = 0

    total_cost: Decimal = Decimal("0.0000")

    error_message: str | None = None

    model_config = ConfigDict(from_attributes=True)

    started_at: datetime

    completed_at: datetime | None = None



class WorkflowUpdate(BaseModel):
    status: WorkflowStatus | None = None