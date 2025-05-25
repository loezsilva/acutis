"""criando tabela de benfeitores

Revision ID: ae0be73980fc
Revises: 592012181d55
Create Date: 2025-02-28 09:23:00.572892

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ae0be73980fc'
down_revision = '592012181d55'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('benfeitores',
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('numero_documento', sa.String(length=50), nullable=False),
    sa.Column('nome', sa.String(), nullable=False),
    sa.Column('criado_em', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('atualizado_em', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('benfeitores', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_benfeitores_numero_documento'), ['numero_documento'], unique=True)



def downgrade():
    with op.batch_alter_table('benfeitores', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_benfeitores_numero_documento'))

    op.drop_table('benfeitores')
