"""Criando tabela sacramento vocacional

Revision ID: f8b70e21a413
Revises: fb4a0195bae9
Create Date: 2025-03-14 02:46:13.460551

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f8b70e21a413'
down_revision = 'fb4a0195bae9'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('sacramentos_vocacional',
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('fk_ficha_vocacional_id', sa.Uuid(), nullable=False),
    sa.Column('nome', sa.Enum('batismo', 'crisma', 'eucaristia', 'penitencia', 'uncao_dos_enfermos', 'ordem', 'matrimonio', name='vocationalsacramentsenum'), nullable=False),
    sa.Column('criado_em', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('atualizado_em', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.ForeignKeyConstraint(['fk_ficha_vocacional_id'], ['fichas_vocacional.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('sacramentos_vocacional', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_sacramentos_vocacional_fk_ficha_vocacional_id'), ['fk_ficha_vocacional_id'], unique=False)
        batch_op.create_index(batch_op.f('ix_sacramentos_vocacional_id'), ['id'], unique=False)



def downgrade():
    with op.batch_alter_table('sacramentos_vocacional', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_sacramentos_vocacional_id'))
        batch_op.drop_index(batch_op.f('ix_sacramentos_vocacional_fk_ficha_vocacional_id'))

    op.drop_table('sacramentos_vocacional')
