"""adicionando tabela de acoes agape

Revision ID: 4e324c702cf8
Revises: e8d78c08a296
Create Date: 2025-04-11 17:21:37.225295

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4e324c702cf8'
down_revision = 'e8d78c08a296'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('acoes_agape',
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('nome', sa.String(), nullable=False),
    sa.Column('criado_em', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('atualizado_em', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    op.drop_table('acoes_agape')
