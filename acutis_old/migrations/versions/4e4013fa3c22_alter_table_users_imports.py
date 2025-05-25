"""alter_table_users_imports

Revision ID: 4e4013fa3c22
Revises: 9e5fdac9c651
Create Date: 2024-07-24 12:26:42.196285

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4e4013fa3c22'
down_revision = '9e5fdac9c651'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('users_imports', schema=None) as batch_op:
        batch_op.alter_column('origem_cadastro',
               existing_type=sa.VARCHAR(collation='SQL_Latin1_General_CP1_CI_AS'),
               type_=sa.Integer(),
               nullable=False)
        batch_op.create_foreign_key(None, 'actions_leads', ['origem_cadastro'], ['id'])



def downgrade():
    with op.batch_alter_table('users_imports', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.alter_column('origem_cadastro',
               existing_type=sa.Integer(),
               type_=sa.VARCHAR(collation='SQL_Latin1_General_CP1_CI_AS'),
               nullable=True)
