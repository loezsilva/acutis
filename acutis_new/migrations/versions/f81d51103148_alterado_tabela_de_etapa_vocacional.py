"""alterado tabela de etapa vocacional

Revision ID: f81d51103148
Revises: 22e37c552410
Create Date: 2025-03-27 20:36:09.534527

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f81d51103148'
down_revision = '22e37c552410'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('etapas_vocacional', schema=None) as batch_op:
        batch_op.add_column(sa.Column('fk_responsavel_id', sa.Uuid(), nullable=True))
        batch_op.drop_index('ix_etapas_vocacional_fk_usuario_vocacional_id')
        batch_op.create_index(batch_op.f('ix_etapas_vocacional_fk_usuario_vocacional_id'), ['fk_usuario_vocacional_id'], unique=False)
        batch_op.create_foreign_key('ix_etapas_vocacional_fk_responsavel_id', 'membros', ['fk_responsavel_id'], ['id'])
        batch_op.drop_column('responsavel')


def downgrade():
    with op.batch_alter_table('etapas_vocacional', schema=None) as batch_op:
        batch_op.add_column(sa.Column('responsavel', sa.INTEGER(), autoincrement=False, nullable=True))
        batch_op.drop_constraint('ix_etapas_vocacional_fk_responsavel_id', type_='foreignkey')
        batch_op.drop_index(batch_op.f('ix_etapas_vocacional_fk_usuario_vocacional_id'))
        batch_op.create_index('ix_etapas_vocacional_fk_usuario_vocacional_id', ['fk_usuario_vocacional_id'], unique=True)
        batch_op.drop_column('fk_responsavel_id')
