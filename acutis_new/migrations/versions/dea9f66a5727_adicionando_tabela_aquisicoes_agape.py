"""adicionando tabela aquisicoes agape

Revision ID: dea9f66a5727
Revises: b2fcdb2b39e0
Create Date: 2025-04-11 17:50:01.696225

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dea9f66a5727'
down_revision = 'b2fcdb2b39e0'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('aquisicoes_agape',
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('fk_estoque_agape_id', sa.Uuid(), nullable=False),
    sa.Column('quantidade', sa.Integer(), nullable=False),
    sa.Column('criado_em', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('atualizado_em', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.ForeignKeyConstraint(['fk_estoque_agape_id'], ['estoques_agape.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('aquisicoes_agape', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_aquisicoes_agape_fk_estoque_agape_id'), ['fk_estoque_agape_id'], unique=False)



def downgrade():
    with op.batch_alter_table('aquisicoes_agape', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_aquisicoes_agape_fk_estoque_agape_id'))

    op.drop_table('aquisicoes_agape')
