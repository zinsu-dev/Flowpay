"""moless

Revision ID: c4d2b3266a1a
Revises: a7d84edf6154
Create Date: 2026-09-30 12:02:06.581950

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c4d2b3266a1a'
down_revision: Union[str, Sequence[str], None] = 'a7d84edf6154'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    if not inspector.has_table("session"):
        op.create_table(
            "session",
            sa.Column("sessionId", sa.String(), nullable=False),
            sa.Column("userId", sa.String(), nullable=False),
            sa.Column("token", sa.String(), nullable=False),
            sa.Column("created_at", sa.DateTime(timezone=True), nullable=True),
            sa.ForeignKeyConstraint(["userId"], ["user.userId"]),
            sa.PrimaryKeyConstraint("sessionId"),
        )
    user_columns = {column["name"] for column in inspector.get_columns("user")}
    if "token" in user_columns:
        op.drop_column("user", "token")


def downgrade() -> None:
    """Downgrade schema."""
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    if inspector.has_table("session"):
        op.drop_table("session")
    user_columns = {column["name"] for column in inspector.get_columns("user")}
    if "token" not in user_columns:
        op.add_column("user", sa.Column("token", sa.String(), nullable=True))
