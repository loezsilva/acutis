"""cria modelos de permissoes
Revision ID: 73fefac0cf5c
Revises: 67f3f5e71cca
Create Date: 2025-05-30 15:52:14.607097
"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '73fefac0cf5c'
down_revision = '67f3f5e71cca'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('menus_sistema',
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('nome', sa.String(length=100), nullable=False),
    sa.Column('descricao', sa.String(length=255), nullable=True),
    sa.Column('criado_em', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('atualizado_em', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('nome')
    )
    op.create_table('perfis',
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('nome', sa.String(length=100), nullable=False),
    sa.Column('status', sa.Boolean(), nullable=False),
    sa.Column('super_perfil', sa.Boolean(), nullable=False),
    sa.Column('criado_em', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('atualizado_em', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('perfis', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_perfis_nome'), ['nome'], unique=False)

    op.create_table('permissoes_lead',
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('lead_id', sa.Uuid(), nullable=False),
    sa.Column('perfil_id', sa.Uuid(), nullable=False),
    sa.Column('criado_em', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('atualizado_em', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.ForeignKeyConstraint(['lead_id'], ['leads.id'], ),
    sa.ForeignKeyConstraint(['perfil_id'], ['perfis.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('permissoes_lead', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_permissoes_lead_lead_id'), ['lead_id'], unique=False)
        batch_op.create_index(batch_op.f('ix_permissoes_lead_perfil_id'), ['perfil_id'], unique=False)

    op.create_table('permissoes_menu',
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('perfil_id', sa.Uuid(), nullable=False),
    sa.Column('menu_id', sa.Uuid(), nullable=False),
    sa.Column('acessar', sa.Boolean(), nullable=False),
    sa.Column('criar', sa.Boolean(), nullable=False),
    sa.Column('editar', sa.Boolean(), nullable=False),
    sa.Column('deletar', sa.Boolean(), nullable=False),
    sa.Column('criado_em', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('atualizado_em', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.ForeignKeyConstraint(['menu_id'], ['menus_sistema.id'], ),
    sa.ForeignKeyConstraint(['perfil_id'], ['perfis.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('permissoes_menu', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_permissoes_menu_menu_id'), ['menu_id'], unique=False)
        batch_op.create_index(batch_op.f('ix_permissoes_menu_perfil_id'), ['perfil_id'], unique=False)


def downgrade():

    with op.batch_alter_table('permissoes_menu', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_permissoes_menu_perfil_id'))
        batch_op.drop_index(batch_op.f('ix_permissoes_menu_menu_id'))

    op.drop_table('permissoes_menu')
    with op.batch_alter_table('permissoes_lead', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_permissoes_lead_perfil_id'))
        batch_op.drop_index(batch_op.f('ix_permissoes_lead_lead_id'))

    op.drop_table('permissoes_lead')
    with op.batch_alter_table('perfis', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_perfis_nome'))

    op.drop_table('perfis')
    op.drop_table('menus_sistema')
    # ### end Alembic commands ###