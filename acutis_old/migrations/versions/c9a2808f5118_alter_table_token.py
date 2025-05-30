"""alter table token

Revision ID: c9a2808f5118
Revises: 6835b15ea9b8
Create Date: 2025-01-22 20:40:08.331403

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c9a2808f5118'
down_revision = '6835b15ea9b8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('tokens', schema=None) as batch_op:
        batch_op.alter_column('token',
               existing_type=sa.VARCHAR(length=255, collation='SQL_Latin1_General_CP1_CI_AS'),
               type_=sa.String(length=350),
               existing_nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('tokens', schema=None) as batch_op:
        batch_op.alter_column('token',
               existing_type=sa.String(length=350),
               type_=sa.VARCHAR(length=255, collation='SQL_Latin1_General_CP1_CI_AS'),
               existing_nullable=True)

    # ### end Alembic commands ###
