"""adicionado tabela de templates lp

Revision ID: 4f6af38759d2
Revises: 9380decda06c
Create Date: 2025-02-28 12:47:46.600959

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4f6af38759d2'
down_revision = '9380decda06c'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('templates_lp',
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('titulo', sa.String(), nullable=False),
    sa.Column('conteudo', sa.String(), nullable=False),
    sa.Column('criado_em', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('criado_por', sa.Uuid(), nullable=False),
    sa.Column('atualizado_em', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.ForeignKeyConstraint(['criado_por'], ['membros.id'], ),
    sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    op.drop_table('templates_lp')
