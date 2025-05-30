from flask import Flask

from .admin_benfeitores import admin_benfeitores_bp
from .admin_campanhas import admin_campanha_bp
from .admin_cargos_oficiais import admin_cargos_oficiais_bp
from .admin_doacoes import admin_doacoes_bp
from .admin_exportar_dados import admin_exportar_dados_bp
from .admin_graficos_cadastros import admin_graficos_cadastros_bp
from .admin_membros import admin_membros_bp
from .admin_membros_oficiais import admin_membros_oficiais
from .agape import agape_bp
from .autenticacao import autenticacao_bp
from .doacoes import doacoes_bp
from .enderecos import enderecos_bp
from .lives import lives_bp
from .membros import membros_bp
from .membros_oficiais import membros_oficiais_bp
from .rotas_publicas import rotas_publicas_bp
from .vocacional import vocacional_bp
from .webhooks import webhooks_bp

blueprints = [
    admin_benfeitores_bp,
    admin_campanha_bp,
    admin_cargos_oficiais_bp,
    admin_doacoes_bp,
    admin_exportar_dados_bp,
    admin_graficos_cadastros_bp,
    admin_membros_bp,
    admin_membros_oficiais,
    autenticacao_bp,
    doacoes_bp,
    enderecos_bp,
    membros_oficiais_bp,
    membros_bp,
    rotas_publicas_bp,
    vocacional_bp,
    webhooks_bp,
    lives_bp,
    agape_bp,
]


def initialize_routes(app: Flask):
    for bp in blueprints:
        app.register_blueprint(bp, url_prefix=f'/api{bp.url_prefix}')
