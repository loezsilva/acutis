"""criando tabela de oficiais

Revision ID: 9380decda06c
Revises: 40d21293f22d
Create Date: 2025-02-28 12:18:02.179261

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9380decda06c'
down_revision = '40d21293f22d'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('oficiais',
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('fk_membro_id', sa.Uuid(), nullable=False),
    sa.Column('superior', sa.Uuid(), nullable=True),
    sa.Column('nome_cargo', sa.Enum('general', 'marechal', name='cargosenum'), nullable=False),
    sa.Column('status', sa.Enum('aprovado', 'pendente', 'recusado', name='statusoficialenum'), nullable=False),
    sa.Column('criado_em', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('atualizado_em', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.ForeignKeyConstraint(['fk_membro_id'], ['membros.id'], ),
    sa.ForeignKeyConstraint(['superior'], ['membros.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('oficiais', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_oficiais_fk_membro_id'), ['fk_membro_id'], unique=True)
        batch_op.create_index(batch_op.f('ix_oficiais_nome_cargo'), ['nome_cargo'], unique=False)
        batch_op.create_index(batch_op.f('ix_oficiais_status'), ['status'], unique=False)
        batch_op.create_index(batch_op.f('ix_oficiais_superior'), ['superior'], unique=False)



def downgrade():
    with op.batch_alter_table('oficiais', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_oficiais_superior'))
        batch_op.drop_index(batch_op.f('ix_oficiais_status'))
        batch_op.drop_index(batch_op.f('ix_oficiais_nome_cargo'))
        batch_op.drop_index(batch_op.f('ix_oficiais_fk_membro_id'))

    op.drop_table('oficiais')
