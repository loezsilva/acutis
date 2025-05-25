"""adicionando tabela de familias agape

Revision ID: e8d78c08a296
Revises: 710e9f5a64fe
Create Date: 2025-04-11 17:17:24.464710

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e8d78c08a296'
down_revision = '710e9f5a64fe'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('familias_agape',
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('fk_endereco_id', sa.Uuid(), nullable=False),
    sa.Column('nome_familia', sa.String(length=100), nullable=False),
    sa.Column('status', sa.Boolean(), nullable=False),
    sa.Column('observacao', sa.String(), nullable=True),
    sa.Column('comprovante_residencia', sa.String(), nullable=True),
    sa.Column('deletado_em', sa.DateTime(), nullable=True),
    sa.Column('criado_em', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('atualizado_em', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('cadastrada_por', sa.Uuid(), nullable=False),
    sa.ForeignKeyConstraint(['cadastrada_por'], ['membros.id'], ),
    sa.ForeignKeyConstraint(['fk_endereco_id'], ['enderecos.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('familias_agape', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_familias_agape_cadastrada_por'), ['cadastrada_por'], unique=False)
        batch_op.create_index(batch_op.f('ix_familias_agape_fk_endereco_id'), ['fk_endereco_id'], unique=False)
        batch_op.create_index(batch_op.f('ix_familias_agape_nome_familia'), ['nome_familia'], unique=False)
        batch_op.create_index(batch_op.f('ix_familias_agape_status'), ['status'], unique=False)



def downgrade():
    with op.batch_alter_table('familias_agape', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_familias_agape_status'))
        batch_op.drop_index(batch_op.f('ix_familias_agape_nome_familia'))
        batch_op.drop_index(batch_op.f('ix_familias_agape_fk_endereco_id'))
        batch_op.drop_index(batch_op.f('ix_familias_agape_cadastrada_por'))

    op.drop_table('familias_agape')
