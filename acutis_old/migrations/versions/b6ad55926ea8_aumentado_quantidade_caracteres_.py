"""aumentado quantidade caracteres telefone clifor

Revision ID: b6ad55926ea8
Revises: d638e4050e42
Create Date: 2025-01-29 00:22:15.037955

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "b6ad55926ea8"
down_revision = "d638e4050e42"
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("clifor", schema=None) as batch_op:
        batch_op.alter_column(
            "telefone1",
            existing_type=sa.VARCHAR(
                length=15, collation="SQL_Latin1_General_CP1_CI_AS"
            ),
            type_=sa.String(length=30),
            existing_nullable=True,
        )


def downgrade():
    with op.batch_alter_table("clifor", schema=None) as batch_op:
        batch_op.alter_column(
            "telefone1",
            existing_type=sa.String(length=30),
            type_=sa.VARCHAR(
                length=15, collation="SQL_Latin1_General_CP1_CI_AS"
            ),
            existing_nullable=True,
        )
