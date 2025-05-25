"""adicionado index na coluna data processamento da tabela processamento pedido

Revision ID: 0dc6b6d32563
Revises: b6ad55926ea8
Create Date: 2025-02-04 18:30:32.632601

"""

from alembic import op


# revision identifiers, used by Alembic.
revision = "0dc6b6d32563"
down_revision = "b6ad55926ea8"
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("processamento_pedido", schema=None) as batch_op:
        batch_op.create_index(
            batch_op.f("ix_processamento_pedido_data_processamento"),
            ["data_processamento"],
            unique=False,
        )


def downgrade():
    with op.batch_alter_table("processamento_pedido", schema=None) as batch_op:
        batch_op.drop_index(
            batch_op.f("ix_processamento_pedido_data_processamento")
        )
