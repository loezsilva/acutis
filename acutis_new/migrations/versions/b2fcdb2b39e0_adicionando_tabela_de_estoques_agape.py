"""adicionando tabela de estoques agape

Revision ID: b2fcdb2b39e0
Revises: 4e324c702cf8
Create Date: 2025-04-11 17:37:12.084556

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b2fcdb2b39e0'
down_revision = '4e324c702cf8'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('estoques_agape',
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('item', sa.String(length=100), nullable=False),
    sa.Column('quantidade', sa.Integer(), nullable=False),
    sa.Column('criado_em', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('atualizado_em', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('estoques_agape', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_estoques_agape_item'), ['item'], unique=False)



def downgrade():
    with op.batch_alter_table('estoques_agape', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_estoques_agape_item'))

    op.drop_table('estoques_agape')
