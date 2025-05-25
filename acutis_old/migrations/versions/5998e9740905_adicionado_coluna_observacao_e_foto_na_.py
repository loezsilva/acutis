"""adicionado coluna observacao e foto na tabela familia agape

Revision ID: 5998e9740905
Revises: 10cc6a204747
Create Date: 2025-02-06 14:11:42.532720

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "5998e9740905"
down_revision = "10cc6a204747"
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("familia_agape", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column("observacao", sa.String(length=255), nullable=True)
        )
        batch_op.add_column(
            sa.Column("foto", sa.String(length=100), nullable=True)
        )


def downgrade():
    with op.batch_alter_table("familia_agape", schema=None) as batch_op:
        batch_op.drop_column("foto")
        batch_op.drop_column("observacao")
