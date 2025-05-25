"""adicionando coluna contabilizar na tabela benfeitores

Revision ID: 710e9f5a64fe
Revises: f81d51103148
Create Date: 2025-04-11 17:02:56.229161

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '710e9f5a64fe'
down_revision = 'f81d51103148'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('benfeitores', schema=None) as batch_op:
        batch_op.add_column(sa.Column('contabilizar', sa.Boolean(), nullable=False))
        batch_op.create_index(batch_op.f('ix_benfeitores_contabilizar'), ['contabilizar'], unique=False)


def downgrade():
    with op.batch_alter_table('benfeitores', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_benfeitores_contabilizar'))
        batch_op.drop_column('contabilizar')
