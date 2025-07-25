"""init

Revision ID: 61b956ec8284
Revises: 
Create Date: 2025-06-25 02:08:20.474986

"""
from typing import Sequence, Union
import sqlmodel.sql.sqltypes
from alembic import op
import sqlalchemy as sa



# revision identifiers, used by Alembic.
revision: str = '61b956ec8284'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('accountuser',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sqlmodel.sql.sqltypes.AutoString(length=100), nullable=False),
    sa.Column('email', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('hashed_password', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('disabled', sa.Boolean(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_accountuser_email'), 'accountuser', ['email'], unique=True)
    op.create_table('category',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('id_tmdb', sa.Integer(), nullable=True),
    sa.Column('name', sqlmodel.sql.sqltypes.AutoString(length=100), nullable=False),
    sa.Column('description', sqlmodel.sql.sqltypes.AutoString(length=500), nullable=True),
    sa.Column('slug', sqlmodel.sql.sqltypes.AutoString(length=100), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('slug')
    )
    op.create_index(op.f('ix_category_id_tmdb'), 'category', ['id_tmdb'], unique=True)
    op.create_index(op.f('ix_category_name'), 'category', ['name'], unique=True)
    op.create_table('genre',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('id_tmdb', sa.Integer(), nullable=True),
    sa.Column('name', sqlmodel.sql.sqltypes.AutoString(length=100), nullable=False),
    sa.Column('description', sqlmodel.sql.sqltypes.AutoString(length=500), nullable=True),
    sa.Column('slug', sqlmodel.sql.sqltypes.AutoString(length=100), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_genre_id_tmdb'), 'genre', ['id_tmdb'], unique=True)
    op.create_index(op.f('ix_genre_name'), 'genre', ['name'], unique=True)
    op.create_index(op.f('ix_genre_slug'), 'genre', ['slug'], unique=True)
    op.create_table('movie',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('id_tmdb', sa.Integer(), nullable=True),
    sa.Column('title', sqlmodel.sql.sqltypes.AutoString(length=512), nullable=False),
    sa.Column('original_title', sqlmodel.sql.sqltypes.AutoString(length=512), nullable=True),
    sa.Column('original_language', sqlmodel.sql.sqltypes.AutoString(length=15), nullable=True),
    sa.Column('description', sqlmodel.sql.sqltypes.AutoString(length=2000), nullable=True),
    sa.Column('slug', sqlmodel.sql.sqltypes.AutoString(length=512), nullable=True),
    sa.Column('popularity', sa.Float(), nullable=True),
    sa.Column('adult', sa.Boolean(), nullable=False),
    sa.Column('poster', sqlmodel.sql.sqltypes.AutoString(length=255), nullable=True),
    sa.Column('backdrop', sqlmodel.sql.sqltypes.AutoString(length=255), nullable=True),
    sa.Column('release_date', sqlmodel.sql.sqltypes.AutoString(length=10), nullable=True),
    sa.Column('vote_average', sa.Float(), nullable=True),
    sa.Column('vote_count', sa.Integer(), nullable=True),
    sa.Column('category_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['category_id'], ['category.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_movie_category_id'), 'movie', ['category_id'], unique=False)
    op.create_index(op.f('ix_movie_id_tmdb'), 'movie', ['id_tmdb'], unique=True)
    op.create_index(op.f('ix_movie_popularity'), 'movie', ['popularity'], unique=False)
    op.create_index(op.f('ix_movie_release_date'), 'movie', ['release_date'], unique=False)
    op.create_index(op.f('ix_movie_slug'), 'movie', ['slug'], unique=False)
    op.create_index(op.f('ix_movie_title'), 'movie', ['title'], unique=False)
    op.create_index(op.f('ix_movie_vote_average'), 'movie', ['vote_average'], unique=False)
    op.create_index(op.f('ix_movie_vote_count'), 'movie', ['vote_count'], unique=False)
    op.create_table('moviegenrelink',
    sa.Column('movie_id', sa.Integer(), nullable=False),
    sa.Column('genre_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['genre_id'], ['genre.id'], ),
    sa.ForeignKeyConstraint(['movie_id'], ['movie.id'], ),
    sa.PrimaryKeyConstraint('movie_id', 'genre_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('moviegenrelink')
    op.drop_index(op.f('ix_movie_vote_count'), table_name='movie')
    op.drop_index(op.f('ix_movie_vote_average'), table_name='movie')
    op.drop_index(op.f('ix_movie_title'), table_name='movie')
    op.drop_index(op.f('ix_movie_slug'), table_name='movie')
    op.drop_index(op.f('ix_movie_release_date'), table_name='movie')
    op.drop_index(op.f('ix_movie_popularity'), table_name='movie')
    op.drop_index(op.f('ix_movie_id_tmdb'), table_name='movie')
    op.drop_index(op.f('ix_movie_category_id'), table_name='movie')
    op.drop_table('movie')
    op.drop_index(op.f('ix_genre_slug'), table_name='genre')
    op.drop_index(op.f('ix_genre_name'), table_name='genre')
    op.drop_index(op.f('ix_genre_id_tmdb'), table_name='genre')
    op.drop_table('genre')
    op.drop_index(op.f('ix_category_name'), table_name='category')
    op.drop_index(op.f('ix_category_id_tmdb'), table_name='category')
    op.drop_table('category')
    op.drop_index(op.f('ix_accountuser_email'), table_name='accountuser')
    op.drop_table('accountuser')
    # ### end Alembic commands ###
