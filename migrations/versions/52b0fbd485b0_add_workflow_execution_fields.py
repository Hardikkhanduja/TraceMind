"""add workflow execution fields

Revision ID: 52b0fbd485b0
Revises: 3c640c4135e0
Create Date: 2026-07-13 13:27:14.118129

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "52b0fbd485b0"
down_revision: Union[str, Sequence[str], None] = "3c640c4135e0"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.add_column(
        "workflows",
        sa.Column("analysis", sa.Text(), nullable=True),
    )

    op.add_column(
        "workflows",
        sa.Column("duration", sa.Float(), nullable=True),
    )

    op.add_column(
        "workflows",
        sa.Column("trace_id", sa.String(length=255), nullable=True),
    )

    op.add_column(
        "workflows",
        sa.Column(
            "total_tokens",
            sa.Integer(),
            nullable=False,
            server_default=sa.text("0"),
        ),
    )

    op.add_column(
        "workflows",
        sa.Column(
            "total_cost",
            sa.Numeric(precision=10, scale=4),
            nullable=False,
            server_default=sa.text("0.0000"),
        ),
    )

    op.add_column(
        "workflows",
        sa.Column("error_message", sa.Text(), nullable=True),
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_column("workflows", "error_message")
    op.drop_column("workflows", "total_cost")
    op.drop_column("workflows", "total_tokens")
    op.drop_column("workflows", "trace_id")
    op.drop_column("workflows", "duration")
    op.drop_column("workflows", "analysis")