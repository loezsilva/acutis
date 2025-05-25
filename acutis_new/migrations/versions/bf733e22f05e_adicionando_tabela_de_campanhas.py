"""adicionando tabela de campanhas

Revision ID: bf733e22f05e
Revises: 4f6af38759d2
Create Date: 2025-02-28 13:21:48.563507

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bf733e22f05e'
down_revision = '4f6af38759d2'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('campanhas',
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('objetivo', sa.Enum('pre_cadastro', 'cadastro', 'doacao', name='objetivoscampanhaenum'), nullable=False),
    sa.Column('nome', sa.String(), nullable=False),
    sa.Column('publica', sa.Boolean(), nullable=False),
    sa.Column('ativa', sa.Boolean(), nullable=False),
    sa.Column('meta', sa.Float(), nullable=True),
    sa.Column('capa', sa.String(), nullable=True),
    sa.Column('chave_pix', sa.String(), nullable=True),
    sa.Column('criado_em', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('criado_por', sa.Uuid(), nullable=False),
    sa.Column('atualizado_em', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.ForeignKeyConstraint(['criado_por'], ['membros.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('campanhas', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_campanhas_ativa'), ['ativa'], unique=False)
        batch_op.create_index(batch_op.f('ix_campanhas_objetivo'), ['objetivo'], unique=False)
        batch_op.create_index(batch_op.f('ix_campanhas_publica'), ['publica'], unique=False)



def downgrade():
    with op.batch_alter_table('campanhas', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_campanhas_publica'))
        batch_op.drop_index(batch_op.f('ix_campanhas_objetivo'))
        batch_op.drop_index(batch_op.f('ix_campanhas_ativa'))

    op.drop_table('campanhas')
