"""alter_table_cadastro_vocacional

Revision ID: 6ca8a02848f4
Revises: fbf3be8e167a
Create Date: 2024-11-08 10:50:53.311104

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6ca8a02848f4'
down_revision = 'fbf3be8e167a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('cadastro_vocacional', schema=None) as batch_op:
        batch_op.alter_column('cpf',
               existing_type=sa.VARCHAR(length=11, collation='SQL_Latin1_General_CP1_CI_AS'),
               type_=sa.String(length=50),
               existing_nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('cadastro_vocacional', schema=None) as batch_op:
        batch_op.alter_column('cpf',
               existing_type=sa.String(length=50),
               type_=sa.VARCHAR(length=11, collation='SQL_Latin1_General_CP1_CI_AS'),
               existing_nullable=False)

    # ### end Alembic commands ###
