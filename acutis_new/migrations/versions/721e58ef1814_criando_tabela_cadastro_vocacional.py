"""Criando tabela cadastro vocacional

Revision ID: 721e58ef1814
Revises: 902401750ce0
Create Date: 2025-03-14 02:18:32.650719

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '721e58ef1814'
down_revision = '902401750ce0'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('cadastros_vocacional',
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('fk_usuario_vocacional_id', sa.Uuid(), nullable=False),
    sa.Column('fk_endereco_id', sa.Uuid(), nullable=False),
    sa.Column('data_nascimento', sa.Date(), nullable=False),
    sa.Column('documento_identidade', sa.String(), nullable=False),
    sa.Column('criado_em', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('atualizado_em', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.ForeignKeyConstraint(['fk_endereco_id'], ['enderecos.id'], ),
    sa.ForeignKeyConstraint(['fk_usuario_vocacional_id'], ['usuarios_vocacional.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('cadastros_vocacional', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_cadastros_vocacional_fk_endereco_id'), ['fk_endereco_id'], unique=False)
        batch_op.create_index(batch_op.f('ix_cadastros_vocacional_fk_usuario_vocacional_id'), ['fk_usuario_vocacional_id'], unique=True)
        batch_op.create_index(batch_op.f('ix_cadastros_vocacional_id'), ['id'], unique=False)



def downgrade():
    with op.batch_alter_table('cadastros_vocacional', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_cadastros_vocacional_id'))
        batch_op.drop_index(batch_op.f('ix_cadastros_vocacional_fk_usuario_vocacional_id'))
        batch_op.drop_index(batch_op.f('ix_cadastros_vocacional_fk_endereco_id'))

    op.drop_table('cadastros_vocacional')
