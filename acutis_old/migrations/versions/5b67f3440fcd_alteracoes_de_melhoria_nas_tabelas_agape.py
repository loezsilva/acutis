"""alteracoes de melhoria nas tabelas agape

Revision ID: 5b67f3440fcd
Revises: edb110e7b33f
Create Date: 2025-04-07 11:08:42.309969

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5b67f3440fcd'
down_revision = 'edb110e7b33f'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('fotos_familias_agape',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('fk_familia_agape_id', sa.Integer(), nullable=False),
    sa.Column('foto', sa.String(length=100), nullable=False),
    sa.Column('criado_em', sa.DateTime(), nullable=True),
    sa.Column('atualizado_em', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['fk_familia_agape_id'], ['familia_agape.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('fotos_familias_agape', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_fotos_familias_agape_criado_em'), ['criado_em'], unique=False)
        batch_op.create_index(batch_op.f('ix_fotos_familias_agape_fk_familia_agape_id'), ['fk_familia_agape_id'], unique=False)

    with op.batch_alter_table('familia_agape', schema=None) as batch_op:
        batch_op.add_column(sa.Column('comprovante_residencia', sa.String(length=100), nullable=True))
        batch_op.drop_column('foto')

    with op.batch_alter_table('membro_agape', schema=None) as batch_op:
        batch_op.add_column(sa.Column('foto_documento', sa.String(length=100), nullable=True))
        batch_op.add_column(sa.Column('beneficiario_assistencial', sa.Boolean(), nullable=True))
        batch_op.alter_column('renda',
               existing_type=sa.NUMERIC(precision=15, scale=2),
               nullable=True)
        batch_op.create_index(batch_op.f('ix_membro_agape_beneficiario_assistencial'), ['beneficiario_assistencial'], unique=False)


def downgrade():
    with op.batch_alter_table('membro_agape', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_membro_agape_beneficiario_assistencial'))
        batch_op.alter_column('renda',
               existing_type=sa.NUMERIC(precision=15, scale=2),
               nullable=False)
        batch_op.drop_column('beneficiario_assistencial')
        batch_op.drop_column('foto_documento')

    with op.batch_alter_table('familia_agape', schema=None) as batch_op:
        batch_op.add_column(sa.Column('foto', sa.VARCHAR(length=100, collation='SQL_Latin1_General_CP1_CI_AS'), autoincrement=False, nullable=True))
        batch_op.drop_column('comprovante_residencia')

    with op.batch_alter_table('fotos_familias_agape', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_fotos_familias_agape_fk_familia_agape_id'))
        batch_op.drop_index(batch_op.f('ix_fotos_familias_agape_criado_em'))

    op.drop_table('fotos_familias_agape')
