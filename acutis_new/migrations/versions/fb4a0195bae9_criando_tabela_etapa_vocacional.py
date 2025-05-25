"""Criando tabela etapa vocacional

Revision ID: fb4a0195bae9
Revises: 0f19a97ffd53
Create Date: 2025-03-14 02:30:09.539251

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fb4a0195bae9'
down_revision = '0f19a97ffd53'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('etapas_vocacional',
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('fk_usuario_vocacional_id', sa.Uuid(), nullable=False),
    sa.Column('etapa', sa.Enum('pre_cadastro', 'cadastro', 'ficha_vocacional', name='vocationalstepsenum'), nullable=False),
    sa.Column('status', sa.Enum('pendente', 'aprovado', 'reprovado', 'desistencia', name='vocationalstepsstatusenum'), nullable=False),
    sa.Column('justificativa', sa.UnicodeText(), nullable=True),
    sa.Column('responsavel', sa.Integer(), nullable=True),
    sa.Column('criado_em', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('atualizado_em', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.ForeignKeyConstraint(['fk_usuario_vocacional_id'], ['usuarios_vocacional.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('etapas_vocacional', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_etapas_vocacional_fk_usuario_vocacional_id'), ['fk_usuario_vocacional_id'], unique=True)
        batch_op.create_index(batch_op.f('ix_etapas_vocacional_id'), ['id'], unique=False)



def downgrade():
    with op.batch_alter_table('etapas_vocacional', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_etapas_vocacional_id'))
        batch_op.drop_index(batch_op.f('ix_etapas_vocacional_fk_usuario_vocacional_id'))

    op.drop_table('etapas_vocacional')
