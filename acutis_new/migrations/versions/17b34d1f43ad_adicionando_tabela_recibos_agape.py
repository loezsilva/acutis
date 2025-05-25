"""adicionando tabela recibos agape

Revision ID: 17b34d1f43ad
Revises: 3ed57318c487
Create Date: 2025-04-11 18:36:35.209587

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '17b34d1f43ad'
down_revision = '3ed57318c487'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('recibos_agape',
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('fk_doacao_agape_id', sa.Uuid(), nullable=False),
    sa.Column('recibo', sa.String(), nullable=False),
    sa.Column('criado_em', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('atualizado_em', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.ForeignKeyConstraint(['fk_doacao_agape_id'], ['doacoes_agape.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('recibos_agape', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_recibos_agape_fk_doacao_agape_id'), ['fk_doacao_agape_id'], unique=False)



def downgrade():
    with op.batch_alter_table('recibos_agape', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_recibos_agape_fk_doacao_agape_id'))

    op.drop_table('recibos_agape')
