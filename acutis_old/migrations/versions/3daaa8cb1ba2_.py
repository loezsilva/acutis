"""empty message

Revision ID: 3daaa8cb1ba2
Revises: 90427cd3d1fc
Create Date: 2023-11-16 17:15:18.788699

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3daaa8cb1ba2'
down_revision = '90427cd3d1fc'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('pedido', schema=None) as batch_op:
        batch_op.add_column(sa.Column('recorrencia_ativa', sa.Boolean(), nullable=True))

    with op.batch_alter_table('processamento_pedido', schema=None) as batch_op:
        batch_op.alter_column('transaction_id',
               existing_type=sa.VARCHAR(length=100, collation='SQL_Latin1_General_CP1_CI_AS'),
               nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('processamento_pedido', schema=None) as batch_op:
        batch_op.alter_column('transaction_id',
               existing_type=sa.VARCHAR(length=100, collation='SQL_Latin1_General_CP1_CI_AS'),
               nullable=False)

    with op.batch_alter_table('pedido', schema=None) as batch_op:
        batch_op.drop_column('recorrencia_ativa')

    # ### end Alembic commands ###
