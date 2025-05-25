"""reestruturacao tabelas agape

Revision ID: 8a73e41471c7
Revises: 6bd8b01a5b9b
Create Date: 2025-01-09 17:08:08.273991

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "8a73e41471c7"
down_revision = "6bd8b01a5b9b"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "instancia_acao_agape",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("fk_endereco_id", sa.Integer(), nullable=False),
        sa.Column("fk_acao_agape_id", sa.Integer(), nullable=False),
        sa.Column("status", sa.String(length=20), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(
            ["fk_acao_agape_id"],
            ["acao_agape.id"],
        ),
        sa.ForeignKeyConstraint(
            ["fk_endereco_id"],
            ["endereco.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    with op.batch_alter_table("instancia_acao_agape", schema=None) as batch_op:
        batch_op.create_index(
            batch_op.f("ix_instancia_acao_agape_fk_acao_agape_id"),
            ["fk_acao_agape_id"],
            unique=False,
        )
        batch_op.create_index(
            batch_op.f("ix_instancia_acao_agape_fk_endereco_id"),
            ["fk_endereco_id"],
            unique=False,
        )

    op.create_table(
        "item_instancia_agape",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("fk_estoque_agape_id", sa.Integer(), nullable=False),
        sa.Column("fk_instancia_acao_agape_id", sa.Integer(), nullable=False),
        sa.Column("quantidade", sa.Integer(), nullable=False),
        sa.Column("data_inicio", sa.DateTime(), nullable=True),
        sa.Column("data_termino", sa.DateTime(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(
            ["fk_estoque_agape_id"],
            ["estoque_agape.id"],
        ),
        sa.ForeignKeyConstraint(
            ["fk_instancia_acao_agape_id"],
            ["instancia_acao_agape.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    with op.batch_alter_table("item_instancia_agape", schema=None) as batch_op:
        batch_op.create_index(
            batch_op.f("ix_item_instancia_agape_fk_instancia_acao_agape_id"),
            ["fk_instancia_acao_agape_id"],
            unique=False,
        )

    op.create_table(
        "item_doacao_agape",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("fk_item_instancia_agape_id", sa.Integer(), nullable=False),
        sa.Column("fk_doacao_agape_id", sa.Integer(), nullable=False),
        sa.Column("quantidade", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(
            ["fk_doacao_agape_id"],
            ["doacao_agape.id"],
        ),
        sa.ForeignKeyConstraint(
            ["fk_item_instancia_agape_id"],
            ["item_instancia_agape.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    with op.batch_alter_table("item_doacao_agape", schema=None) as batch_op:
        batch_op.create_index(
            batch_op.f("ix_item_doacao_agape_fk_doacao_agape_id"),
            ["fk_doacao_agape_id"],
            unique=False,
        )
        batch_op.create_index(
            batch_op.f("ix_item_doacao_agape_fk_item_instancia_agape_id"),
            ["fk_item_instancia_agape_id"],
            unique=False,
        )

    with op.batch_alter_table("acao_agape", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column("created_at", sa.DateTime(), nullable=True)
        )
        batch_op.add_column(
            sa.Column("updated_at", sa.DateTime(), nullable=True)
        )
        batch_op.drop_index("ix_acao_agape_criado_em")
        batch_op.drop_index("ix_acao_agape_fk_endereco_id")
        batch_op.drop_index("ix_acao_agape_fk_estoque_agape_id")
        batch_op.drop_index("ix_acao_agape_fk_programacao_acao_agape_id")
        batch_op.create_index(
            batch_op.f("ix_acao_agape_created_at"),
            ["created_at"],
            unique=False,
        )
        batch_op.drop_constraint(
            "FK__acao_agap__fk_en__4979DDF4", type_="foreignkey"
        )
        batch_op.drop_constraint(
            "FK__acao_agap__fk_pr__7EE1CA6C", type_="foreignkey"
        )
        batch_op.drop_constraint(
            "FK__acao_agap__fk_es__4A6E022D", type_="foreignkey"
        )
        batch_op.drop_column("criado_em")
        batch_op.drop_column("atualizado_em")
        batch_op.drop_column("fk_estoque_agape_id")
        batch_op.drop_column("fk_endereco_id")
        batch_op.drop_column("fk_programacao_acao_agape_id")
        batch_op.drop_column("quantidade")

    with op.batch_alter_table(
        "programacao_acao_agape", schema=None
    ) as batch_op:
        batch_op.drop_index("ix_programacao_acao_agape_criado_em")
        batch_op.drop_index("ix_programacao_acao_agape_data_acao")

    op.drop_table("programacao_acao_agape")
    with op.batch_alter_table("aquisicao_agape", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column("created_at", sa.DateTime(), nullable=True)
        )
        batch_op.add_column(
            sa.Column("updated_at", sa.DateTime(), nullable=True)
        )
        batch_op.drop_index("ix_aquisicao_agape_data_aquisicao")
        batch_op.drop_column("criado_em")
        batch_op.drop_column("atualizado_em")
        batch_op.drop_column("data_aquisicao")

    with op.batch_alter_table("doacao_agape", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column("created_at", sa.DateTime(), nullable=True)
        )
        batch_op.add_column(
            sa.Column("updated_at", sa.DateTime(), nullable=True)
        )
        batch_op.drop_index("ix_doacao_agape_data_doacao")
        batch_op.drop_index("ix_doacao_agape_fk_acao_agape_id")
        batch_op.drop_index("ix_doacao_agape_fk_estoque_agape_id")
        batch_op.create_index(
            batch_op.f("ix_doacao_agape_created_at"),
            ["created_at"],
            unique=False,
        )
        batch_op.drop_constraint(
            "FK__doacao_ag__fk_ac__5026DB83", type_="foreignkey"
        )
        batch_op.drop_constraint(
            "FK__doacao_ag__fk_es__511AFFBC", type_="foreignkey"
        )
        batch_op.drop_column("criado_em")
        batch_op.drop_column("atualizado_em")
        batch_op.drop_column("fk_estoque_agape_id")
        batch_op.drop_column("data_doacao")
        batch_op.drop_column("fk_acao_agape_id")
        batch_op.drop_column("quantidade")

    with op.batch_alter_table("estoque_agape", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column("created_at", sa.DateTime(), nullable=True)
        )
        batch_op.add_column(
            sa.Column("updated_at", sa.DateTime(), nullable=True)
        )
        batch_op.drop_index("ix_estoque_agape_criado_em")
        batch_op.create_index(
            batch_op.f("ix_estoque_agape_created_at"),
            ["created_at"],
            unique=False,
        )
        batch_op.drop_column("criado_em")
        batch_op.drop_column("atualizado_em")

    with op.batch_alter_table("familia_agape", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column("created_at", sa.DateTime(), nullable=True)
        )
        batch_op.add_column(
            sa.Column("updated_at", sa.DateTime(), nullable=True)
        )
        batch_op.drop_index("ix_familia_agape_criado_em")
        batch_op.create_index(
            batch_op.f("ix_familia_agape_created_at"),
            ["created_at"],
            unique=False,
        )
        batch_op.drop_column("criado_em")
        batch_op.drop_column("atualizado_em")

    with op.batch_alter_table("membro_agape", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column("created_at", sa.DateTime(), nullable=True)
        )
        batch_op.add_column(
            sa.Column("updated_at", sa.DateTime(), nullable=True)
        )
        batch_op.create_index(
            batch_op.f("ix_membro_agape_created_at"),
            ["created_at"],
            unique=False,
        )
        batch_op.drop_column("criado_em")
        batch_op.drop_column("atualizado_em")

    with op.batch_alter_table("recibo_agape", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column("created_at", sa.DateTime(), nullable=True)
        )
        batch_op.add_column(
            sa.Column("updated_at", sa.DateTime(), nullable=True)
        )
        batch_op.drop_column("criado_em")
        batch_op.drop_column("atualizado_em")


def downgrade():
    with op.batch_alter_table("recibo_agape", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column(
                "atualizado_em",
                sa.DATETIME(),
                autoincrement=False,
                nullable=True,
            )
        )
        batch_op.add_column(
            sa.Column(
                "criado_em", sa.DATETIME(), autoincrement=False, nullable=True
            )
        )
        batch_op.drop_column("updated_at")
        batch_op.drop_column("created_at")

    with op.batch_alter_table("membro_agape", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column(
                "atualizado_em",
                sa.DATETIME(),
                autoincrement=False,
                nullable=True,
            )
        )
        batch_op.add_column(
            sa.Column(
                "criado_em", sa.DATETIME(), autoincrement=False, nullable=True
            )
        )
        batch_op.drop_index(batch_op.f("ix_membro_agape_created_at"))
        batch_op.drop_column("updated_at")
        batch_op.drop_column("created_at")

    with op.batch_alter_table("familia_agape", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column(
                "atualizado_em",
                sa.DATETIME(),
                autoincrement=False,
                nullable=True,
            )
        )
        batch_op.add_column(
            sa.Column(
                "criado_em", sa.DATETIME(), autoincrement=False, nullable=True
            )
        )
        batch_op.drop_index(batch_op.f("ix_familia_agape_created_at"))
        batch_op.create_index(
            "ix_familia_agape_criado_em", ["criado_em"], unique=False
        )
        batch_op.drop_column("updated_at")
        batch_op.drop_column("created_at")

    with op.batch_alter_table("estoque_agape", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column(
                "atualizado_em",
                sa.DATETIME(),
                autoincrement=False,
                nullable=True,
            )
        )
        batch_op.add_column(
            sa.Column(
                "criado_em", sa.DATETIME(), autoincrement=False, nullable=True
            )
        )
        batch_op.drop_index(batch_op.f("ix_estoque_agape_created_at"))
        batch_op.create_index(
            "ix_estoque_agape_criado_em", ["criado_em"], unique=False
        )
        batch_op.drop_column("updated_at")
        batch_op.drop_column("created_at")

    with op.batch_alter_table("doacao_agape", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column(
                "quantidade", sa.INTEGER(), autoincrement=False, nullable=False
            )
        )
        batch_op.add_column(
            sa.Column(
                "fk_acao_agape_id",
                sa.INTEGER(),
                autoincrement=False,
                nullable=True,
            )
        )
        batch_op.add_column(
            sa.Column(
                "data_doacao",
                sa.DATETIME(),
                autoincrement=False,
                nullable=False,
            )
        )
        batch_op.add_column(
            sa.Column(
                "fk_estoque_agape_id",
                sa.INTEGER(),
                autoincrement=False,
                nullable=False,
            )
        )
        batch_op.add_column(
            sa.Column(
                "atualizado_em",
                sa.DATETIME(),
                autoincrement=False,
                nullable=True,
            )
        )
        batch_op.add_column(
            sa.Column(
                "criado_em", sa.DATETIME(), autoincrement=False, nullable=True
            )
        )
        batch_op.create_foreign_key(
            "FK__doacao_ag__fk_es__511AFFBC",
            "estoque_agape",
            ["fk_estoque_agape_id"],
            ["id"],
        )
        batch_op.create_foreign_key(
            "FK__doacao_ag__fk_ac__5026DB83",
            "acao_agape",
            ["fk_acao_agape_id"],
            ["id"],
        )
        batch_op.drop_index(batch_op.f("ix_doacao_agape_created_at"))
        batch_op.create_index(
            "ix_doacao_agape_fk_estoque_agape_id",
            ["fk_estoque_agape_id"],
            unique=False,
        )
        batch_op.create_index(
            "ix_doacao_agape_fk_acao_agape_id",
            ["fk_acao_agape_id"],
            unique=False,
        )
        batch_op.create_index(
            "ix_doacao_agape_data_doacao", ["data_doacao"], unique=False
        )
        batch_op.drop_column("updated_at")
        batch_op.drop_column("created_at")

    with op.batch_alter_table("aquisicao_agape", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column(
                "data_aquisicao",
                sa.DATETIME(),
                autoincrement=False,
                nullable=False,
            )
        )
        batch_op.add_column(
            sa.Column(
                "atualizado_em",
                sa.DATETIME(),
                autoincrement=False,
                nullable=True,
            )
        )
        batch_op.add_column(
            sa.Column(
                "criado_em", sa.DATETIME(), autoincrement=False, nullable=True
            )
        )
        batch_op.create_index(
            "ix_aquisicao_agape_data_aquisicao",
            ["data_aquisicao"],
            unique=False,
        )
        batch_op.drop_column("updated_at")
        batch_op.drop_column("created_at")

    with op.batch_alter_table("acao_agape", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column(
                "quantidade", sa.INTEGER(), autoincrement=False, nullable=False
            )
        )
        batch_op.add_column(
            sa.Column(
                "fk_programacao_acao_agape_id",
                sa.INTEGER(),
                autoincrement=False,
                nullable=False,
            )
        )
        batch_op.add_column(
            sa.Column(
                "fk_endereco_id",
                sa.INTEGER(),
                autoincrement=False,
                nullable=True,
            )
        )
        batch_op.add_column(
            sa.Column(
                "fk_estoque_agape_id",
                sa.INTEGER(),
                autoincrement=False,
                nullable=False,
            )
        )
        batch_op.add_column(
            sa.Column(
                "atualizado_em",
                sa.DATETIME(),
                autoincrement=False,
                nullable=True,
            )
        )
        batch_op.add_column(
            sa.Column(
                "criado_em", sa.DATETIME(), autoincrement=False, nullable=True
            )
        )
        batch_op.create_foreign_key(
            "FK__acao_agap__fk_es__4A6E022D",
            "estoque_agape",
            ["fk_estoque_agape_id"],
            ["id"],
        )
        batch_op.create_foreign_key(
            "FK__acao_agap__fk_pr__7EE1CA6C",
            "programacao_acao_agape",
            ["fk_programacao_acao_agape_id"],
            ["id"],
        )
        batch_op.create_foreign_key(
            "FK__acao_agap__fk_en__4979DDF4",
            "endereco",
            ["fk_endereco_id"],
            ["id"],
        )
        batch_op.drop_index(batch_op.f("ix_acao_agape_created_at"))
        batch_op.create_index(
            "ix_acao_agape_fk_programacao_acao_agape_id",
            ["fk_programacao_acao_agape_id"],
            unique=False,
        )
        batch_op.create_index(
            "ix_acao_agape_fk_estoque_agape_id",
            ["fk_estoque_agape_id"],
            unique=False,
        )
        batch_op.create_index(
            "ix_acao_agape_fk_endereco_id", ["fk_endereco_id"], unique=False
        )
        batch_op.create_index(
            "ix_acao_agape_criado_em", ["criado_em"], unique=False
        )
        batch_op.drop_column("updated_at")
        batch_op.drop_column("created_at")

    op.create_table(
        "programacao_acao_agape",
        sa.Column(
            "id",
            sa.INTEGER(),
            sa.Identity(always=False, start=1, increment=1),
            autoincrement=True,
            nullable=False,
        ),
        sa.Column(
            "data_acao", sa.DATETIME(), autoincrement=False, nullable=False
        ),
        sa.Column(
            "criado_em", sa.DATETIME(), autoincrement=False, nullable=True
        ),
        sa.Column(
            "atualizado_em", sa.DATETIME(), autoincrement=False, nullable=True
        ),
        sa.PrimaryKeyConstraint("id", name="PK__programa__3213E83F2E1B0EE7"),
    )
    with op.batch_alter_table(
        "programacao_acao_agape", schema=None
    ) as batch_op:
        batch_op.create_index(
            "ix_programacao_acao_agape_data_acao", ["data_acao"], unique=False
        )
        batch_op.create_index(
            "ix_programacao_acao_agape_criado_em", ["criado_em"], unique=False
        )

    with op.batch_alter_table("item_doacao_agape", schema=None) as batch_op:
        batch_op.drop_index(
            batch_op.f("ix_item_doacao_agape_fk_item_instancia_agape_id")
        )
        batch_op.drop_index(
            batch_op.f("ix_item_doacao_agape_fk_doacao_agape_id")
        )

    op.drop_table("item_doacao_agape")
    with op.batch_alter_table("item_instancia_agape", schema=None) as batch_op:
        batch_op.drop_index(
            batch_op.f("ix_item_instancia_agape_fk_instancia_acao_agape_id")
        )

    op.drop_table("item_instancia_agape")
    with op.batch_alter_table("instancia_acao_agape", schema=None) as batch_op:
        batch_op.drop_index(
            batch_op.f("ix_instancia_acao_agape_fk_endereco_id")
        )
        batch_op.drop_index(
            batch_op.f("ix_instancia_acao_agape_fk_acao_agape_id")
        )

    op.drop_table("instancia_acao_agape")
