"""Merge wallet and authentication migration branches."""

from typing import Sequence, Union


revision: str = "d190f7b3a2c1"
down_revision: Union[str, Sequence[str], None] = (
    "5223c6c11fb9",
    "c4d2b3266a1a",
)
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass