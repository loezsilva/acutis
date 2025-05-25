"""adicionando numero documento em membro

Revision ID: 036b9849ecb2
Revises: 7993552d764b
Create Date: 2025-02-28 16:06:13.533009

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '036b9849ecb2'
down_revision = '7993552d764b'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('membros', schema=None) as batch_op:
        batch_op.add_column(sa.Column('numero_documento', sa.String(length=50), nullable=True))
        batch_op.create_index('ix_membros_numero_documento', ['numero_documento'], unique=True, mssql_where=sa.text('numero_documento IS NOT NULL'))


def downgrade():
    with op.batch_alter_table('membros', schema=None) as batch_op:
        batch_op.drop_index('ix_membros_numero_documento', mssql_where=sa.text('numero_documento IS NOT NULL'))
        batch_op.drop_column('numero_documento')
