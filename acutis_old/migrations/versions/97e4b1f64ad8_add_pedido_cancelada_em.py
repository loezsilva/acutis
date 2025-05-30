"""add: pedido/cancelada-em

Revision ID: 97e4b1f64ad8
Revises: ae57ee4bcb46
Create Date: 2024-09-03 14:52:28.374378

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '97e4b1f64ad8'
down_revision = 'ae57ee4bcb46'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('pedido', schema=None) as batch_op:
        batch_op.add_column(sa.Column('cancelada_em', sa.DateTime(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('pedido', schema=None) as batch_op:
        batch_op.drop_column('cancelada_em')

    # ### end Alembic commands ###
