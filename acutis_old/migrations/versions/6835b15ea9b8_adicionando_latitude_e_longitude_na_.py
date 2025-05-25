"""adicionando latitude e longitude na tabela endereco

Revision ID: 6835b15ea9b8
Revises: 36bef7f62a95
Create Date: 2025-01-22 17:14:22.092603

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "6835b15ea9b8"
down_revision = "36bef7f62a95"
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("endereco", schema=None) as batch_op:
        batch_op.add_column(sa.Column("latitude", sa.Float(), nullable=True))
        batch_op.add_column(sa.Column("longitude", sa.Float(), nullable=True))

    with op.batch_alter_table("familia_agape", schema=None) as batch_op:
        batch_op.drop_column("latitude")
        batch_op.drop_column("longitude")


def downgrade():
    with op.batch_alter_table("familia_agape", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column(
                "longitude",
                sa.FLOAT(precision=53),
                autoincrement=False,
                nullable=True,
            )
        )
        batch_op.add_column(
            sa.Column(
                "latitude",
                sa.FLOAT(precision=53),
                autoincrement=False,
                nullable=True,
            )
        )

    with op.batch_alter_table("endereco", schema=None) as batch_op:
        batch_op.drop_column("longitude")
        batch_op.drop_column("latitude")
