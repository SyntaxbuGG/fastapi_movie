"""create link usermovievot

Revision ID: 738429f2805b
Revises: bc28ea1c5b37
Create Date: 2025-06-26 18:41:03.454202

"""
from typing import Sequence, Union
import sqlmodel.sql.sqltypes
from alembic import op
import sqlalchemy as sa



# revision identifiers, used by Alembic.
revision: str = '738429f2805b'
down_revision: Union[str, Sequence[str], None] = 'bc28ea1c5b37'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('usermovievote',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('movie_id', sa.Integer(), nullable=False),
    sa.Column('vote_type', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['movie_id'], ['movie.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['accountuser.id'], ),
    sa.PrimaryKeyConstraint('user_id', 'movie_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('usermovievote')
    # ### end Alembic commands ###
