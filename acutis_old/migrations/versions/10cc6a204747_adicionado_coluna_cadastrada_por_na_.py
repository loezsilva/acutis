"""adicionado coluna cadastrada_por na tabela familia agape

Revision ID: 10cc6a204747
Revises: 0dc6b6d32563
Create Date: 2025-02-06 09:13:32.188229

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "10cc6a204747"
down_revision = "0dc6b6d32563"
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("familia_agape", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column("cadastrada_por", sa.Integer(), nullable=True)
        )
        batch_op.create_index(
            batch_op.f("ix_familia_agape_cadastrada_por"),
            ["cadastrada_por"],
            unique=False,
        )
        batch_op.create_foreign_key(
            None, "usuario", ["cadastrada_por"], ["id"]
        )


def downgrade():
    with op.batch_alter_table("familia_agape", schema=None) as batch_op:
        batch_op.drop_constraint(None, type_="foreignkey")
        batch_op.drop_index(batch_op.f("ix_familia_agape_cadastrada_por"))
        batch_op.drop_column("cadastrada_por")
