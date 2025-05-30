"""Alter_table_foto_leads

Revision ID: c794f1ea1f42
Revises: 79fa57ecabe9
Create Date: 2024-08-05 11:05:19.678915

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c794f1ea1f42'
down_revision = '79fa57ecabe9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('foto_leads', schema=None) as batch_op:
        batch_op.add_column(sa.Column('data_download', sa.DateTime(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('foto_leads', schema=None) as batch_op:
        batch_op.drop_column('data_download')

    # ### end Alembic commands ###
