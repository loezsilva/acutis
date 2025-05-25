"""Criando tabela ficha vocacional

Revision ID: 0f19a97ffd53
Revises: 721e58ef1814
Create Date: 2025-03-14 02:22:26.327591

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0f19a97ffd53'
down_revision = '721e58ef1814'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('fichas_vocacional',
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('fk_usuario_vocacional_id', sa.Uuid(), nullable=False),
    sa.Column('motivacao_instituto', sa.String(length=255), nullable=False),
    sa.Column('motivacao_admissao_vocacional', sa.String(length=255), nullable=False),
    sa.Column('referencia_conhecimento_instituto', sa.String(length=255), nullable=False),
    sa.Column('identificacao_instituto', sa.String(length=255), nullable=False),
    sa.Column('foto_vocacional', sa.String(), nullable=False),
    sa.Column('seminario_realizado_em', sa.Date(), nullable=False),
    sa.Column('testemunho_conversao', sa.UnicodeText(), nullable=False),
    sa.Column('escolaridade', sa.String(length=100), nullable=False),
    sa.Column('profissao', sa.String(length=100), nullable=False),
    sa.Column('cursos', sa.String(length=255), nullable=False),
    sa.Column('rotina_diaria', sa.UnicodeText(), nullable=False),
    sa.Column('aceitacao_familiar', sa.UnicodeText(), nullable=False),
    sa.Column('estado_civil', sa.String(length=100), nullable=False),
    sa.Column('motivo_divorcio', sa.String(length=255), nullable=False),
    sa.Column('deixou_religiao_anterior_em', sa.Date(), nullable=False),
    sa.Column('remedio_controlado_inicio', sa.Date(), nullable=False),
    sa.Column('remedio_controlado_termino', sa.Date(), nullable=False),
    sa.Column('descricao_problema_saude', sa.UnicodeText(), nullable=False),
    sa.Column('criado_em', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('atualizado_em', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.ForeignKeyConstraint(['fk_usuario_vocacional_id'], ['usuarios_vocacional.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('fichas_vocacional', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_fichas_vocacional_fk_usuario_vocacional_id'), ['fk_usuario_vocacional_id'], unique=True)
        batch_op.create_index(batch_op.f('ix_fichas_vocacional_id'), ['id'], unique=False)



def downgrade():
    with op.batch_alter_table('fichas_vocacional', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_fichas_vocacional_id'))
        batch_op.drop_index(batch_op.f('ix_fichas_vocacional_fk_usuario_vocacional_id'))

    op.drop_table('fichas_vocacional')
