from flask import request
from flask_sqlalchemy import SQLAlchemy

from exceptions.error_types.http_not_found import NotFoundError
from models.campanha import Campanha
from models.forma_pagamento import FormaPagamento
from models.pedido import Pedido
from models.processamento_pedido import ProcessamentoPedido


class DonationsAnonimous:
    def __init__(self, conn: SQLAlchemy) -> None:
        self.__conn = conn
        self.__http_args = request.args
        self.__campanha_id = self.__http_args.get("campanha_id")
        self.__forma_pagamento = self.__http_args.get("forma_pagamento")
        self.__data_fim = self.__http_args.get("data_fim")
        self.__data_inicio = self.__http_args.get("data_inicio")
        
    def execute(self):
        donations = self.__get_donations_anonimous()
        campaigns = self.__get_campaigns()
        data_anonimous = self.__format_list_anonimous(donations)
        data_nao_anonimous = self.__format_list_nao_anonimous(donations)
        total_arrecadado = sum(item.total for item in donations) 
        
        return self.__format_response(campaigns, data_anonimous, data_nao_anonimous, total_arrecadado)
          
    def __get_campaigns(self):
        query_campaigns = (
            self.__conn.session.query(
                Campanha.titulo.label("campanha_titulo"),
                Campanha.id.label("campanha_id"),
            )
            .join(Pedido, Pedido.fk_campanha_id == Campanha.id)
            .join(ProcessamentoPedido, ProcessamentoPedido.fk_pedido_id == Pedido.id)
            .filter(
                Campanha.objetivo == "doacao",
                Campanha.contabilizar_doacoes == 1,
                (
                    ProcessamentoPedido.data_processamento >= self.__data_inicio
                    if self.__data_inicio
                    else True
                ),
                (
                    self.__conn.cast(ProcessamentoPedido.data_processamento, self.__conn.Date)
                    <= self.__conn.cast(self.__data_fim, self.__conn.Date)
                    if self.__data_fim
                    else True
                ),
            )
            .distinct(Campanha.id)
        )

        campanhas = [
            {"id": item.campanha_id, "titulo": item.campanha_titulo}
            for item in query_campaigns
        ]
    
        return campanhas
    
    def __get_donations_anonimous(self):
        resultados = (
            self.__conn.session.query(
                Pedido.anonimo,
                self.__conn.func.sum(ProcessamentoPedido.valor).label("total"),
                self.__conn.func.count(Pedido.id).label("count"),
            )
            .join(ProcessamentoPedido, ProcessamentoPedido.fk_pedido_id == Pedido.id)
            .outerjoin(Campanha, Pedido.fk_campanha_id == Campanha.id)
            .join(
                FormaPagamento,
                FormaPagamento.id == ProcessamentoPedido.fk_forma_pagamento_id,
            )
            .filter(
                self.__conn.or_(Campanha.contabilizar_doacoes == 1, Campanha.id.is_(None)),
                ProcessamentoPedido.status_processamento == 1,
                Pedido.contabilizar_doacao == True,
                ProcessamentoPedido.contabilizar_doacao == True,
                (
                    FormaPagamento.id == self.__forma_pagamento
                    if self.__forma_pagamento
                    else True
                ),
                (
                    ProcessamentoPedido.data_processamento >= self.__data_inicio
                    if self.__data_inicio
                    else True
                ),
                (
                    self.__conn.cast(ProcessamentoPedido.data_processamento, self.__conn.Date)
                    <= self.__conn.cast(self.__data_fim, self.__conn.Date)
                    if self.__data_fim
                    else True
                ),
                (Pedido.fk_campanha_id == self.__campanha_id  if self.__campanha_id  else True),
            )
            .group_by(Pedido.anonimo)
            .all()
        )
        
        return resultados
    
    def __format_list_anonimous(self, data_anonimous: list) -> dict:
        total_arrecadado = sum(item.total for item in data_anonimous)

        donations_anonymous = {
            "anonimo_total": round(sum(item.total for item in data_anonimous if item.anonimo), 2),
            "anonimo_count": sum(item.count for item in data_anonimous if item.anonimo),
            "anonimo_percentage": round(
                (sum(item.total for item in data_anonimous if item.anonimo) / total_arrecadado) * 100
                if total_arrecadado != 0
                else 0,
                2,
            ),
        }
        
        return donations_anonymous

    def __format_list_nao_anonimous(self, data_anonimous: list) -> dict:
        total_arrecadado = sum(item.total for item in data_anonimous)

        donations_non_anonymous = {
            "nao_anonimo_total": round(sum(item.total for item in data_anonimous if not item.anonimo), 2),
            "nao_anonimo_count": sum(item.count for item in data_anonimous if not item.anonimo),
            "nao_anonimo_percentage": round(
                (sum(item.total for item in data_anonimous if not item.anonimo) / total_arrecadado) * 100
                if total_arrecadado != 0
                else 0,
                2,
            ),
        }
        
        return donations_non_anonymous
    def __format_response(self, campaigns: dict, data_anonimous: dict, data_nao_anonimous: dict, total_arrecadado) -> tuple:
        return {
            "campaigns": campaigns,
            "donations_anonymous": data_anonimous,
            "donations_non_anonymous": data_nao_anonimous,
            "total_arrecadado": round(total_arrecadado, 2)
        }, 200
        
        
            