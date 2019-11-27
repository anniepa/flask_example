"""empty message

Revision ID: e54bae31e314
Revises: 
Create Date: 2019-11-27 15:06:56.700189

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e54bae31e314'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('trainer',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=True),
    sa.Column('pw_hash', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_trainer_username'), 'trainer', ['username'], unique=True)
    op.create_table('pokemon',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nickname', sa.String(length=140), nullable=True),
    sa.Column('species', sa.String(length=64), nullable=True),
    sa.Column('level', sa.String(length=64), nullable=True),
    sa.Column('trainer', sa.String(length=64), nullable=True),
    sa.Column('ev_hp', sa.Integer(), nullable=True),
    sa.Column('ev_attack', sa.Integer(), nullable=True),
    sa.Column('ev_spattack', sa.Integer(), nullable=True),
    sa.Column('ev_defence', sa.Integer(), nullable=True),
    sa.Column('ev_spdefence', sa.Integer(), nullable=True),
    sa.Column('ev_speed', sa.Integer(), nullable=True),
    sa.Column('pokerus', sa.Boolean(), nullable=True),
    sa.Column('in_session', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['trainer'], ['trainer.username'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_pokemon_nickname'), 'pokemon', ['nickname'], unique=True)
    op.create_table('session',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('pokemon', sa.String(length=140), nullable=True),
    sa.Column('times_start', sa.DateTime(), nullable=True),
    sa.Column('times_end', sa.DateTime(), nullable=True),
    sa.Column('sess_length', sa.Integer(), nullable=True),
    sa.Column('trainer', sa.String(length=64), nullable=True),
    sa.ForeignKeyConstraint(['pokemon'], ['pokemon.nickname'], ),
    sa.ForeignKeyConstraint(['trainer'], ['trainer.username'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('session')
    op.drop_index(op.f('ix_pokemon_nickname'), table_name='pokemon')
    op.drop_table('pokemon')
    op.drop_index(op.f('ix_trainer_username'), table_name='trainer')
    op.drop_table('trainer')
    # ### end Alembic commands ###