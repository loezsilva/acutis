"""adicionado coluna abrangencia em instancia acao agape

Revision ID: 4ba17a7c6324
Revises: 84aad71b2456
Create Date: 2025-01-20 14:21:51.415815

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "4ba17a7c6324"
down_revision = "84aad71b2456"
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("instancia_acao_agape", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column("abrangencia", sa.String(length=20), nullable=True)
        )
        batch_op.create_index(
            batch_op.f("ix_instancia_acao_agape_abrangencia"),
            ["abrangencia"],
            unique=False,
        )
        batch_op.create_index(
            batch_op.f("ix_instancia_acao_agape_status"),
            ["status"],
            unique=False,
        )


def downgrade():
    with op.batch_alter_table("instancia_acao_agape", schema=None) as batch_op:
        batch_op.drop_index(batch_op.f("ix_instancia_acao_agape_status"))
        batch_op.drop_index(batch_op.f("ix_instancia_acao_agape_abrangencia"))
        batch_op.drop_column("abrangencia")
