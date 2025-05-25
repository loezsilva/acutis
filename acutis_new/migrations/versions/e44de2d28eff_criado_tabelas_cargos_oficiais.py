"""criado tabelas cargos_oficiais

Revision ID: e44de2d28eff
Revises: f8b70e21a413
Create Date: 2025-03-17 13:34:08.055888

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e44de2d28eff'
down_revision = 'f8b70e21a413'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('cargos_oficiais',
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('nome_cargo', sa.String(length=50), nullable=False),
    sa.Column('criado_por', sa.Uuid(), nullable=False),
    sa.Column('criado_em', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('atualizado_por', sa.Uuid(), nullable=True),
    sa.Column('atualizado_em', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.ForeignKeyConstraint(['atualizado_por'], ['membros.id'], ),
    sa.ForeignKeyConstraint(['criado_por'], ['membros.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('nome_cargo')
    )
    with op.batch_alter_table('cargos_oficiais', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_cargos_oficiais_nome_cargo'), ['nome_cargo'], unique=True)
        batch_op.create_index(batch_op.f('ix_cargos_oficiais_id'), ['id'], unique=False)

    with op.batch_alter_table('campanhas', schema=None) as batch_op:
        batch_op.add_column(sa.Column('fk_cargo_oficial_id', sa.Uuid(), nullable=True))
        batch_op.add_column(sa.Column('superior_obrigatorio', sa.Boolean(), nullable=False))
        batch_op.create_index(batch_op.f('ix_campanhas_fk_cargo_oficial_id'), ['fk_cargo_oficial_id'], unique=False)
        batch_op.create_index(batch_op.f('ix_campanhas_superior_obrigatorio'), ['superior_obrigatorio'], unique=False)
        batch_op.create_foreign_key('FK__campanhas__cargos_oficiais__381bf0b6', 'cargos_oficiais', ['fk_cargo_oficial_id'], ['id'])



def downgrade():
    with op.batch_alter_table('campanhas', schema=None) as batch_op:
        batch_op.drop_constraint('FK__campanhas__cargos_oficiais__381bf0b6', type_='foreignkey')
        batch_op.drop_index(batch_op.f('ix_campanhas_superior_obrigatorio'))
        batch_op.drop_index(batch_op.f('ix_campanhas_fk_cargo_oficial_id'))
        batch_op.drop_column('superior_obrigatorio')
        batch_op.drop_column('fk_cargo_oficial_id')

    with op.batch_alter_table('cargos_oficiais', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_cargos_oficiais_id'))
        batch_op.drop_index(batch_op.f('ix_cargos_oficiais_nome_cargo'))

    op.drop_table('cargos_oficiais')
