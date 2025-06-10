"""remove não nulo de criado por

Revision ID: 1eddc76a8b7a
Revises: 9ad997dcb468
Create Date: 2025-05-12 21:58:46.636179

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mssql

# revision identifiers, used by Alembic.
revision = '1eddc76a8b7a'
down_revision = '9ad997dcb468'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('campanhas', schema=None) as batch_op:
        batch_op.alter_column('criado_por',
               existing_type=mssql.UNIQUEIDENTIFIER(),
               nullable=True)

    with op.batch_alter_table('cargos_oficiais', schema=None) as batch_op:
        batch_op.alter_column('criado_por',
               existing_type=mssql.UNIQUEIDENTIFIER(),
               nullable=True)
        batch_op.create_index('ix_lembretes_doacoes_recorrentes_criado_por', ['criado_por'], unique=False)

    with op.batch_alter_table('lembretes_doacoes_recorrentes', schema=None) as batch_op:
        batch_op.drop_index('ix_lembretes_doacoes_recorrentes_criado_por')
        batch_op.alter_column('criado_por',
               existing_type=mssql.UNIQUEIDENTIFIER(),
               nullable=True)

    with op.batch_alter_table('templates_lp', schema=None) as batch_op:
        batch_op.alter_column('criado_por',
               existing_type=mssql.UNIQUEIDENTIFIER(),
               nullable=True)


def downgrade():
    
    
    
    with op.batch_alter_table('templates_lp', schema=None) as batch_op:
        batch_op.alter_column('criado_por',
               existing_type=mssql.UNIQUEIDENTIFIER(),
               nullable=False)

    with op.batch_alter_table('lembretes_doacoes_recorrentes', schema=None) as batch_op:
        batch_op.drop_index('ix_lembretes_doacoes_recorrentes_criado_por')
        batch_op.alter_column('criado_por',
               existing_type=mssql.UNIQUEIDENTIFIER(),
               nullable=False)
        
        batch_op.create_index('ix_lembretes_doacoes_recorrentes_criado_por', ['criado_por'], unique=False)

    with op.batch_alter_table('cargos_oficiais', schema=None) as batch_op:
        batch_op.alter_column('criado_por',
               existing_type=mssql.UNIQUEIDENTIFIER(),
               nullable=False)

    with op.batch_alter_table('campanhas', schema=None) as batch_op:
        batch_op.alter_column('criado_por',
               existing_type=mssql.UNIQUEIDENTIFIER(),
               nullable=False)
