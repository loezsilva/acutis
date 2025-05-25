"""adicionado tabela de campos adicionais

Revision ID: dc259e8a6a98
Revises: 908e75a86ec9
Create Date: 2025-02-28 15:22:36.480740

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dc259e8a6a98'
down_revision = '908e75a86ec9'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('campos_adicionais',
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('fk_campanha_id', sa.Uuid(), nullable=False),
    sa.Column('nome_campo', sa.String(), nullable=False),
    sa.Column('tipo_campo', sa.Enum('string', 'integer', 'float', 'date', 'datetime', 'arquivo', 'imagem', name='tiposcampoenum'), nullable=False),
    sa.Column('obrigatorio', sa.Boolean(), nullable=False),
    sa.Column('criado_em', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('atualizado_em', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.ForeignKeyConstraint(['fk_campanha_id'], ['campanhas.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('campos_adicionais', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_campos_adicionais_fk_campanha_id'), ['fk_campanha_id'], unique=False)



def downgrade():
    with op.batch_alter_table('campos_adicionais', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_campos_adicionais_fk_campanha_id'))

    op.drop_table('campos_adicionais')
