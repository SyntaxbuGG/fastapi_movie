"""to active

Revision ID: d23c8847df71
Revises: 584df514f07b
Create Date: 2025-07-08 18:00:40.995070

"""

from typing import Sequence, Union
import sqlmodel.sql.sqltypes
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "d23c8847df71"
down_revision: Union[str, Sequence[str], None] = "584df514f07b"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute("""
               UPDATE accountuser SET is_active = TRUE WHERE is_active IS NULL; 
               """)
    op.alter_column(
        "accountuser", "is_active", existing_type=sa.Boolean(), nullable=False
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        'accountuser',
        'is_active',
        existing_type=sa.Boolean(),
        nullable=True
    )
    # ### end Alembic commands ###
