"""usermodel

Revision ID: a7d84edf6154
Revises:
Create Date: 2026-09-28 22:21:36.068953

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a7d84edf6154'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    bind = op.get_bind()
    if not sa.inspect(bind).has_table("user"):
        op.create_table(
            "user",
            sa.Column("first_name", sa.String(), nullable=False),
            sa.Column("last_name", sa.String(), nullable=False),
            sa.Column("userId", sa.String(), nullable=False),
            sa.Column("username", sa.String(), nullable=False),
            sa.Column("email", sa.String(), nullable=False),
            sa.Column("phone_number", sa.String(), nullable=True),
            sa.Column("transaction_pin", sa.Integer(), nullable=False),
            sa.Column("token", sa.String(), nullable=True),
            sa.Column("password", sa.String(), nullable=False),
            sa.Column("created_at", sa.DateTime(timezone=True), nullable=True),
            sa.PrimaryKeyConstraint("userId"),
            sa.UniqueConstraint("email"),
            sa.UniqueConstraint("phone_number"),
            sa.UniqueConstraint("username"),
        )


def downgrade() -> None:
    """Downgrade schema."""
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    if inspector.has_table("user") and not inspector.has_table("wallet"):
        op.drop_table("user")
