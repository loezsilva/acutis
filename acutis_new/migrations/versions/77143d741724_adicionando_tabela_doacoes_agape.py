"""adicionando tabela doacoes agape

Revision ID: 77143d741724
Revises: dea9f66a5727
Create Date: 2025-04-11 17:54:41.713880

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '77143d741724'
down_revision = 'dea9f66a5727'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('doacoes_agape',
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('fk_familia_agape_id', sa.Uuid(), nullable=False),
    sa.Column('criado_em', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('atualizado_em', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.ForeignKeyConstraint(['fk_familia_agape_id'], ['familias_agape.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('doacoes_agape', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_doacoes_agape_fk_familia_agape_id'), ['fk_familia_agape_id'], unique=False)



def downgrade():
    with op.batch_alter_table('doacoes_agape', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_doacoes_agape_fk_familia_agape_id'))

    op.drop_table('doacoes_agape')
