"""adicionando tabela instancias acoes agape

Revision ID: 7454bd027061
Revises: f6710eecd1f8
Create Date: 2025-04-11 18:06:29.672243

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7454bd027061'
down_revision = 'f6710eecd1f8'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('instancias_acoes_agape',
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('fk_endereco_id', sa.Uuid(), nullable=False),
    sa.Column('fk_acao_agape_id', sa.Uuid(), nullable=False),
    sa.Column('data_inicio', sa.DateTime(), nullable=True),
    sa.Column('data_termino', sa.DateTime(), nullable=True),
    sa.Column('status', sa.Enum('nao_iniciado', 'em_andamento', 'finalizado', name='statusacaoagapeenum'), nullable=False),
    sa.Column('abrangencia', sa.Enum('cep', 'rua', 'bairro', 'cidade', 'estado', 'sem_restricao', name='abrangenciainstanciaacaoagapeenum'), nullable=False),
    sa.Column('criado_em', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('atualizado_em', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.ForeignKeyConstraint(['fk_acao_agape_id'], ['acoes_agape.id'], ),
    sa.ForeignKeyConstraint(['fk_endereco_id'], ['enderecos.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('instancias_acoes_agape', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_instancias_acoes_agape_abrangencia'), ['abrangencia'], unique=False)
        batch_op.create_index(batch_op.f('ix_instancias_acoes_agape_fk_acao_agape_id'), ['fk_acao_agape_id'], unique=False)
        batch_op.create_index(batch_op.f('ix_instancias_acoes_agape_fk_endereco_id'), ['fk_endereco_id'], unique=False)
        batch_op.create_index(batch_op.f('ix_instancias_acoes_agape_status'), ['status'], unique=False)



def downgrade():
    with op.batch_alter_table('instancias_acoes_agape', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_instancias_acoes_agape_status'))
        batch_op.drop_index(batch_op.f('ix_instancias_acoes_agape_fk_endereco_id'))
        batch_op.drop_index(batch_op.f('ix_instancias_acoes_agape_fk_acao_agape_id'))
        batch_op.drop_index(batch_op.f('ix_instancias_acoes_agape_abrangencia'))

    op.drop_table('instancias_acoes_agape')
