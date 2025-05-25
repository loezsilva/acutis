"""adicionado tabela historico movimentacao agape

Revision ID: 23ea2baf1c5e
Revises: cdddabb2d4ff
Create Date: 2025-01-17 12:39:41.113074

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "23ea2baf1c5e"
down_revision = "cdddabb2d4ff"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "historico_movimentacoes_agape",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("fk_estoque_agape_id", sa.Integer(), nullable=False),
        sa.Column("quantidade", sa.Integer(), nullable=False),
        sa.Column("tipo_movimentacao", sa.String(length=10), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(
            ["fk_estoque_agape_id"],
            ["estoque_agape.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    with op.batch_alter_table(
        "historico_movimentacoes_agape", schema=None
    ) as batch_op:
        batch_op.create_index(
            batch_op.f("ix_historico_movimentacoes_agape_created_at"),
            ["created_at"],
            unique=False,
        )
        batch_op.create_index(
            batch_op.f("ix_historico_movimentacoes_agape_fk_estoque_agape_id"),
            ["fk_estoque_agape_id"],
            unique=False,
        )
        batch_op.create_index(
            batch_op.f("ix_historico_movimentacoes_agape_tipo_movimentacao"),
            ["tipo_movimentacao"],
            unique=False,
        )


def downgrade():
    with op.batch_alter_table(
        "historico_movimentacoes_agape", schema=None
    ) as batch_op:
        batch_op.drop_index(
            batch_op.f("ix_historico_movimentacoes_agape_tipo_movimentacao")
        )
        batch_op.drop_index(
            batch_op.f("ix_historico_movimentacoes_agape_fk_estoque_agape_id")
        )
        batch_op.drop_index(
            batch_op.f("ix_historico_movimentacoes_agape_created_at")
        )

    op.drop_table("historico_movimentacoes_agape")
