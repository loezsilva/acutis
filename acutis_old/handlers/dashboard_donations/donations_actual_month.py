from flask import request
from flask_sqlalchemy import SQLAlchemy

from exceptions.error_types.http_bad_request import BadRequestError
from models.campanha import Campanha
from models.pedido import Pedido
from models.processamento_pedido import ProcessamentoPedido
from utils.functions import get_current_time


class DonationsActualMonth:
    def __init__(self, conn: SQLAlchemy) -> None:
        self.__conn = conn
        self.__http_args = request.args
        self.__campanha_id = self.__http_args.get("fk_campanha_id")        
        self.__forma_pagamento = self.__http_args.get("forma_pagamento", None, type=int)
        
        self.__visualizar_por = self.__http_args.get("visualizar_por", "total", type=str)
    
    def execute(self):
        return self.__type_of_visualization(self.__visualizar_por)
        
    def __type_of_visualization(self, type: str):
        
        types = ["total", "campanha"]
        
        if type not in types:
            raise BadRequestError("Tipo de visualização não suportado")
        
        if type == "total":
            return self.__visualization_per_total()
        
        if type == "campanha":
            return self.__visualization_per_campaings()
        
        
    def __visualization_per_total(self):
        
        campanhas = self.__get_campaigns()
        
        today = get_current_time().date()

        query = (
            self.__conn.session.query(
                self.__conn.func.sum(ProcessamentoPedido.valor).label("total"),
                self.__conn.cast(ProcessamentoPedido.data_processamento, self.__conn.Date).label("data_processamento"),
            )
            .join(Pedido, ProcessamentoPedido.fk_pedido_id == Pedido.id)
            .outerjoin(Campanha, Pedido.fk_campanha_id == Campanha.id)
            .filter(
                self.__conn.func.year(ProcessamentoPedido.data_processamento) == get_current_time().year,
                self.__conn.func.month(ProcessamentoPedido.data_processamento) == get_current_time().month,
                ProcessamentoPedido.status_processamento == 1,
                Pedido.contabilizar_doacao == True,
                ProcessamentoPedido.contabilizar_doacao == True,
                (
                    Pedido.fk_forma_pagamento_id == self.__forma_pagamento
                    if self.__forma_pagamento
                    else True
                ),
                (
                    Pedido.fk_campanha_id.in_(list(map(int, self.__campanha_id.split(","))))
                    if self.__campanha_id
                    else True
                ),
                self.__conn.or_(
                    Campanha.contabilizar_doacoes == 1, Campanha.id.is_(None)
                ),
            )
            .group_by(
                self.__conn.cast(ProcessamentoPedido.data_processamento, self.__conn.Date),
            )
        )

        total_donations = query.all()

        daily_donations_dict = {
            item.data_processamento.strftime("%d-%m-%Y"): {
                "total": f"{round(item.total or 0, 2):.2f}"
            }
            for item in total_donations
        }

        today_str = today.strftime("%d-%m-%Y")
        if today_str not in daily_donations_dict:
            daily_donations_dict[today_str] = {"total": "0.00"}

        return self.__format_response_total(campanhas, daily_donations_dict )


    def __visualization_per_campaings(self):
        subquery_totais = (
            self.__conn.session.query(
                self.__conn.func.extract(
                    "day", ProcessamentoPedido.data_processamento
                ).label("dia"),
                self.__conn.func.sum(ProcessamentoPedido.valor).label("valor_total"),
                self.__conn.func.count(ProcessamentoPedido.id).label("quantidade_total"),
            )
            .join(Pedido, Pedido.id == ProcessamentoPedido.fk_pedido_id)
            .outerjoin(Campanha, Pedido.fk_campanha_id == Campanha.id)
            .filter(
                self.__conn.or_(
                    Campanha.contabilizar_doacoes == 1, Campanha.id.is_(None)
                ),
                ProcessamentoPedido.contabilizar_doacao == 1,
                Pedido.contabilizar_doacao == 1,
                ProcessamentoPedido.status_processamento == 1,
                self.__conn.func.year(ProcessamentoPedido.data_processamento) == get_current_time().year,
                self.__conn.func.month(ProcessamentoPedido.data_processamento) == get_current_time().month,
            )
            .group_by(
                self.__conn.func.extract("day", ProcessamentoPedido.data_processamento)
            )
            .subquery()
        )

        query = (
            self.__conn.session.query(
                Campanha.titulo,
                self.__conn.func.sum(ProcessamentoPedido.valor).label("valor_campanha"),
                self.__conn.func.count(ProcessamentoPedido.id).label(
                    "quantidade_pedidos"
                ),
                subquery_totais.c.valor_total.label("valor_total"),
                subquery_totais.c.dia.label("dia"),
            )
            .join(Pedido, Pedido.id == ProcessamentoPedido.fk_pedido_id)
            .outerjoin(Campanha, Campanha.id == Pedido.fk_campanha_id)
            .join(
                subquery_totais,
                subquery_totais.c.dia
                == self.__conn.func.extract(
                    "day", ProcessamentoPedido.data_processamento
                ),
            )
            .filter(
                ProcessamentoPedido.contabilizar_doacao == 1,
                self.__conn.or_(
                    Campanha.contabilizar_doacoes == 1, Campanha.id.is_(None)
                ),
                Pedido.contabilizar_doacao == 1,
                ProcessamentoPedido.status_processamento == 1,
                self.__conn.func.year(ProcessamentoPedido.data_processamento) == get_current_time().year,
                self.__conn.func.month(ProcessamentoPedido.data_processamento) == get_current_time().month,
                )
            .group_by(
                Campanha.titulo,
                subquery_totais.c.valor_total,
                subquery_totais.c.dia,
            )
            .order_by(subquery_totais.c.dia)
        )

        return self.__format_response_campaigns(query.all())

    def __format_response_campaigns(self, results):
        day_dict = {}

        for result in results:
            dia = result.dia
            valor_total = round(result.valor_total, 2)

            if dia not in day_dict:
                day_dict[dia] = {
                    "campaigns": [],
                    "day": f"{get_current_time().year}-{get_current_time().month}-{dia}",
                    "valor_total": f"{valor_total:.2f}",
                }

            percentual = (
                (result.valor_campanha / valor_total * 100) if valor_total > 0 else 0
            )

            day_dict[dia]["campaigns"].append(
                {
                    "name": result.titulo or "Sem campanha",
                    "percentage": f"{percentual:.2f}",
                    "quantidade_total": result.quantidade_pedidos,
                    "valor_campanha": f"{round(result.valor_campanha, 2):.2f}",
                }
            )

        return list(day_dict.values())


    def __get_campaigns(self):
        query_campaigns = (
            self.__conn.session.query(
                Campanha.titulo.label("campanha_titulo"),
                Campanha.id.label("campanha_id"),
            )
            .join(Pedido, Pedido.fk_campanha_id == Campanha.id)
            .join(
                ProcessamentoPedido, ProcessamentoPedido.fk_pedido_id == Pedido.id
            )
            .filter(
                Campanha.objetivo == "doacao",
                self.__conn.func.month(ProcessamentoPedido.data_processamento)
                == get_current_time().month,
                self.__conn.func.year(ProcessamentoPedido.data_processamento)
                == get_current_time().year,
            )
            .distinct(Campanha.id)
        )

        campanhas = [
            {"id": item.campanha_id, "titulo": item.campanha_titulo}
            for item in query_campaigns
        ]
        
        return campanhas
    
    def __format_response_total(self, campanhas: dict, list_per_total: dict) -> dict:
        return {
            "campaigns": campanhas,
            "daily_donations": list_per_total,
        }, 200