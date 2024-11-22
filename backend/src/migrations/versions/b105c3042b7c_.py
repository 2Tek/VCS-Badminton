"""empty message

Revision ID: b105c3042b7c
Revises: 
Create Date: 2024-11-22 16:35:17.559708

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b105c3042b7c'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('courts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('court_no', sa.Integer(), nullable=False),
    sa.Column('date', sa.String(), nullable=False),
    sa.Column('time', sa.String(), nullable=False),
    sa.Column('max_players', sa.Integer(), nullable=False),
    sa.Column('level', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('court_registrations',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('court_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('player_unique_id', sa.String(), nullable=False),
    sa.Column('role', sa.String(), nullable=False),
    sa.Column('reg_date_time', sa.String(), nullable=False),
    sa.Column('fee', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['court_id'], ['courts.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('court_registrations')
    op.drop_table('courts')
    # ### end Alembic commands ###