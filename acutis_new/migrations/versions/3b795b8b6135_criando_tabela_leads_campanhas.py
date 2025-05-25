"""criando tabela leads campanhas

Revision ID: 3b795b8b6135
Revises: 036b9849ecb2
Create Date: 2025-03-06 11:51:18.080799

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3b795b8b6135'
down_revision = '036b9849ecb2'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('leads_campanhas',
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('fk_lead_id', sa.Uuid(), nullable=False),
    sa.Column('fk_campanha_id', sa.Uuid(), nullable=False),
    sa.Column('criado_em', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('atualizado_em', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.ForeignKeyConstraint(['fk_campanha_id'], ['campanhas.id'], ),
    sa.ForeignKeyConstraint(['fk_lead_id'], ['leads.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('leads_campanhas', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_leads_campanhas_fk_campanha_id'), ['fk_campanha_id'], unique=False)
        batch_op.create_index(batch_op.f('ix_leads_campanhas_fk_lead_id'), ['fk_lead_id'], unique=False)



def downgrade():
    with op.batch_alter_table('leads_campanhas', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_leads_campanhas_fk_lead_id'))
        batch_op.drop_index(batch_op.f('ix_leads_campanhas_fk_campanha_id'))

    op.drop_table('leads_campanhas')
