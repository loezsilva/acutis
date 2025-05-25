"""adicionando latitude e longitude na tabela familias agape

Revision ID: 36bef7f62a95
Revises: 4ba17a7c6324
Create Date: 2025-01-22 17:09:25.397817

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "36bef7f62a95"
down_revision = "4ba17a7c6324"
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("familia_agape", schema=None) as batch_op:
        batch_op.add_column(sa.Column("latitude", sa.Float(), nullable=True))
        batch_op.add_column(sa.Column("longitude", sa.Float(), nullable=True))


def downgrade():
    with op.batch_alter_table("familia_agape", schema=None) as batch_op:
        batch_op.drop_column("longitude")
        batch_op.drop_column("latitude")
