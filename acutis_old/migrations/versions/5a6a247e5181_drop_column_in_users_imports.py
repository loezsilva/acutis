"""Drop_Column_In_Users_imports

Revision ID: 5a6a247e5181
Revises: 8b9abc364e7e
Create Date: 2024-04-17 15:22:09.687813

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5a6a247e5181'
down_revision = '8b9abc364e7e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users_imports', schema=None) as batch_op:
        batch_op.drop_column('data_nascimento')
        batch_op.drop_column('id_user')
        batch_op.drop_column('country')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users_imports', schema=None) as batch_op:
        batch_op.add_column(sa.Column('country', sa.NVARCHAR(length=255), autoincrement=False, nullable=True))
        batch_op.add_column(sa.Column('id_user', sa.INTEGER(), autoincrement=False, nullable=False))
        batch_op.add_column(sa.Column('data_nascimento', sa.DATETIME(), autoincrement=False, nullable=True))

    # ### end Alembic commands ###
