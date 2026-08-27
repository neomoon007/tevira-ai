"""reset_schema_with_uuid_owner_id

Revision ID: 18e9c2bff4e3
Revises: f1a10b754cd1
Create Date: 2026-08-26 13:09:22.938447

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "18e9c2bff4e3"
down_revision: Union[str, Sequence[str], None] = "f1a10b754cd1"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column(
        "progress_notes",
        "owner_id",
        existing_type=sa.VARCHAR(),
        type_=sa.Uuid(),
        existing_nullable=False,
        postgresql_using="owner_id::uuid",
    )
    op.alter_column(
        "projects",
        "owner_id",
        existing_type=sa.VARCHAR(),
        type_=sa.Uuid(),
        existing_nullable=False,
        postgresql_using="owner_id::uuid",
    )
    op.alter_column(
        "tasks",
        "owner_id",
        existing_type=sa.VARCHAR(),
        type_=sa.Uuid(),
        existing_nullable=False,
        postgresql_using="owner_id::uuid",
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column(
        "tasks",
        "owner_id",
        existing_type=sa.Uuid(),
        type_=sa.VARCHAR(),
        existing_nullable=False,
    )
    op.alter_column(
        "projects",
        "owner_id",
        existing_type=sa.Uuid(),
        type_=sa.VARCHAR(),
        existing_nullable=False,
    )
    op.alter_column(
        "progress_notes",
        "owner_id",
        existing_type=sa.Uuid(),
        type_=sa.VARCHAR(),
        existing_nullable=False,
    )
