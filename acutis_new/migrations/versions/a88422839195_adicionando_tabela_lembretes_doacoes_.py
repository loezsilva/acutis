"""adicionando tabela lembretes doacoes recorrentes

Revision ID: a88422839195
Revises: 37680b47262b
Create Date: 2025-04-11 19:56:56.611008

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a88422839195'
down_revision = '37680b47262b'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('lembretes_doacoes_recorrentes',
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('fk_processamento_doacao_id', sa.Uuid(), nullable=False),
    sa.Column('criado_por', sa.Uuid(), nullable=False),
    sa.Column('criado_em', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('atualizado_em', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.ForeignKeyConstraint(['criado_por'], ['membros.id'], ),
    sa.ForeignKeyConstraint(['fk_processamento_doacao_id'], ['processamentos_doacoes.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('lembretes_doacoes_recorrentes', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_lembretes_doacoes_recorrentes_criado_por'), ['criado_por'], unique=False)
        batch_op.create_index(batch_op.f('ix_lembretes_doacoes_recorrentes_fk_processamento_doacao_id'), ['fk_processamento_doacao_id'], unique=False)



def downgrade():
    with op.batch_alter_table('lembretes_doacoes_recorrentes', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_lembretes_doacoes_recorrentes_fk_processamento_doacao_id'))
        batch_op.drop_index(batch_op.f('ix_lembretes_doacoes_recorrentes_criado_por'))

    op.drop_table('lembretes_doacoes_recorrentes')
