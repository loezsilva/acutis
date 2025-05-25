"""create_table_actions_leads

Revision ID: c26ecdb982bf
Revises: 327fd91cc633
Create Date: 2024-07-24 11:17:14.422398

"""
from alembic import op
import sqlalchemy as sa


revision = 'c26ecdb982bf'
down_revision = '327fd91cc633'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('actions_leads',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nome', sa.String(), nullable=False),
    sa.Column('create_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    op.drop_table('actions_leads')
