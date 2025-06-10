"""alterado tabela de benfeitores e campanhas doacao

Revision ID: 67f3f5e71cca
Revises: 37c33ec18660
Create Date: 2025-05-28 09:17:29.023087

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mssql

# revision identifiers, used by Alembic.
revision = '67f3f5e71cca'
down_revision = '37c33ec18660'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('benfeitores', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_benfeitores_numero_documento'))
        batch_op.alter_column('numero_documento',
               existing_type=sa.VARCHAR(length=50, collation='SQL_Latin1_General_CP1_CI_AS'),
               nullable=True)
        batch_op.create_index('ix_benfeitores_numero_documento', ['numero_documento'], unique=True, mssql_where=sa.text('numero_documento IS NOT NULL'))

    with op.batch_alter_table('doacoes', schema=None) as batch_op:
        batch_op.alter_column('fk_campanha_doacao_id',
               existing_type=mssql.UNIQUEIDENTIFIER(),
               nullable=True)


def downgrade():
    with op.batch_alter_table('doacoes', schema=None) as batch_op:
        batch_op.drop_index('ix_doacoes_fk_campanha_doacao_id')
        batch_op.alter_column('fk_campanha_doacao_id',
               existing_type=mssql.UNIQUEIDENTIFIER(),
               nullable=False)
        batch_op.create_index('ix_doacoes_fk_campanha_doacao_id', ['fk_campanha_doacao_id'])

    with op.batch_alter_table('benfeitores', schema=None) as batch_op:
        batch_op.drop_index('ix_benfeitores_numero_documento', mssql_where=sa.text('numero_documento IS NOT NULL'))
        batch_op.alter_column('numero_documento',
               existing_type=sa.VARCHAR(length=50, collation='SQL_Latin1_General_CP1_CI_AS'),
               nullable=False)
        batch_op.create_index(batch_op.f('ix_benfeitores_numero_documento'), ['numero_documento'], unique=True)
