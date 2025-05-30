"""alter table mensageria motivo_retorno

Revision ID: d638e4050e42
Revises: c7a36fd36622
Create Date: 2025-01-28 15:56:12.496255

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd638e4050e42'
down_revision = 'c7a36fd36622'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('mensageria', schema=None) as batch_op:
        batch_op.alter_column('motivo_retorno',
               existing_type=sa.VARCHAR(length=200, collation='SQL_Latin1_General_CP1_CI_AS'),
               type_=sa.String(length=1000),
               existing_nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('mensageria', schema=None) as batch_op:
        batch_op.alter_column('motivo_retorno',
               existing_type=sa.String(length=1000),
               type_=sa.VARCHAR(length=200, collation='SQL_Latin1_General_CP1_CI_AS'),
               existing_nullable=True)

    # ### end Alembic commands ###
