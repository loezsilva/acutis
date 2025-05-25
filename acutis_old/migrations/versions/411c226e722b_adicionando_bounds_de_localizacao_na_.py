"""adicionando bounds de localizacao na tabela enderecos

Revision ID: 411c226e722b
Revises: f00ceecec0d8
Create Date: 2025-01-23 15:38:58.864470

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "411c226e722b"
down_revision = "f00ceecec0d8"
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("endereco", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column("latitude_nordeste", sa.Float(), nullable=True)
        )
        batch_op.add_column(
            sa.Column("longitude_nordeste", sa.Float(), nullable=True)
        )
        batch_op.add_column(
            sa.Column("latitude_sudoeste", sa.Float(), nullable=True)
        )
        batch_op.add_column(
            sa.Column("longitude_sudoeste", sa.Float(), nullable=True)
        )


def downgrade():
    with op.batch_alter_table("endereco", schema=None) as batch_op:
        batch_op.drop_column("longitude_sudoeste")
        batch_op.drop_column("latitude_sudoeste")
        batch_op.drop_column("longitude_nordeste")
        batch_op.drop_column("latitude_nordeste")
