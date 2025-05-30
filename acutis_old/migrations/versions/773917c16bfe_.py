"""empty message

Revision ID: 773917c16bfe
Revises: 1becfa82cdd6
Create Date: 2023-10-10 10:31:44.763358

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '773917c16bfe'
down_revision = '1becfa82cdd6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('cargo',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nome', sa.String(length=100), nullable=False),
    sa.Column('descricao', sa.String(length=255), nullable=True),
    sa.Column('superior', sa.Integer(), nullable=True),
    sa.Column('data_criacao', sa.DateTime(), nullable=True),
    sa.Column('usuario_criacao', sa.Integer(), nullable=False),
    sa.Column('data_alteracao', sa.DateTime(), nullable=True),
    sa.Column('usuario_alteracao', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['superior'], ['cargo.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('cargo_usuario',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('fk_usuario_id', sa.Integer(), nullable=False),
    sa.Column('fk_cargo_id', sa.Integer(), nullable=False),
    sa.Column('fk_usuario_superior_id', sa.Integer(), nullable=True),
    sa.Column('convite', sa.SmallInteger(), nullable=False),
    sa.Column('data_convite_aceito', sa.DateTime(), nullable=True),
    sa.Column('usuario_convite_aceito', sa.Integer(), nullable=True),
    sa.Column('data_criacao', sa.DateTime(), nullable=True),
    sa.Column('usuario_criacao', sa.Integer(), nullable=False),
    sa.Column('data_alteracao', sa.DateTime(), nullable=True),
    sa.Column('usuario_alteracao', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['fk_cargo_id'], ['cargo.id'], ),
    sa.ForeignKeyConstraint(['fk_usuario_id'], ['usuario.id'], ),
    sa.ForeignKeyConstraint(['fk_usuario_superior_id'], ['usuario.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('landpage',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('campanha_id', sa.Integer(), nullable=True),
    sa.Column('background', sa.String(length=100), nullable=False),
    sa.Column('banner', sa.String(length=100), nullable=False),
    sa.Column('titulo', sa.String(length=100), nullable=False),
    sa.Column('descricao', sa.UnicodeText(), nullable=False),
    sa.Column('tipo_cadastro', sa.String(length=50), nullable=False),
    sa.Column('url', sa.String(), nullable=False),
    sa.Column('data_criacao', sa.DateTime(), nullable=True),
    sa.Column('usuario_criacao', sa.Integer(), nullable=False),
    sa.Column('data_alteracao', sa.DateTime(), nullable=True),
    sa.Column('usuario_alteracao', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['campanha_id'], ['campanha.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('conteudo_landpage',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('landpage_id', sa.Integer(), nullable=False),
    sa.Column('imagem', sa.String(length=100), nullable=False),
    sa.Column('html', sa.UnicodeText(), nullable=False),
    sa.Column('data_criacao', sa.DateTime(), nullable=True),
    sa.Column('usuario_criacao', sa.Integer(), nullable=False),
    sa.Column('data_alteracao', sa.DateTime(), nullable=True),
    sa.Column('usuario_alteracao', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['landpage_id'], ['landpage.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('pedido', schema=None) as batch_op:
        batch_op.alter_column('order_id',
               existing_type=sa.VARCHAR(length=100, collation='SQL_Latin1_General_CP1_CI_AS'),
               nullable=True)

    with op.batch_alter_table('usuario', schema=None) as batch_op:
        batch_op.add_column(sa.Column('avatar', sa.String(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('usuario', schema=None) as batch_op:
        batch_op.drop_column('avatar')

    with op.batch_alter_table('pedido', schema=None) as batch_op:
        batch_op.alter_column('order_id',
               existing_type=sa.VARCHAR(length=100, collation='SQL_Latin1_General_CP1_CI_AS'),
               nullable=False)

    op.drop_table('conteudo_landpage')
    op.drop_table('landpage')
    op.drop_table('cargo_usuario')
    op.drop_table('cargo')
    # ### end Alembic commands ###
