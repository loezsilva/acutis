"""criado coluna atualizado_por em oficiais

Revision ID: f80b5db04d03
Revises: 3c57bbed232c
Create Date: 2025-03-22 18:48:19.305955

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f80b5db04d03'
down_revision = '3c57bbed232c'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('oficiais', schema=None) as batch_op:
        batch_op.add_column(sa.Column('atualizado_por', sa.Uuid(), nullable=True))
        batch_op.create_foreign_key('FK_atualiz_840KGIU', 'membros', ['atualizado_por'], ['id'])


def downgrade():
    with op.batch_alter_table('oficiais', schema=None) as batch_op:
        batch_op.drop_constraint('FK_atualiz_840KGIU', type_='foreignkey')
        batch_op.drop_column('atualizado_por')
