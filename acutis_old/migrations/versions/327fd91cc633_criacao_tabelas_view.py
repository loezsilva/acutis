"""criacao_tabelas_view

Revision ID: 327fd91cc633
Revises: 030c6d00c812
Create Date: 2024-07-22 17:33:32.362768

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '327fd91cc633'
down_revision = '030c6d00c812'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('view_canais_youtube',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('tag', sa.String(length=100), nullable=False),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('view_lives',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('titulo', sa.String(length=255), nullable=False),
                    sa.Column('fk_campanha_id', sa.Integer(), nullable=True),
                    sa.Column('rede_social', sa.String(
                        length=50), nullable=False),
                    sa.Column('fk_view_canal_youtube_id',
                              sa.Integer(), nullable=True),
                    sa.ForeignKeyConstraint(
                        ['fk_campanha_id'], ['campanha.id'], ),
                    sa.ForeignKeyConstraint(['fk_view_canal_youtube_id'], [
                        'view_canais_youtube.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('view_audiencias',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('fk_view_live_id', sa.Integer(), nullable=True),
                    sa.Column('data_hora_registro',
                              sa.DateTime(), nullable=True),
                    sa.Column('audiencia', sa.Integer(), nullable=False),
                    sa.ForeignKeyConstraint(
                        ['fk_view_live_id'], ['view_lives.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('view_avulsas',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('data_hora_inicio',
                              sa.DateTime(), nullable=False),
                    sa.Column('data_hora_fim', sa.DateTime(), nullable=False),
                    sa.Column('fk_view_live_id', sa.Integer(), nullable=True),
                    sa.ForeignKeyConstraint(
                        ['fk_view_live_id'], ['view_lives.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('view_recorrentes',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('dia_semana', sa.String(
                        length=50), nullable=False),
                    sa.Column('hora_inicio', sa.Time(), nullable=False),
                    sa.Column('hora_fim', sa.Time(), nullable=False),
                    sa.Column('fk_view_live_id', sa.Integer(), nullable=True),
                    sa.ForeignKeyConstraint(
                        ['fk_view_live_id'], ['view_lives.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    # with op.batch_alter_table('foto_campanha', schema=None) as batch_op:
    #     batch_op.drop_constraint('FK__foto_camp__fk_la__5EDF0F2E', type_='foreignkey')
    #     batch_op.drop_column('fk_landpage_id')

    # with op.batch_alter_table('historico_campanha_doacoes', schema=None) as batch_op:
    #     batch_op.drop_constraint('FK__historico__fk_ca__04459E07', type_='foreignkey')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('historico_campanha_doacoes', schema=None) as batch_op:
        batch_op.create_foreign_key('FK__historico__fk_ca__04459E07', 'campanha', [
                                    'fk_campanha_id'], ['id'])

    with op.batch_alter_table('foto_campanha', schema=None) as batch_op:
        batch_op.add_column(
            sa.Column('fk_landpage_id', sa.INTEGER(), autoincrement=False, nullable=True))
        batch_op.create_foreign_key('FK__foto_camp__fk_la__5EDF0F2E', 'landpage', [
                                    'fk_landpage_id'], ['id'])

    op.drop_table('view_recorrentes')
    op.drop_table('view_avulsas')
    op.drop_table('view_audiencias')
    op.drop_table('view_lives')
    op.drop_table('view_canais_youtube')
    # ### end Alembic commands ###
