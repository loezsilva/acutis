"""Update_Historico_campanhas

Revision ID: 7b2eac8477ca
Revises: 7497296858dc
Create Date: 2024-06-03 12:34:47.296722

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7b2eac8477ca'
down_revision = '7497296858dc'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('historico_campanha_doacoes', schema=None) as batch_op:
        batch_op.add_column(sa.Column('deleted_at', sa.DateTime(), nullable=True))
        batch_op.alter_column('mes_ano',
               existing_type=sa.VARCHAR(collation='SQL_Latin1_General_CP1_CI_AS'),
               type_=sa.Date(),
               existing_nullable=False)
        batch_op.drop_column('data_alteracao')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('historico_campanha_doacoes', schema=None) as batch_op:
        batch_op.add_column(sa.Column('data_alteracao', sa.DATE(), autoincrement=False, nullable=True))
        batch_op.alter_column('mes_ano',
               existing_type=sa.Date(),
               type_=sa.VARCHAR(collation='SQL_Latin1_General_CP1_CI_AS'),
               existing_nullable=False)
        batch_op.drop_column('deleted_at')

    # ### end Alembic commands ###
