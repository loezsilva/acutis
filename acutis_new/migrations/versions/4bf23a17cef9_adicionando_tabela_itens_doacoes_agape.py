"""adicionando tabela itens doacoes agape

Revision ID: 4bf23a17cef9
Revises: 9a07757ddbdc
Create Date: 2025-04-11 18:23:02.266175

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4bf23a17cef9'
down_revision = '9a07757ddbdc'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('itens_doacoes_agape',
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('fk_item_instancia_agape_id', sa.Uuid(), nullable=False),
    sa.Column('fk_doacao_agape_id', sa.Uuid(), nullable=False),
    sa.Column('quantidade', sa.Integer(), nullable=False),
    sa.Column('criado_em', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('atualizado_em', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.ForeignKeyConstraint(['fk_doacao_agape_id'], ['doacoes_agape.id'], ),
    sa.ForeignKeyConstraint(['fk_item_instancia_agape_id'], ['itens_instancias_agape.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('itens_doacoes_agape', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_itens_doacoes_agape_fk_doacao_agape_id'), ['fk_doacao_agape_id'], unique=False)
        batch_op.create_index(batch_op.f('ix_itens_doacoes_agape_fk_item_instancia_agape_id'), ['fk_item_instancia_agape_id'], unique=False)



def downgrade():
    with op.batch_alter_table('itens_doacoes_agape', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_itens_doacoes_agape_fk_item_instancia_agape_id'))
        batch_op.drop_index(batch_op.f('ix_itens_doacoes_agape_fk_doacao_agape_id'))

    op.drop_table('itens_doacoes_agape')
