"""adicionando tabela processamentos doacoes

Revision ID: 37680b47262b
Revises: 21ed6f4e51a9
Create Date: 2025-04-11 19:54:35.745214

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '37680b47262b'
down_revision = '21ed6f4e51a9'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('processamentos_doacoes',
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('fk_pagamento_doacao_id', sa.Uuid(), nullable=False),
    sa.Column('forma_pagamento', sa.Enum('pix', 'credito', 'boleto', name='formapagamentoenum'), nullable=False),
    sa.Column('processado_em', sa.DateTime(), nullable=True),
    sa.Column('codigo_referencia', sa.String(), nullable=True),
    sa.Column('codigo_transacao', sa.String(), nullable=True),
    sa.Column('codigo_comprovante', sa.String(), nullable=True),
    sa.Column('nosso_numero', sa.String(), nullable=True),
    sa.Column('status', sa.Enum('pendente', 'pago', 'expirado', 'estornado', name='statusprocessamentoenum'), nullable=False),
    sa.Column('criado_em', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('atualizado_em', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.ForeignKeyConstraint(['fk_pagamento_doacao_id'], ['pagamentos_doacoes.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('processamentos_doacoes', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_processamentos_doacoes_fk_pagamento_doacao_id'), ['fk_pagamento_doacao_id'], unique=False)
        batch_op.create_index(batch_op.f('ix_processamentos_doacoes_forma_pagamento'), ['forma_pagamento'], unique=False)
        batch_op.create_index(batch_op.f('ix_processamentos_doacoes_status'), ['status'], unique=False)



def downgrade():
    with op.batch_alter_table('processamentos_doacoes', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_processamentos_doacoes_status'))
        batch_op.drop_index(batch_op.f('ix_processamentos_doacoes_forma_pagamento'))
        batch_op.drop_index(batch_op.f('ix_processamentos_doacoes_fk_pagamento_doacao_id'))

    op.drop_table('processamentos_doacoes')
