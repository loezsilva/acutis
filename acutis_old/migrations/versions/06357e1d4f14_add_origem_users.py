"""Add_origem_users

Revision ID: 06357e1d4f14
Revises: 7dbcb2f52fde
Create Date: 2024-07-13 19:31:52.996315

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '06357e1d4f14'
down_revision = '7dbcb2f52fde'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('usuario', schema=None) as batch_op:
        batch_op.add_column(sa.Column('origem_cadastro', sa.String(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('usuario', schema=None) as batch_op:
        batch_op.drop_column('origem_cadastro')

    # ### end Alembic commands ###
