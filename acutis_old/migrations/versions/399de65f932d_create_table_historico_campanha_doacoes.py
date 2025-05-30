"""Create_Table_Historico_Campanha_Doacoes

Revision ID: 399de65f932d
Revises: 706f39f5f0f4
Create Date: 2024-05-08 16:54:37.097912

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '399de65f932d'
down_revision = '706f39f5f0f4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('historico_campanha_doacoes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('fk_campanha_id', sa.Integer(), nullable=False),
    sa.Column('mes_ano', sa.DateTime(), nullable=False),
    sa.Column('valor_meta', sa.Numeric(), nullable=False),
    sa.Column('valor_atingido', sa.Numeric(), nullable=True),
    sa.ForeignKeyConstraint(['fk_campanha_id'], ['campanha.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('historico_campanha_doacoes')
    # ### end Alembic commands ###
