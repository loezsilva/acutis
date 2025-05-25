"""adicionando tabela itens instancias agape

Revision ID: 9a07757ddbdc
Revises: 3044119f7e35
Create Date: 2025-04-11 18:19:58.317039

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9a07757ddbdc'
down_revision = '3044119f7e35'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('itens_instancias_agape',
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('fk_estoque_agape_id', sa.Uuid(), nullable=False),
    sa.Column('fk_instancia_acao_agape_id', sa.Uuid(), nullable=False),
    sa.Column('quantidade', sa.Integer(), nullable=False),
    sa.Column('criado_em', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('atualizado_em', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.ForeignKeyConstraint(['fk_estoque_agape_id'], ['estoques_agape.id'], ),
    sa.ForeignKeyConstraint(['fk_instancia_acao_agape_id'], ['instancias_acoes_agape.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('itens_instancias_agape', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_itens_instancias_agape_fk_estoque_agape_id'), ['fk_estoque_agape_id'], unique=False)
        batch_op.create_index(batch_op.f('ix_itens_instancias_agape_fk_instancia_acao_agape_id'), ['fk_instancia_acao_agape_id'], unique=False)



def downgrade():
    with op.batch_alter_table('itens_instancias_agape', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_itens_instancias_agape_fk_instancia_acao_agape_id'))
        batch_op.drop_index(batch_op.f('ix_itens_instancias_agape_fk_estoque_agape_id'))

    op.drop_table('itens_instancias_agape')
