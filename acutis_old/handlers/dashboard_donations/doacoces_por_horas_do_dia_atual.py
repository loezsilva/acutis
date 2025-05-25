from flask import request
from flask_sqlalchemy import SQLAlchemy

from exceptions.error_types.http_bad_request import BadRequestError
from models.campanha import Campanha
from models.forma_pagamento import FormaPagamento
from models.pedido import Pedido
from models.processamento_pedido import ProcessamentoPedido
from utils.functions import get_current_time


class DonationsPerHoursNow:
    def __init__(self, conn: SQLAlchemy):
        self.__conn = conn
        self.__http_args = request.args
        self.__tipo_visualizacao = self.__http_args.get("visualizar_por", "total", type=str)
        self.__forma_pagamento = self.__http_args.get("forma_pagamento")
        self.__filter_data = self.__http_args.get("data_inicio")
        self.__filter_campanha = self.__http_args.get("campanha")
    
    def execute(self):
        print(self.__tipo_visualizacao)
        return self.__visualizar_por(self.__tipo_visualizacao)

    def __get_campanhas(self):
        query_campaigns = (
            self.__conn.session.query(
                Campanha.titulo.label("campanha_titulo"),
                Campanha.id.label("campanha_id"),
            )
            .join(Pedido, Pedido.fk_campanha_id == Campanha.id)
            .join(ProcessamentoPedido, ProcessamentoPedido.fk_pedido_id == Pedido.id)
            .filter(
                Campanha.objetivo == "doacao",
                (
                    self.__conn.cast(ProcessamentoPedido.data_processamento, self.__conn.Date)
                    == self.__conn.cast(self.__filter_data, self.__conn.Date)
                    if self.__filter_data
                    else self.__conn.cast(ProcessamentoPedido.data_processamento, self.__conn.Date)
                    == self.__conn.cast(get_current_time(), self.__conn.Date)
                ),
            )
            .distinct(Campanha.id)
        )
    
        campanhas = [
            {"id": item.campanha_id, "titulo": item.campanha_titulo}
            for item in query_campaigns
        ]
        
        return campanhas
    
    def __visualizar_por(self, type: str):
        
        types = ["total", "campanha"]
        
        if type not in types:
            raise BadRequestError("Tipo de visualização não suportado")
        
        if type == "total":
            return self.__visualizar_por_total()
        
        if type == "campanha":
            return self.__visualizar_por_campanha()
    
    def __visualizar_por_total(self):
                  
        result = (
            self.__conn.session.query(
            self.__conn.func.sum(ProcessamentoPedido.valor).label("valor_total"),
            self.__conn.func.extract(
                "hour", ProcessamentoPedido.data_processamento
            ).label("hora"),
            )
            .join(Pedido, Pedido.id == ProcessamentoPedido.fk_pedido_id)
            .join(
                FormaPagamento,
                FormaPagamento.id == ProcessamentoPedido.fk_forma_pagamento_id,
            )
            .outerjoin(Campanha, Campanha.id == Pedido.fk_campanha_id)
            .filter(
                (
                    self.__conn.cast(ProcessamentoPedido.data_processamento, self.__conn.Date)
                    == self.__conn.cast(self.__filter_data, self.__conn.Date)
                    if self.__filter_data
                    else self.__conn.cast(ProcessamentoPedido.data_processamento, self.__conn.Date)
                    == self.__conn.cast(get_current_time(), self.__conn.Date)
                ),
                self.__conn.or_(Campanha.contabilizar_doacoes == 1, Campanha.id.is_(None)),
                ProcessamentoPedido.contabilizar_doacao == 1,
                Pedido.contabilizar_doacao == 1,
                ProcessamentoPedido.status_processamento == 1,
                (
                    Campanha.id.in_(list(map(int, self.__filter_campanha.split(","))))
                    if self.__filter_campanha
                    else True
                ),
                (
                    FormaPagamento.id == self.__forma_pagamento
                    if self.__forma_pagamento
                    else True
                ),
            )
            .group_by(
                self.__conn.func.extract("hour", ProcessamentoPedido.data_processamento),
            )
            .order_by(
                self.__conn.func.extract(
                    "hour", ProcessamentoPedido.data_processamento
                ).asc()
            )
            .all()
        )

        return self.__format_response_total(result)
    
    def __format_response_total(self, data: tuple) -> tuple:
        campanhas = self.__get_campanhas()
        
        res = [
            {"hora": register.hora, "valor": round(register.valor_total, 2) or 0}
            for register in data
        ]
        
        return {"campaigns": campanhas, "doacoes_por_hora": res}, 200
            
    def __visualizar_por_campanha(self):
        
        subquery_totais = (
            self.__conn.session.query(
                self.__conn.func.extract(
                    "hour", ProcessamentoPedido.data_processamento
                ).label("hora"),
                self.__conn.func.sum(ProcessamentoPedido.valor).label("valor_total"),
                self.__conn.func.count(ProcessamentoPedido.id).label("quantidade_total"),
            )
            .join(Pedido, Pedido.id == ProcessamentoPedido.fk_pedido_id)
            .outerjoin(Campanha, Pedido.fk_campanha_id == Campanha.id)
            .filter(
                self.__conn.or_(Campanha.contabilizar_doacoes == 1, Campanha.id.is_(None)),
                ProcessamentoPedido.contabilizar_doacao == 1,
                Pedido.contabilizar_doacao == 1,
                ProcessamentoPedido.status_processamento == 1,
                self.__conn.func.cast(ProcessamentoPedido.data_processamento, self.__conn.Date)
                == (
                    self.__conn.func.cast(self.__filter_data, self.__conn.Date)
                    if self.__filter_data
                    else self.__conn.func.cast(get_current_time(), self.__conn.Date)
                ),
            )
            .group_by(
                self.__conn.func.extract("hour", ProcessamentoPedido.data_processamento)
            )
            .subquery()
        )

        query = (
            self.__conn.session.query(
                Campanha.titulo,
                self.__conn.func.sum(ProcessamentoPedido.valor).label("valor_campanha"),
                self.__conn.func.count(ProcessamentoPedido.id).label("quantidade_pedidos"),
                self.__conn.func.extract(
                    "hour", ProcessamentoPedido.data_processamento
                ).label("hora"),
                subquery_totais.c.valor_total,
                subquery_totais.c.quantidade_total,
            )
            .join(Pedido, Pedido.id == ProcessamentoPedido.fk_pedido_id)
            .outerjoin(Campanha, Campanha.id == Pedido.fk_campanha_id)
            .join(
                subquery_totais,
                subquery_totais.c.hora
                == self.__conn.func.extract("hour", ProcessamentoPedido.data_processamento),
            )
            .filter(
                ProcessamentoPedido.contabilizar_doacao == 1,
                self.__conn.or_(Campanha.contabilizar_doacoes == 1, Campanha.id.is_(None)),
                Pedido.contabilizar_doacao == 1,
                ProcessamentoPedido.status_processamento == 1,
                self.__conn.func.cast(ProcessamentoPedido.data_processamento, self.__conn.Date)
                == (
                    self.__conn.func.cast(self.__filter_data, self.__conn.Date)
                    if self.__filter_data
                    else self.__conn.func.cast(get_current_time(), self.__conn.Date)
                ),
            )
            .group_by(
                Campanha.titulo,
                self.__conn.func.extract("hour", ProcessamentoPedido.data_processamento),
                subquery_totais.c.valor_total,
                subquery_totais.c.quantidade_total,
            )
            .order_by(
                self.__conn.func.extract("hour", ProcessamentoPedido.data_processamento)
            )
        )

        results = query.all()
        
        return self.__format_response_campanha(results)

    def __format_response_campanha(self, data: tuple) -> list:
        
        result_list = []
        for result in data:
            percentual = (
                (result.valor_campanha / result.valor_total) * 100
                if result.valor_total > 0
                else 0
            )
            result_list.append(
                {
                    "campanha": result.titulo,
                    "valor_campanha": round(result.valor_campanha, 2),
                    "quantidade_pedidos": result.quantidade_pedidos,
                    "hora": int(result.hora),
                    "valor_total": round(result.valor_total, 2),
                    "quantidade_total": result.quantidade_total,
                    "percentual": round(percentual, 2),
                }
            )

        return result_list