"""add premium content

Revision ID: ad07433c2310
Revises: a852c1f3ddf6
Create Date: 2025-07-04 21:38:39.819614

"""
from typing import Sequence, Union
import sqlmodel.sql.sqltypes
from alembic import op
import sqlalchemy as sa



# revision identifiers, used by Alembic.
revision: str = 'ad07433c2310'
down_revision: Union[str, Sequence[str], None] = 'a852c1f3ddf6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###