from datetime import datetime, UTC      
from uuid import UUID, uuid4

from sqlalchemy import DateTime, Enum as SQLEnum, String
from sqlalchemy import Text
from sqlalchemy import Float
from sqlalchemy import Integer
from sqlalchemy import Numeric
from decimal import Decimal
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base
from app.enums.workflow import WorkflowStatus

class Workflow(Base):
    __tablename__ = "workflows"
    id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid = True),
        primary_key = True,
        default= uuid4
    )

    name: Mapped[str] = mapped_column(
        String(255),
        nullable = False
    )

    user_prompt: Mapped[str] = mapped_column(
        Text, 
        nullable = False
    )

    status: Mapped[WorkflowStatus] = mapped_column(
        SQLEnum(WorkflowStatus),
        default = WorkflowStatus.PENDING,
        nullable = False
    )

    started_at: Mapped[datetime] = mapped_column(
        DateTime(timezone = True),
        default=lambda: datetime.now(UTC)
    )

    completed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone = True),
        nullable = True
    )

    analysis: Mapped[str | None] = mapped_column(
        Text,
        nullable = True,
    )

    duration: Mapped[float | None] = mapped_column(
        Float,
        nullable = True,
    )

    trace_id: Mapped[str | None] = mapped_column(
        String(255),
        nullable = True,
    )

    total_tokens: Mapped[int] = mapped_column(
        Integer,
        default = 0,
        nullable = False,
    )

    total_cost: Mapped[Decimal] = mapped_column(
        Numeric(10,4),
        default = Decimal("0.0000"),
        nullable = False,
    )

    error_message: Mapped[str | None] = mapped_column(
        Text,
        nullable = True,
    )
