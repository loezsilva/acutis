"""adicionando historico de movimentacoes agape

Revision ID: 3044119f7e35
Revises: 7454bd027061
Create Date: 2025-04-11 18:13:42.351707

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3044119f7e35'
down_revision = '7454bd027061'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('historicos_movimentacoes_agape',
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('fk_estoque_agape_id', sa.Uuid(), nullable=False),
    sa.Column('quantidade', sa.Integer(), nullable=False),
    sa.Column('tipo_movimentacoes', sa.Enum('entrada', 'saida', name='tipomovimentacaoenum'), nullable=False),
    sa.Column('origem', sa.Enum('acao', 'aquisicao', 'estoque', name='historicoorigemenum'), nullable=True),
    sa.Column('destino', sa.Enum('acao', 'doacao', 'estoque', name='historicodestinoenum'), nullable=True),
    sa.Column('fk_instancia_acao_agape_id', sa.Uuid(), nullable=True),
    sa.Column('criado_em', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('atualizado_em', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.ForeignKeyConstraint(['fk_estoque_agape_id'], ['estoques_agape.id'], ),
    sa.ForeignKeyConstraint(['fk_instancia_acao_agape_id'], ['instancias_acoes_agape.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('historicos_movimentacoes_agape', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_historicos_movimentacoes_agape_destino'), ['destino'], unique=False)
        batch_op.create_index(batch_op.f('ix_historicos_movimentacoes_agape_fk_estoque_agape_id'), ['fk_estoque_agape_id'], unique=False)
        batch_op.create_index(batch_op.f('ix_historicos_movimentacoes_agape_fk_instancia_acao_agape_id'), ['fk_instancia_acao_agape_id'], unique=False)
        batch_op.create_index(batch_op.f('ix_historicos_movimentacoes_agape_origem'), ['origem'], unique=False)
        batch_op.create_index(batch_op.f('ix_historicos_movimentacoes_agape_tipo_movimentacoes'), ['tipo_movimentacoes'], unique=False)


def downgrade():
    with op.batch_alter_table('historicos_movimentacoes_agape', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_historicos_movimentacoes_agape_tipo_movimentacoes'))
        batch_op.drop_index(batch_op.f('ix_historicos_movimentacoes_agape_origem'))
        batch_op.drop_index(batch_op.f('ix_historicos_movimentacoes_agape_fk_instancia_acao_agape_id'))
        batch_op.drop_index(batch_op.f('ix_historicos_movimentacoes_agape_fk_estoque_agape_id'))
        batch_op.drop_index(batch_op.f('ix_historicos_movimentacoes_agape_destino'))

    op.drop_table('historicos_movimentacoes_agape')
