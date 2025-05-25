"""cria fk_cargo_superior_id em cargos oficiais

Revision ID: 9ad997dcb468
Revises: cd1ebe1bfed1
Create Date: 2025-05-07 09:53:39.972786

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '9ad997dcb468'
down_revision = 'cd1ebe1bfed1'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('cargos_oficiais', schema=None) as batch_op:
        batch_op.add_column(sa.Column('fk_cargo_superior_id', sa.Uuid(), nullable=True))
        batch_op.create_foreign_key('FK_cargo_superior_BIDI1', 'cargos_oficiais', ['fk_cargo_superior_id'], ['id'])

def downgrade():
    with op.batch_alter_table('cargos_oficiais', schema=None) as batch_op:
        batch_op.drop_constraint('FK_cargo_superior_BIDI1', type_='foreignkey')
        batch_op.drop_column('fk_cargo_superior_id')
