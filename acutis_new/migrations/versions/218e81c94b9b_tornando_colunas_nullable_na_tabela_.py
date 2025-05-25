"""tornando colunas nullable na tabela fichas vocacional

Revision ID: 218e81c94b9b
Revises: a88422839195
Create Date: 2025-04-12 03:38:26.042250

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '218e81c94b9b'
down_revision = 'a88422839195'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('fichas_vocacional', schema=None) as batch_op:
        batch_op.alter_column('cursos',
               existing_type=sa.VARCHAR(length=255, collation='SQL_Latin1_General_CP1_CI_AS'),
               nullable=True)
        batch_op.alter_column('motivo_divorcio',
               existing_type=sa.VARCHAR(length=255, collation='SQL_Latin1_General_CP1_CI_AS'),
               nullable=True)
        batch_op.alter_column('deixou_religiao_anterior_em',
               existing_type=sa.DATE(),
               nullable=True)
        batch_op.alter_column('remedio_controlado_inicio',
               existing_type=sa.DATE(),
               nullable=True)
        batch_op.alter_column('remedio_controlado_termino',
               existing_type=sa.DATE(),
               nullable=True)
        batch_op.alter_column('descricao_problema_saude',
               existing_type=sa.NVARCHAR(collation='SQL_Latin1_General_CP1_CI_AS'),
               nullable=True)



def downgrade():
    with op.batch_alter_table('fichas_vocacional', schema=None) as batch_op:
        batch_op.alter_column('descricao_problema_saude',
               existing_type=sa.NVARCHAR(collation='SQL_Latin1_General_CP1_CI_AS'),
               nullable=False)
        batch_op.alter_column('remedio_controlado_termino',
               existing_type=sa.DATE(),
               nullable=False)
        batch_op.alter_column('remedio_controlado_inicio',
               existing_type=sa.DATE(),
               nullable=False)
        batch_op.alter_column('deixou_religiao_anterior_em',
               existing_type=sa.DATE(),
               nullable=False)
        batch_op.alter_column('motivo_divorcio',
               existing_type=sa.VARCHAR(length=255, collation='SQL_Latin1_General_CP1_CI_AS'),
               nullable=False)
        batch_op.alter_column('cursos',
               existing_type=sa.VARCHAR(length=255, collation='SQL_Latin1_General_CP1_CI_AS'),
               nullable=False)
