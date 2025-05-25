"""adicionado tabela de metadados de leads

Revision ID: 7993552d764b
Revises: dc259e8a6a98
Create Date: 2025-02-28 15:30:43.868881

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7993552d764b'
down_revision = 'dc259e8a6a98'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('metadados_leads',
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('fk_lead_id', sa.Uuid(), nullable=False),
    sa.Column('fk_campo_adicional_id', sa.Uuid(), nullable=False),
    sa.Column('valor_campo', sa.UnicodeText(), nullable=False),
    sa.Column('criado_em', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('atualizado_em', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.ForeignKeyConstraint(['fk_campo_adicional_id'], ['campos_adicionais.id'], ),
    sa.ForeignKeyConstraint(['fk_lead_id'], ['leads.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('metadados_leads', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_metadados_leads_fk_campo_adicional_id'), ['fk_campo_adicional_id'], unique=False)
        batch_op.create_index(batch_op.f('ix_metadados_leads_fk_lead_id'), ['fk_lead_id'], unique=False)



def downgrade():
    with op.batch_alter_table('metadados_leads', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_metadados_leads_fk_lead_id'))
        batch_op.drop_index(batch_op.f('ix_metadados_leads_fk_campo_adicional_id'))

    op.drop_table('metadados_leads')
