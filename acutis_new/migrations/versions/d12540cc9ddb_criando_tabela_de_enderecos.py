"""criando tabela de enderecos

Revision ID: d12540cc9ddb
Revises: ae0be73980fc
Create Date: 2025-02-28 10:36:24.192705

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd12540cc9ddb'
down_revision = 'ae0be73980fc'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('enderecos',
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('codigo_postal', sa.String(), nullable=True),
    sa.Column('tipo_logradouro', sa.String(), nullable=True),
    sa.Column('logradouro', sa.String(), nullable=True),
    sa.Column('numero', sa.String(), nullable=True),
    sa.Column('complemento', sa.String(), nullable=True),
    sa.Column('bairro', sa.String(), nullable=True),
    sa.Column('cidade', sa.String(), nullable=True),
    sa.Column('estado', sa.String(), nullable=True),
    sa.Column('pais', sa.String(), nullable=True),
    sa.Column('obriga_atualizar_endereco', sa.Boolean(), nullable=True),
    sa.Column('criado_em', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('atualizado_em', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('enderecos', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_enderecos_obriga_atualizar_endereco'), ['obriga_atualizar_endereco'], unique=False)


def downgrade():
    with op.batch_alter_table('enderecos', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_enderecos_obriga_atualizar_endereco'))

    op.drop_table('enderecos')
