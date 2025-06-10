"""Adiciona coluna na tabela de landing pages

Revision ID: 37c33ec18660
Revises: 1eddc76a8b7a
Create Date: 2025-05-20 09:16:30.193576

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mssql

# revision identifiers, used by Alembic.
revision = '37c33ec18660'
down_revision = '1eddc76a8b7a'
branch_labels = None
depends_on = None

def upgrade():

    with op.batch_alter_table('landing_pages', schema=None) as batch_op:
        batch_op.add_column(sa.Column('estrutura_json', sa.UnicodeText(),
           nullable=True)
        )

def downgrade():

    with op.batch_alter_table('landing_pages', schema=None) as batch_op:
        batch_op.drop_column('estrutura_json')
