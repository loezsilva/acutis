"""aumentado quantidade caracteres password hash usuario

Revision ID: 1f803bf9a531
Revises: c73b64e95561
Create Date: 2024-12-17 14:11:28.204328

"""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "1f803bf9a531"
down_revision = "c73b64e95561"
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("usuario", schema=None) as batch_op:
        batch_op.alter_column(
            "password_hash",
            existing_type=sa.VARCHAR(
                length=128, collation="SQL_Latin1_General_CP1_CI_AS"
            ),
            type_=sa.String(),
            existing_nullable=True,
        )


def downgrade():
    with op.batch_alter_table("usuario", schema=None) as batch_op:
        batch_op.alter_column(
            "password_hash",
            existing_type=sa.String(),
            type_=sa.VARCHAR(
                length=128, collation="SQL_Latin1_General_CP1_CI_AS"
            ),
            existing_nullable=True,
        )
