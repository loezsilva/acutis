"""removendo tabelas antigo vocacional

Revision ID: dd6cae1d8835
Revises: 1b026a1c6682
Create Date: 2025-01-28 11:04:16.488037

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "dd6cae1d8835"
down_revision = "1b026a1c6682"
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("endereco", schema=None) as batch_op:
        batch_op.drop_constraint(
            "FK__endereco__fk_cad__000AF8CF", type_="foreignkey"
        )
        batch_op.drop_column("fk_cadastro_vocacional_id")
    op.drop_table("ficha_vocacional")
    op.drop_table("cadastro_vocacional")
    op.drop_table("pre_cadastro_vocacional")


def downgrade():
    op.create_table(
        "pre_cadastro_vocacional",
        sa.Column(
            "id",
            sa.INTEGER(),
            sa.Identity(always=False, start=1, increment=1),
            autoincrement=True,
            nullable=False,
        ),
        sa.Column(
            "nome",
            sa.VARCHAR(length=250, collation="SQL_Latin1_General_CP1_CI_AS"),
            autoincrement=False,
            nullable=False,
        ),
        sa.Column(
            "email",
            sa.VARCHAR(length=250, collation="SQL_Latin1_General_CP1_CI_AS"),
            autoincrement=False,
            nullable=True,
        ),
        sa.Column(
            "telefone",
            sa.VARCHAR(length=19, collation="SQL_Latin1_General_CP1_CI_AS"),
            autoincrement=False,
            nullable=True,
        ),
        sa.Column(
            "status",
            sa.VARCHAR(length=18, collation="SQL_Latin1_General_CP1_CI_AS"),
            autoincrement=False,
            nullable=False,
        ),
        sa.Column(
            "contatado_em", sa.DATETIME(), autoincrement=False, nullable=True
        ),
        sa.Column(
            "contatado_por", sa.INTEGER(), autoincrement=False, nullable=True
        ),
        sa.Column(
            "observacao",
            sa.VARCHAR(collation="SQL_Latin1_General_CP1_CI_AS"),
            autoincrement=False,
            nullable=True,
        ),
        sa.Column(
            "vocacional",
            sa.VARCHAR(length=15, collation="SQL_Latin1_General_CP1_CI_AS"),
            autoincrement=False,
            nullable=False,
        ),
        sa.Column(
            "created_at", sa.DATETIME(), autoincrement=False, nullable=True
        ),
        sa.Column(
            "deleted_at", sa.DATETIME(), autoincrement=False, nullable=True
        ),
        sa.Column(
            "etapa",
            sa.VARCHAR(length=27, collation="SQL_Latin1_General_CP1_CI_AS"),
            autoincrement=False,
            nullable=False,
        ),
        sa.Column(
            "desistencia_em", sa.DATETIME(), autoincrement=False, nullable=True
        ),
        sa.PrimaryKeyConstraint("id", name="PK__pre_cada__3213E83F9BF75E70"),
    )
    op.create_table(
        "cadastro_vocacional",
        sa.Column(
            "id",
            sa.INTEGER(),
            sa.Identity(always=False, start=1, increment=1),
            autoincrement=True,
            nullable=False,
        ),
        sa.Column(
            "fk_pre_cadastro_id",
            sa.INTEGER(),
            autoincrement=False,
            nullable=False,
        ),
        sa.Column(
            "status",
            sa.VARCHAR(length=15, collation="SQL_Latin1_General_CP1_CI_AS"),
            autoincrement=False,
            nullable=False,
        ),
        sa.Column(
            "data_nascimento", sa.DATE(), autoincrement=False, nullable=True
        ),
        sa.Column(
            "created_at", sa.DATETIME(), autoincrement=False, nullable=False
        ),
        sa.Column(
            "deleted_at", sa.DATETIME(), autoincrement=False, nullable=True
        ),
        sa.Column(
            "observacao",
            sa.VARCHAR(collation="SQL_Latin1_General_CP1_CI_AS"),
            autoincrement=False,
            nullable=True,
        ),
        sa.Column(
            "cpf",
            sa.VARCHAR(length=50, collation="SQL_Latin1_General_CP1_CI_AS"),
            autoincrement=False,
            nullable=False,
        ),
        sa.Column(
            "desistencia_em", sa.DATETIME(), autoincrement=False, nullable=True
        ),
        sa.Column(
            "atualizado_por", sa.INTEGER(), autoincrement=False, nullable=True
        ),
        sa.Column(
            "atualizado_em", sa.DATETIME(), autoincrement=False, nullable=True
        ),
        sa.ForeignKeyConstraint(
            ["fk_pre_cadastro_id"],
            ["pre_cadastro_vocacional.id"],
            name="FK__cadastro___fk_pr__7C3A67EB",
        ),
        sa.PrimaryKeyConstraint("id", name="PK__cadastro__3213E83FC8FA2372"),
    )
    op.create_table(
        "ficha_vocacional",
        sa.Column(
            "id",
            sa.INTEGER(),
            sa.Identity(always=False, start=1, increment=1),
            autoincrement=True,
            nullable=False,
        ),
        sa.Column(
            "fk_cadastro_vocacional_id",
            sa.INTEGER(),
            autoincrement=False,
            nullable=False,
        ),
        sa.Column(
            "created_at", sa.DATETIME(), autoincrement=False, nullable=False
        ),
        sa.Column(
            "deleted_at", sa.DATETIME(), autoincrement=False, nullable=True
        ),
        sa.Column(
            "status",
            sa.VARCHAR(length=20, collation="SQL_Latin1_General_CP1_CI_AS"),
            autoincrement=False,
            nullable=False,
        ),
        sa.Column(
            "desistencia_em", sa.DATETIME(), autoincrement=False, nullable=True
        ),
        sa.Column(
            "atualizado_em", sa.DATETIME(), autoincrement=False, nullable=True
        ),
        sa.Column(
            "atualizado_por", sa.INTEGER(), autoincrement=False, nullable=True
        ),
        sa.Column(
            "observacao",
            sa.VARCHAR(collation="SQL_Latin1_General_CP1_CI_AS"),
            autoincrement=False,
            nullable=True,
        ),
        sa.Column(
            "escolaridade",
            sa.VARCHAR(length=150, collation="SQL_Latin1_General_CP1_CI_AS"),
            autoincrement=False,
            nullable=True,
        ),
        sa.Column(
            "profissao",
            sa.VARCHAR(length=150, collation="SQL_Latin1_General_CP1_CI_AS"),
            autoincrement=False,
            nullable=True,
        ),
        sa.Column(
            "cursos",
            sa.VARCHAR(collation="SQL_Latin1_General_CP1_CI_AS"),
            autoincrement=False,
            nullable=True,
        ),
        sa.Column(
            "sacramentos",
            sa.VARCHAR(collation="SQL_Latin1_General_CP1_CI_AS"),
            autoincrement=False,
            nullable=True,
        ),
        sa.Column(
            "estado_civil",
            sa.VARCHAR(length=100, collation="SQL_Latin1_General_CP1_CI_AS"),
            autoincrement=False,
            nullable=True,
        ),
        sa.Column(
            "justificativa_divorcio",
            sa.VARCHAR(collation="SQL_Latin1_General_CP1_CI_AS"),
            autoincrement=False,
            nullable=True,
        ),
        sa.Column(
            "referencia_conhecimento_instituto",
            sa.VARCHAR(collation="SQL_Latin1_General_CP1_CI_AS"),
            autoincrement=False,
            nullable=True,
        ),
        sa.Column(
            "motivacao_admissao_vocacional",
            sa.VARCHAR(collation="SQL_Latin1_General_CP1_CI_AS"),
            autoincrement=False,
            nullable=True,
        ),
        sa.Column(
            "motivacao_pelo_instituto",
            sa.VARCHAR(collation="SQL_Latin1_General_CP1_CI_AS"),
            autoincrement=False,
            nullable=True,
        ),
        sa.Column(
            "identificacao_com_instituto",
            sa.VARCHAR(collation="SQL_Latin1_General_CP1_CI_AS"),
            autoincrement=False,
            nullable=True,
        ),
        sa.Column(
            "rotina_diaria",
            sa.VARCHAR(collation="SQL_Latin1_General_CP1_CI_AS"),
            autoincrement=False,
            nullable=True,
        ),
        sa.Column(
            "seminario_vida_espirito_santo_realizado_em",
            sa.DATE(),
            autoincrement=False,
            nullable=True,
        ),
        sa.Column(
            "deixou_religiao_anterior_em",
            sa.DATE(),
            autoincrement=False,
            nullable=True,
        ),
        sa.Column(
            "aceitacao_familiar",
            sa.VARCHAR(collation="SQL_Latin1_General_CP1_CI_AS"),
            autoincrement=False,
            nullable=True,
        ),
        sa.Column(
            "problema_saude_descricao",
            sa.VARCHAR(length=255, collation="SQL_Latin1_General_CP1_CI_AS"),
            autoincrement=False,
            nullable=True,
        ),
        sa.Column(
            "remedio_controlado",
            sa.VARCHAR(length=255, collation="SQL_Latin1_General_CP1_CI_AS"),
            autoincrement=False,
            nullable=True,
        ),
        sa.Column(
            "remedio_controlado_data_inicio",
            sa.DATE(),
            autoincrement=False,
            nullable=True,
        ),
        sa.Column(
            "remedio_controlado_data_fim",
            sa.DATE(),
            autoincrement=False,
            nullable=True,
        ),
        sa.Column(
            "testemunho_conversao",
            sa.VARCHAR(collation="SQL_Latin1_General_CP1_CI_AS"),
            autoincrement=False,
            nullable=True,
        ),
        sa.Column(
            "foto_vocacional",
            sa.VARCHAR(length=150, collation="SQL_Latin1_General_CP1_CI_AS"),
            autoincrement=False,
            nullable=True,
        ),
        sa.ForeignKeyConstraint(
            ["fk_cadastro_vocacional_id"],
            ["cadastro_vocacional.id"],
            name="FK__ficha_voc__fk_ca__7F16D496",
        ),
        sa.PrimaryKeyConstraint("id", name="PK__ficha_vo__3213E83FBFEC0DCD"),
    )
    with op.batch_alter_table("endereco", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column(
                "fk_cadastro_vocacional_id",
                sa.INTEGER(),
                autoincrement=False,
                nullable=True,
            )
        )
        batch_op.create_foreign_key(
            "FK__endereco__fk_cad__000AF8CF",
            "cadastro_vocacional",
            ["fk_cadastro_vocacional_id"],
            ["id"],
        )
