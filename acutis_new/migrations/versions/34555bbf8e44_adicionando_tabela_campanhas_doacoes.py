"""adicionando tabela campanhas doacoes

Revision ID: 34555bbf8e44
Revises: 17b34d1f43ad
Create Date: 2025-04-11 19:45:02.625568

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '34555bbf8e44'
down_revision = '17b34d1f43ad'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('campanhas_doacoes',
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('chave_pix', sa.String(), nullable=False),
    sa.Column('fk_campanha_id', sa.Uuid(), nullable=False),
    sa.Column('criado_em', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('atualizado_em', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.ForeignKeyConstraint(['fk_campanha_id'], ['campanhas.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('campanhas_doacoes', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_campanhas_doacoes_fk_campanha_id'), ['fk_campanha_id'], unique=False)



def downgrade():
    with op.batch_alter_table('campanhas_doacoes', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_campanhas_doacoes_fk_campanha_id'))

    op.drop_table('campanhas_doacoes')
