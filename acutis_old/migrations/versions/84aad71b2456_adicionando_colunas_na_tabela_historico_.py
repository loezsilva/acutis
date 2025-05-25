"""adicionando colunas na tabela historico movimentacao agape

Revision ID: 84aad71b2456
Revises: 23ea2baf1c5e
Create Date: 2025-01-19 00:35:24.303461

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "84aad71b2456"
down_revision = "23ea2baf1c5e"
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table(
        "historico_movimentacoes_agape", schema=None
    ) as batch_op:
        batch_op.add_column(
            sa.Column("origem", sa.String(length=50), nullable=True)
        )
        batch_op.add_column(
            sa.Column("destino", sa.String(length=50), nullable=True)
        )
        batch_op.add_column(
            sa.Column(
                "fk_instancia_acao_agape_id", sa.Integer(), nullable=True
            )
        )
        batch_op.create_index(
            batch_op.f("ix_historico_movimentacoes_agape_destino"),
            ["destino"],
            unique=False,
        )
        batch_op.create_index(
            batch_op.f(
                "ix_historico_movimentacoes_agape_fk_instancia_acao_agape_id"
            ),
            ["fk_instancia_acao_agape_id"],
            unique=False,
        )
        batch_op.create_index(
            batch_op.f("ix_historico_movimentacoes_agape_origem"),
            ["origem"],
            unique=False,
        )
        batch_op.create_foreign_key(
            "FK__historico_movi__fk_inst_ac_aga__A7B3C9E2",
            "instancia_acao_agape",
            ["fk_instancia_acao_agape_id"],
            ["id"],
        )


def downgrade():
    with op.batch_alter_table(
        "historico_movimentacoes_agape", schema=None
    ) as batch_op:
        batch_op.drop_constraint(
            "FK__historico_movi__fk_inst_ac_aga__A7B3C9E2", type_="foreignkey"
        )
        batch_op.drop_index(
            batch_op.f("ix_historico_movimentacoes_agape_origem")
        )
        batch_op.drop_index(
            batch_op.f(
                "ix_historico_movimentacoes_agape_fk_instancia_acao_agape_id"
            )
        )
        batch_op.drop_index(
            batch_op.f("ix_historico_movimentacoes_agape_destino")
        )
        batch_op.drop_column("fk_instancia_acao_agape_id")
        batch_op.drop_column("destino")
        batch_op.drop_column("origem")
