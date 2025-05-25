"""criando tabela de coordenada

Revision ID: 40d21293f22d
Revises: 846ec32a4fc4
Create Date: 2025-02-28 11:53:12.668732

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '40d21293f22d'
down_revision = '846ec32a4fc4'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('coordenadas',
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('fk_endereco_id', sa.Uuid(), nullable=False),
    sa.Column('latitude', sa.Float(), nullable=False),
    sa.Column('longitude', sa.Float(), nullable=False),
    sa.Column('latitude_ne', sa.Float(), nullable=False),
    sa.Column('longitude_ne', sa.Float(), nullable=False),
    sa.Column('latitude_so', sa.Float(), nullable=False),
    sa.Column('longitude_so', sa.Float(), nullable=False),
    sa.Column('criado_em', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('atualizado_em', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.ForeignKeyConstraint(['fk_endereco_id'], ['enderecos.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('coordenadas', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_coordenadas_fk_endereco_id'), ['fk_endereco_id'], unique=False)



def downgrade():
    with op.batch_alter_table('coordenadas', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_coordenadas_fk_endereco_id'))

    op.drop_table('coordenadas')
