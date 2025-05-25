"""criando tabela de membros

Revision ID: 846ec32a4fc4
Revises: d12540cc9ddb
Create Date: 2025-02-28 10:52:57.929827

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '846ec32a4fc4'
down_revision = 'd12540cc9ddb'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('membros',
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('fk_lead_id', sa.Uuid(), nullable=False),
    sa.Column('fk_benfeitor_id', sa.Uuid(), nullable=True),
    sa.Column('fk_endereco_id', sa.Uuid(), nullable=False),
    sa.Column('nome_social', sa.String(), nullable=True),
    sa.Column('data_nascimento', sa.Date(), nullable=True),
    sa.Column('sexo', sa.Enum('masculino', 'feminino', name='sexoenum'), nullable=True),
    sa.Column('foto', sa.String(), nullable=True),
    sa.Column('criado_em', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('atualizado_em', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.ForeignKeyConstraint(['fk_benfeitor_id'], ['benfeitores.id'], ),
    sa.ForeignKeyConstraint(['fk_endereco_id'], ['enderecos.id'], ),
    sa.ForeignKeyConstraint(['fk_lead_id'], ['leads.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('membros', schema=None) as batch_op:
        batch_op.create_index('ix_membros_fk_benfeitor_id', ['fk_benfeitor_id'], unique=True, mssql_where=sa.text('fk_benfeitor_id IS NOT NULL'))
        batch_op.create_index(batch_op.f('ix_membros_fk_endereco_id'), ['fk_endereco_id'], unique=True)
        batch_op.create_index(batch_op.f('ix_membros_fk_lead_id'), ['fk_lead_id'], unique=True)



def downgrade():
    with op.batch_alter_table('membros', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_membros_fk_lead_id'))
        batch_op.drop_index(batch_op.f('ix_membros_fk_endereco_id'))
        batch_op.drop_index('ix_membros_fk_benfeitor_id', mssql_where=sa.text('fk_benfeitor_id IS NOT NULL'))

    op.drop_table('membros')
