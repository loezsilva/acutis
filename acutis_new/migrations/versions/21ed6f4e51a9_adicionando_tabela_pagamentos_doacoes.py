"""adicionando tabela pagamentos doacoes

Revision ID: 21ed6f4e51a9
Revises: 89d6dbcdd611
Create Date: 2025-04-11 19:50:12.496725

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '21ed6f4e51a9'
down_revision = '89d6dbcdd611'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('pagamentos_doacoes',
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('fk_doacao_id', sa.Uuid(), nullable=False),
    sa.Column('valor', sa.Float(), nullable=False),
    sa.Column('recorrente', sa.Boolean(), nullable=False),
    sa.Column('forma_pagamento', sa.Enum('pix', 'credito', 'boleto', name='formapagamentoenum'), nullable=False),
    sa.Column('codigo_ordem_pagamento', sa.String(length=100), nullable=True),
    sa.Column('anonimo', sa.Boolean(), nullable=False),
    sa.Column('gateway', sa.Enum('maxipago', 'mercado_pago', 'itau', name='gatewaypagamentoenum'), nullable=False),
    sa.Column('ativo', sa.Boolean(), nullable=False),
    sa.Column('criado_em', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('atualizado_em', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.ForeignKeyConstraint(['fk_doacao_id'], ['doacoes.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('pagamentos_doacoes', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_pagamentos_doacoes_anonimo'), ['anonimo'], unique=False)
        batch_op.create_index(batch_op.f('ix_pagamentos_doacoes_ativo'), ['ativo'], unique=False)
        batch_op.create_index(batch_op.f('ix_pagamentos_doacoes_codigo_ordem_pagamento'), ['codigo_ordem_pagamento'], unique=False)
        batch_op.create_index(batch_op.f('ix_pagamentos_doacoes_fk_doacao_id'), ['fk_doacao_id'], unique=False)
        batch_op.create_index(batch_op.f('ix_pagamentos_doacoes_forma_pagamento'), ['forma_pagamento'], unique=False)
        batch_op.create_index(batch_op.f('ix_pagamentos_doacoes_gateway'), ['gateway'], unique=False)
        batch_op.create_index(batch_op.f('ix_pagamentos_doacoes_recorrente'), ['recorrente'], unique=False)



def downgrade():
    with op.batch_alter_table('pagamentos_doacoes', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_pagamentos_doacoes_recorrente'))
        batch_op.drop_index(batch_op.f('ix_pagamentos_doacoes_gateway'))
        batch_op.drop_index(batch_op.f('ix_pagamentos_doacoes_forma_pagamento'))
        batch_op.drop_index(batch_op.f('ix_pagamentos_doacoes_fk_doacao_id'))
        batch_op.drop_index(batch_op.f('ix_pagamentos_doacoes_codigo_ordem_pagamento'))
        batch_op.drop_index(batch_op.f('ix_pagamentos_doacoes_ativo'))
        batch_op.drop_index(batch_op.f('ix_pagamentos_doacoes_anonimo'))

    op.drop_table('pagamentos_doacoes')
