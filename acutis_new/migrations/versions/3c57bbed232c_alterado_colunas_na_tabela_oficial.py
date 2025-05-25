"""alterado colunas na tabela oficial

Revision ID: 3c57bbed232c
Revises: e44de2d28eff
Create Date: 2025-03-19 18:58:31.860725

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mssql

# revision identifiers, used by Alembic.
revision = '3c57bbed232c'
down_revision = 'e44de2d28eff'
branch_labels = None
depends_on = None


def upgrade():
    

    with op.batch_alter_table('oficiais', schema=None) as batch_op:
        batch_op.add_column(sa.Column('fk_superior_id', sa.Uuid(), nullable=True))
        batch_op.add_column(sa.Column('fk_cargo_oficial_id', sa.Uuid(), nullable=False))
        batch_op.drop_index('ix_oficiais_nome_cargo')
        batch_op.drop_index('ix_oficiais_superior')
        batch_op.create_index(batch_op.f('ix_oficiais_fk_cargo_oficial_id'), ['fk_cargo_oficial_id'], unique=False)
        batch_op.create_index(batch_op.f('ix_oficiais_fk_superior_id'), ['fk_superior_id'], unique=False)
        batch_op.drop_constraint('FK__oficiais__superi__6F7569AA', type_='foreignkey')
        batch_op.create_foreign_key('FK__oficiais__fk_super_32DF9SA', 'membros', ['fk_superior_id'], ['id'])
        batch_op.create_foreign_key('FK__cargos_ofici__fk_cargos_34KJ8JA', 'cargos_oficiais', ['fk_cargo_oficial_id'], ['id'])
        batch_op.drop_column('superior')
        batch_op.drop_column('nome_cargo')


def downgrade():
    with op.batch_alter_table('oficiais', schema=None) as batch_op:
        batch_op.add_column(sa.Column('nome_cargo', sa.VARCHAR(length=8, collation='SQL_Latin1_General_CP1_CI_AS'), autoincrement=False, nullable=False))
        batch_op.add_column(sa.Column('superior', mssql.UNIQUEIDENTIFIER(), autoincrement=False, nullable=True))
        batch_op.drop_constraint('FK__oficiais__fk_super_32DF9SA', type_='foreignkey')
        batch_op.drop_constraint('FK__cargos_ofici__fk_cargos_34KJ8JA', type_='foreignkey')
        batch_op.create_foreign_key('FK__oficiais__superi__6F7569AA', 'membros', ['superior'], ['id'])
        batch_op.drop_index(batch_op.f('ix_oficiais_fk_superior_id'))
        batch_op.drop_index(batch_op.f('ix_oficiais_fk_cargo_oficial_id'))
        batch_op.create_index('ix_oficiais_superior', ['superior'], unique=False)
        batch_op.create_index('ix_oficiais_nome_cargo', ['nome_cargo'], unique=False)
        batch_op.drop_column('fk_cargo_oficial_id')
        batch_op.drop_column('fk_superior_id')
