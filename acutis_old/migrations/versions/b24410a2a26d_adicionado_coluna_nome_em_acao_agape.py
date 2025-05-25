"""adicionado coluna nome em acao agape

Revision ID: b24410a2a26d
Revises: 8a73e41471c7
Create Date: 2025-01-13 12:27:27.447482

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "b24410a2a26d"
down_revision = "8a73e41471c7"
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("acao_agape", schema=None) as batch_op:
        batch_op.add_column(sa.Column("nome", sa.String(), nullable=False))


def downgrade():
    with op.batch_alter_table("acao_agape", schema=None) as batch_op:
        batch_op.drop_column("nome")
