"""adicionando tabela doacoes

Revision ID: 89d6dbcdd611
Revises: 34555bbf8e44
Create Date: 2025-04-11 19:47:37.952925

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '89d6dbcdd611'
down_revision = '34555bbf8e44'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('doacoes',
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('fk_benfeitor_id', sa.Uuid(), nullable=False),
    sa.Column('fk_campanha_doacao_id', sa.Uuid(), nullable=False),
    sa.Column('cancelado_em', sa.DateTime(), nullable=True),
    sa.Column('cancelado_por', sa.Uuid(), nullable=True),
    sa.Column('contabilizar', sa.Boolean(), nullable=False),
    sa.Column('criado_em', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('atualizado_em', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.ForeignKeyConstraint(['cancelado_por'], ['membros.id'], ),
    sa.ForeignKeyConstraint(['fk_benfeitor_id'], ['benfeitores.id'], ),
    sa.ForeignKeyConstraint(['fk_campanha_doacao_id'], ['campanhas_doacoes.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('doacoes', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_doacoes_contabilizar'), ['contabilizar'], unique=False)
        batch_op.create_index(batch_op.f('ix_doacoes_fk_benfeitor_id'), ['fk_benfeitor_id'], unique=False)
        batch_op.create_index(batch_op.f('ix_doacoes_fk_campanha_doacao_id'), ['fk_campanha_doacao_id'], unique=False)



def downgrade():
    with op.batch_alter_table('doacoes', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_doacoes_fk_campanha_doacao_id'))
        batch_op.drop_index(batch_op.f('ix_doacoes_fk_benfeitor_id'))
        batch_op.drop_index(batch_op.f('ix_doacoes_contabilizar'))

    op.drop_table('doacoes')
