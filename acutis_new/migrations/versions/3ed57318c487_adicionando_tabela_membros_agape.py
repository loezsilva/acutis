"""adicionando tabela membros agape

Revision ID: 3ed57318c487
Revises: 4bf23a17cef9
Create Date: 2025-04-11 18:29:40.339338

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3ed57318c487'
down_revision = '4bf23a17cef9'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('membros_agape',
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('fk_familia_agape_id', sa.Uuid(), nullable=False),
    sa.Column('responsavel', sa.Boolean(), nullable=False),
    sa.Column('nome', sa.String(), nullable=False),
    sa.Column('email', sa.String(), nullable=True),
    sa.Column('telefone', sa.String(), nullable=True),
    sa.Column('cpf', sa.String(length=14), nullable=True),
    sa.Column('data_nascimento', sa.Date(), nullable=False),
    sa.Column('funcao_familiar', sa.String(), nullable=False),
    sa.Column('escolaridade', sa.String(), nullable=False),
    sa.Column('ocupacao', sa.String(), nullable=False),
    sa.Column('renda', sa.Numeric(precision=15, scale=2), nullable=True),
    sa.Column('foto_documento', sa.String(), nullable=True),
    sa.Column('beneficiario_assistencial', sa.Boolean(), nullable=False),
    sa.Column('criado_em', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('atualizado_em', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.ForeignKeyConstraint(['fk_familia_agape_id'], ['familias_agape.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('membros_agape', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_membros_agape_beneficiario_assistencial'), ['beneficiario_assistencial'], unique=False)
        batch_op.create_index(batch_op.f('ix_membros_agape_cpf'), ['cpf'], unique=False)
        batch_op.create_index(batch_op.f('ix_membros_agape_data_nascimento'), ['data_nascimento'], unique=False)
        batch_op.create_index(batch_op.f('ix_membros_agape_fk_familia_agape_id'), ['fk_familia_agape_id'], unique=False)
        batch_op.create_index(batch_op.f('ix_membros_agape_responsavel'), ['responsavel'], unique=False)



def downgrade():
    with op.batch_alter_table('membros_agape', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_membros_agape_responsavel'))
        batch_op.drop_index(batch_op.f('ix_membros_agape_fk_familia_agape_id'))
        batch_op.drop_index(batch_op.f('ix_membros_agape_data_nascimento'))
        batch_op.drop_index(batch_op.f('ix_membros_agape_cpf'))
        batch_op.drop_index(batch_op.f('ix_membros_agape_beneficiario_assistencial'))

    op.drop_table('membros_agape')
