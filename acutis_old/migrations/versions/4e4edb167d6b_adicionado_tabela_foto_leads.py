"""adicionado-tabela-foto-leads

Revision ID: 4e4edb167d6b
Revises: 599666132bd5
Create Date: 2024-07-30 15:12:16.238068

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4e4edb167d6b'
down_revision = '599666132bd5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('foto_leads',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('fk_action_lead_id', sa.Integer(), nullable=True),
    sa.Column('fk_user_import_id', sa.Integer(), nullable=True),
    sa.Column('foto', sa.String(length=100), nullable=True),
    sa.Column('data_criacao', sa.DateTime(), nullable=True),
    sa.Column('data_alteracao', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['fk_action_lead_id'], ['actions_leads.id'], ),
    sa.ForeignKeyConstraint(['fk_user_import_id'], ['users_imports.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('foto_leads')
    # ### end Alembic commands ###
