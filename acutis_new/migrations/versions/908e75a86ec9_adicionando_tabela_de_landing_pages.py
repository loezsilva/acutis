"""adicionando tabela de landing pages

Revision ID: 908e75a86ec9
Revises: bf733e22f05e
Create Date: 2025-02-28 13:39:18.511160

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '908e75a86ec9'
down_revision = 'bf733e22f05e'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('landing_pages',
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('fk_campanha_id', sa.Uuid(), nullable=False),
    sa.Column('conteudo', sa.UnicodeText(), nullable=False),
    sa.Column('shlink', sa.String(), nullable=True),
    sa.Column('criado_em', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('atualizado_em', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.ForeignKeyConstraint(['fk_campanha_id'], ['campanhas.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('landing_pages', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_landing_pages_fk_campanha_id'), ['fk_campanha_id'], unique=False)



def downgrade():
    with op.batch_alter_table('landing_pages', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_landing_pages_fk_campanha_id'))

    op.drop_table('landing_pages')
