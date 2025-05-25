from flask import request
from flask_jwt_extended import current_user
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func

from models.campanha import Campanha
from models.clifor import Clifor
from models.forma_pagamento import FormaPagamento
from models.pedido import Pedido
from models.processamento_pedido import ProcessamentoPedido
from services.file_service import FileService


class GetAllUserDonations:
    def __init__(self, database: SQLAlchemy, file_service: FileService) -> None:
        self.__database = database
        self.__file_service = file_service
        self.__page = request.args.get("page", 1, type=int)
        self.__per_page = request.args.get("per_page", 10, type=int)

    def execute(self):
        clifor_id = current_user["fk_clifor_id"]

        doacoes_query = self.__get_user_donations_query(clifor_id)
        doacoes, total = self.__paginate_query(doacoes_query)
        response = self.__prepare_response(doacoes, total)
        return response, 200

    def __get_user_donations_query(self, clifor_id: int):
        doacoes_query = (
            self.__database.session.query(
                func.distinct(Pedido.id).label("id"),
                Pedido.periodicidade.label("recorrencia"),
                Pedido.recorrencia_ativa,
                Pedido.data_pedido.label("data_doacao"),
                Pedido.valor_total_pedido.label("valor_doacao"),
                FormaPagamento.descricao.label("forma_pagamento"),
                Campanha.titulo,
                Campanha.descricao,
                Campanha.filename,
            )
            .select_from(Pedido)
            .join(ProcessamentoPedido, Pedido.id == ProcessamentoPedido.fk_pedido_id)
            .join(Campanha, Campanha.id == Pedido.fk_campanha_id)
            .join(Clifor, Clifor.id == Pedido.fk_clifor_id)
            .join(FormaPagamento, FormaPagamento.id == Pedido.fk_forma_pagamento_id)
            .filter(Clifor.id == clifor_id)
            .order_by(Pedido.data_pedido.desc())
        )

        return doacoes_query

    def __paginate_query(self, query):
        query_pagination = query.paginate(
            page=self.__page, per_page=self.__per_page, error_out=False
        )
        items, total = query_pagination.items, query_pagination.total
        return items, total

    def __get_campaign_image(self, filename: str) -> str:
        image_url = self.__file_service.get_public_url(object_name=filename)
        return image_url

    def __prepare_response(self, doacoes: list[Pedido], total: int) -> dict:
        response = {
            "page": self.__page,
            "total": total,
            "doacoes": [
                {
                    "id": doacao.id,
                    "recorrencia": "Única" if doacao.recorrencia == 1 else "Recorrente",
                    "recorrencia_ativa": doacao.recorrencia_ativa,
                    "data_doacao": (
                        doacao.data_doacao.strftime("%d/%m/%Y")
                        if doacao.data_doacao
                        else None
                    ),
                    "valor_doacao": round(doacao.valor_doacao, 2),
                    "forma_pagamento": doacao.forma_pagamento,
                    "titulo": doacao.titulo,
                    "descricao": doacao.descricao,
                    "imagem_campanha": self.__get_campaign_image(doacao.filename),
                }
                for doacao in doacoes
            ],
        }
        return response
