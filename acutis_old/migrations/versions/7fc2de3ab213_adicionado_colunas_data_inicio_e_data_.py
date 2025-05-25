"""adicionado colunas data inicio e data termino em instancia acao agape

Revision ID: 7fc2de3ab213
Revises: b24410a2a26d
Create Date: 2025-01-15 13:16:48.602686

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "7fc2de3ab213"
down_revision = "b24410a2a26d"
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("instancia_acao_agape", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column("data_inicio", sa.DateTime(), nullable=True)
        )
        batch_op.add_column(
            sa.Column("data_termino", sa.DateTime(), nullable=True)
        )

    with op.batch_alter_table("item_instancia_agape", schema=None) as batch_op:
        batch_op.drop_column("data_inicio")
        batch_op.drop_column("data_termino")


def downgrade():
    with op.batch_alter_table("item_instancia_agape", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column(
                "data_termino",
                sa.DATETIME(),
                autoincrement=False,
                nullable=True,
            )
        )
        batch_op.add_column(
            sa.Column(
                "data_inicio",
                sa.DATETIME(),
                autoincrement=False,
                nullable=True,
            )
        )

    with op.batch_alter_table("instancia_acao_agape", schema=None) as batch_op:
        batch_op.drop_column("data_termino")
        batch_op.drop_column("data_inicio")
