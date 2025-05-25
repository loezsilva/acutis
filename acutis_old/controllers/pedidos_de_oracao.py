from flask import Blueprint, request
from flask_jwt_extended import current_user, jwt_required
from spectree import Response
from models import PedidosDeOracao
from builder import db, api
import logging
from datetime import datetime, timedelta
from models.pedidos_de_oracao import SchemaPedidoDeOracao
from utils.response import DefaultResponseSchema, DefaultErrorResponseSchema

pedidos_de_oracao = Blueprint(
    "pedidos_de_oracao", __name__, url_prefix="/pedidos-de-oracao"
)


@pedidos_de_oracao.post("")
@api.validate(
    json=SchemaPedidoDeOracao,
    resp=Response(
        HTTP_201=DefaultResponseSchema,
        HTTP_400=DefaultErrorResponseSchema,
        HTTP_403=DefaultErrorResponseSchema,
        HTTP_500=DefaultErrorResponseSchema,
    ),
    tags=["Pedidos de oração"],
)
@jwt_required()
def create_pedido():
    """Permite o usuário criar pedido de oração."""
    try:
        if current_user["fk_perfil_id"] != 1:
            return {
                "error": "Você não tem permissão para realizar esta ação."
            }, 403

        payload = request.get_json()

        requireds = [
            "autor",
            "fk_usuario_criacao",
            "destinado",
            "dados_publicos",
            "descricao_pedido",
            "leitura_publica",
        ]

        for camp in requireds:
            if camp not in payload:
                return {"error": f"O campo {camp} não pode ser nulo!"}, 400

        autor = payload.get("autor")
        destinado = payload.get("destinado")
        dados_publicos = payload.get("dados_publicos")
        descricao_pedido = payload.get("descricao_pedido")
        leitura_publica = payload.get("leitura_publica")
        fk_usuario_criacao = payload.get("fk_usuario_criacao")

        new_pedido_de_oracao = PedidosDeOracao(
            fk_usuario_criacao=fk_usuario_criacao,
            autor=autor,
            destinado=destinado,
            dados_publicos=dados_publicos,
            descricao_pedido=descricao_pedido,
            leitura_publica=leitura_publica,
            created_at=datetime.now(),
        )

        db.session.add(new_pedido_de_oracao)

        try:
            db.session.commit()
            return {"msg": "Pedido de oração criado com sucesso!"}, 201
        except Exception as e:
            logging.error(f"{type(e)} - {e}")
            db.session.rollback()
            return {
                "error": f"Ocorreu um error ao salvar pedido de oração! {e}"
            }, 500
    except Exception as e:
        return {
            "error": f"Ocorreu um error ao criar pedido de oração. {e}"
        }, 500


@pedidos_de_oracao.put("/admin/<int:id>")
@api.validate(
    json=SchemaPedidoDeOracao,
    resp=Response(
        HTTP_200=DefaultResponseSchema,
        HTTP_400=DefaultErrorResponseSchema,
        HTTP_403=DefaultErrorResponseSchema,
        HTTP_404=DefaultErrorResponseSchema,
        HTTP_500=DefaultErrorResponseSchema,
    ),
    tags=["Pedidos de oração"],
)
@jwt_required()
def update_pedido(id):
    """Permite o usuário atualizar um pedido de oração existente."""
    try:
        if current_user["fk_perfil_id"] != 1:
            return {
                "error": "Você não tem permissão para realizar esta ação."
            }, 403

        payload = request.get_json()

        requireds = [
            "autor",
            "destinado",
            "dados_publicos",
            "descricao_pedido",
            "leitura_publica",
        ]

        for camp in requireds:
            if camp not in payload:
                return {"error": f"O campo {camp} não pode ser nulo!"}, 400

        pedido = PedidosDeOracao.query.get(id)
        if not pedido:
            return {"error": "Pedido de oração não encontrado!"}, 404

        pedido.autor = payload.get("autor")
        pedido.destinado = payload.get("destinado")
        pedido.dados_publicos = payload.get("dados_publicos")
        pedido.descricao_pedido = payload.get("descricao_pedido")
        pedido.leitura_publica = payload.get("leitura_publica")
        pedido.local_realizacao = payload.get("local_realizacao")
        pedido.fk_usuario_criacao = payload.get("fk_usuario_criacao")
        pedido.status = "realizado"
        pedido.data_realizacao = datetime.now()

        try:
            db.session.commit()
            return {"msg": "Pedido de oração atualizado com sucesso!"}, 200
        except Exception as e:
            logging.error(f"{type(e)} - {e}")
            db.session.rollback()
            return {
                "error": f"Ocorreu um erro ao atualizar o pedido de oração! {e}"
            }, 500
    except Exception as e:
        return {
            "error": f"Ocorreu um erro ao atualizar o pedido de oração. {e}"
        }, 500


@pedidos_de_oracao.get("/admin")
@api.validate(
    query=None,
    resp=Response(
        HTTP_200=None,
        HTTP_400=DefaultErrorResponseSchema,
        HTTP_403=DefaultErrorResponseSchema,
        HTTP_404=DefaultErrorResponseSchema,
        HTTP_500=DefaultErrorResponseSchema,
    ),
    tags=["Pedidos de oração"],
)
@jwt_required()
def get_pedidos_de_oracao():
    try:
        if current_user["fk_perfil_id"] != 1:
            return {
                "error": "Você não tem permissão para realizar esta ação."
            }, 403

        per_page = request.args.get("per_page", 10, type=int)
        page = request.args.get("page", 1, type=int)
        filter_data_criacao = request.args.get("data_criacao", None, type=str)
        filter_data_realizacao = request.args.get(
            "data_realizacao", None, type=str
        )
        filter_status = request.args.get("status", None, type=str)

        query = PedidosDeOracao.query.order_by(
            db.asc(PedidosDeOracao.created_at)
        )

        if filter_status is not None:
            query = query.filter(PedidosDeOracao.status == filter_status)

        if filter_data_criacao is not None:
            try:
                filter_data_criacao = datetime.strptime(
                    filter_data_criacao, "%Y-%m-%d"
                )
                query = query.filter(
                    PedidosDeOracao.created_at >= filter_data_criacao,
                    PedidosDeOracao.created_at
                    < filter_data_criacao + timedelta(days=1),
                )
            except Exception as e:
                return {"error": "Formato de data inválido!"}, 400

        if filter_data_realizacao is not None:
            try:
                filter_data_realizacao = datetime.strptime(
                    filter_data_realizacao, "%Y-%m-%d"
                )
                query = query.filter(
                    PedidosDeOracao.data_realizacao >= filter_data_realizacao,
                    PedidosDeOracao.data_realizacao
                    < filter_data_realizacao + timedelta(days=1),
                )
            except Exception as e:
                return {"error": "Formato de data inválido!"}, 400

        pedidos = query.paginate(page=page, per_page=per_page, error_out=False)

        if pedidos.items is None or len(pedidos.items) == 0:
            return {"msg": "Nenhum pedido de oração encontrado."}, 200

        response = {
            "pedidos": [
                {
                    "fk_usuario_criacao": pedido.fk_usuario_criacao,
                    "pedido_id": pedido.id,
                    "autor": pedido.autor,
                    "destinado": pedido.destinado,
                    "dados_publicos": pedido.dados_publicos,
                    "leitura_publica": pedido.leitura_publica,
                    "dados_publicos": pedido.dados_publicos,
                    "status": pedido.status,
                    "local_realizacao": pedido.local_realizacao,
                    "data_realizacao": pedido.data_realizacao,
                    "criado_em": pedido.created_at,
                }
                for pedido in pedidos
            ],
            "pagination": {
                "total": pedidos.total,
                "pages": pedidos.pages,
                "page": pedidos.page,
                "per_page": pedidos.per_page,
            },
        }
        return response, 200
    except Exception as e:
        return {
            "error": f"Ocorreu um error ao listar pedidos de oração. {e}"
        }, 500


@pedidos_de_oracao.get("/me/<int:usuario_id>")
@jwt_required()
def get_pedidos_de_oracao_por_usuario(usuario_id):
    try:
        if current_user["fk_perfil_id"] != 1:
            return {
                "error": "Você não tem permissão para realizar esta ação."
            }, 403

        per_page = request.args.get("per_page", 10, type=int)
        page = request.args.get("page", 1, type=int)
        filter_data_criacao = request.args.get("data_criacao", None, type=str)
        filter_data_realizacao = request.args.get(
            "data_realizacao", None, type=str
        )
        filter_status = request.args.get("status", None, type=str)

        query = PedidosDeOracao.query.filter(
            PedidosDeOracao.fk_usuario_criacao == usuario_id
        ).order_by(db.asc(PedidosDeOracao.created_at))

        if filter_status is not None:
            query = query.filter(PedidosDeOracao.status == filter_status)

        if filter_data_criacao:
            try:
                data_criacao = datetime.strptime(
                    filter_data_criacao, "%Y-%m-%d"
                )
                query = query.filter(
                    PedidosDeOracao.created_at >= data_criacao,
                    PedidosDeOracao.created_at
                    < data_criacao + timedelta(days=1),
                )
            except ValueError:
                return {
                    "error": "Formato de data de criação inválido. Use o formato YYYY-MM-DD."
                }, 400

        if filter_data_realizacao:
            try:
                data_realizacao = datetime.strptime(
                    filter_data_realizacao, "%Y-%m-%d"
                )
                query = query.filter(
                    PedidosDeOracao.data_realizacao >= data_realizacao,
                    PedidosDeOracao.data_realizacao
                    < data_realizacao + timedelta(days=1),
                )
            except ValueError:
                return {
                    "error": "Formato de data de realização inválido. Use o formato YYYY-MM-DD."
                }, 400

        pedidos = query.paginate(page=page, per_page=per_page, error_out=False)

        if pedidos.items is None or len(pedidos.items) == 0:
            return {"msg": "nenhum pedido de oração encontrado."}, 200

        response = {
            "pedidos": [
                {
                    "pedido_id": pedido.id,
                    "autor": pedido.autor,
                    "destinado": pedido.destinado,
                    "dados_publicos": pedido.dados_publicos,
                    "leitura_publica": pedido.leitura_publica,
                    "status": pedido.status,
                    "local_realizacao": pedido.local_realizacao,
                    "data_realizacao": pedido.data_realizacao,
                    "criado_em": pedido.created_at,
                }
                for pedido in pedidos.items
            ],
            "pagination": {
                "total": pedidos.total,
                "pages": pedidos.pages,
                "page": pedidos.page,
                "per_page": pedidos.per_page,
            },
        }
        return response, 200
    except Exception as e:
        return {
            "error": f"Ocorreu um error ao listar pedidos de oração. {e}"
        }, 500
