"""criando tabela de leads

Revision ID: 592012181d55
Revises: 
Create Date: 2025-02-27 18:46:48.968808

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '592012181d55'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('leads',
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('nome', sa.String(length=100), nullable=False),
    sa.Column('email', sa.String(length=100), nullable=False),
    sa.Column('telefone', sa.String(), nullable=False),
    sa.Column('pais', sa.String(length=100), nullable=False),
    sa.Column('password_hashed', sa.String(length=500), nullable=False),
    sa.Column('ultimo_acesso', sa.DateTime(), nullable=True),
    sa.Column('status', sa.Boolean(), nullable=True),
    sa.Column('origem_cadastro', sa.String(length=50), nullable=False),
    sa.Column('criado_em', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('atualizado_em', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('leads', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_leads_email'), ['email'], unique=True)
        batch_op.create_index(batch_op.f('ix_leads_nome'), ['nome'], unique=False)
        batch_op.create_index(batch_op.f('ix_leads_pais'), ['pais'], unique=False)
        batch_op.create_index(batch_op.f('ix_leads_password_hashed'), ['password_hashed'], unique=False)
        batch_op.create_index(batch_op.f('ix_leads_status'), ['status'], unique=False)
        batch_op.create_index(batch_op.f('ix_leads_origem_cadastro'), ['origem_cadastro'], unique=False)



def downgrade():
    with op.batch_alter_table('leads', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_leads_origem_cadastro'))
        batch_op.drop_index(batch_op.f('ix_leads_status'))
        batch_op.drop_index(batch_op.f('ix_leads_password_hashed'))
        batch_op.drop_index(batch_op.f('ix_leads_pais'))
        batch_op.drop_index(batch_op.f('ix_leads_nome'))
        batch_op.drop_index(batch_op.f('ix_leads_email'))

    op.drop_table('leads')
