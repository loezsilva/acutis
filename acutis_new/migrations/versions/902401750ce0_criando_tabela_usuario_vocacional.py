"""Criando tabela usuario vocacional

Revision ID: 902401750ce0
Revises: d5ea958175c6
Create Date: 2025-03-14 02:13:02.636668

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '902401750ce0'
down_revision = 'd5ea958175c6'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('usuarios_vocacional',
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('nome', sa.String(), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('telefone', sa.String(), nullable=False),
    sa.Column('genero', sa.Enum('masculino', 'feminino', name='vocationalgendersenum'), nullable=False),
    sa.Column('pais', sa.String(), nullable=False),
    sa.Column('criado_em', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('atualizado_em', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('usuarios_vocacional', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_usuarios_vocacional_email'), ['email'], unique=True)
        batch_op.create_index(batch_op.f('ix_usuarios_vocacional_id'), ['id'], unique=False)



def downgrade():
    with op.batch_alter_table('usuarios_vocacional', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_usuarios_vocacional_id'))
        batch_op.drop_index(batch_op.f('ix_usuarios_vocacional_email'))

    op.drop_table('usuarios_vocacional')
