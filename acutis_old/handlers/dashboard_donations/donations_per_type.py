from flask import request
from flask_sqlalchemy import SQLAlchemy

from exceptions.error_types.http_not_found import NotFoundError
from models.campanha import Campanha
from models.pedido import Pedido
from models.processamento_pedido import ProcessamentoPedido


class DonatinonsPerType:
    def __init__(self, conn: SQLAlchemy) -> None:
        self.__conn = conn
        self.__http_args = request.args
        
        self.__forma_pagamento = self.__http_args.get("forma_pagamento")
        self.__data_fim = self.__http_args.get("data_fim")
        self.__data_inicio = self.__http_args.get("data_inicio")
        self.__filter_campanha = (
            [int(campanha.strip()) for campanha in self.__http_args.get("fk_campanha_id", "").split(",")]
            if self.__http_args.get("fk_campanha_id")
            else []
        )
        
    def execute(self):
        get_recorrentes = self.__get_donations_recurrence()
        get_avulsas = self.__get_donations_avulsas()
        campanhas = self.__get_campaings()
        data_recorrentes = self.__format_recorrentes(get_recorrentes, get_avulsas)
        data_avulsas = self.__format_avulsas(get_avulsas, get_recorrentes)
        
        return self.__format_response(data_avulsas, data_recorrentes, campanhas)
        
    def __get_campaings(self):
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
                    ProcessamentoPedido.data_processamento >= self.__data_inicio
                    if self.__data_inicio
                    else True
                ),
            )
            .filter(
                self.__conn.cast(ProcessamentoPedido.data_processamento, self.__conn.Date)
                <= self.__conn.cast(self.__data_fim, self.__conn.Date)
                if self.__data_fim
                else True
            )
            .distinct(Campanha.id)
        )

        if query_campaigns is None:
            raise NotFoundError("Nenhuma campanha encontrada")        

        campanhas = [
            {"id": item.campanha_id, "titulo": item.campanha_titulo}
            for item in query_campaigns
        ]
        
        return campanhas
    
    def __get_donations_avulsas(self):
               
        avulsa_results = (
            self.__conn.session.query(
                self.__conn.func.coalesce(self.__conn.func.sum(ProcessamentoPedido.valor), 0),
                self.__conn.func.count(Pedido.id),
                Campanha.titulo.label("campanha"),
                Campanha.id.label("campanha_id"),
            )
            .join(Pedido, ProcessamentoPedido.fk_pedido_id == Pedido.id)
            .outerjoin(Campanha, Pedido.fk_campanha_id == Campanha.id)
            .filter(
                self.__conn.or_(Campanha.contabilizar_doacoes == 1, Campanha.id.is_(None)),
                Pedido.contabilizar_doacao == True,
                ProcessamentoPedido.contabilizar_doacao == True,
                Pedido.periodicidade == 1,
                ProcessamentoPedido.status_processamento == 1,
                Campanha.id.in_(self.__filter_campanha) if self.__filter_campanha else True,
                (
                    Pedido.fk_forma_pagamento_id == self.__forma_pagamento
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
            )
            .group_by(Campanha.titulo, Campanha.id)
            .all()
        )
        
        if avulsa_results is None:
            raise NotFoundError("Nenhum doação avulsa encontrada")        

        return avulsa_results
    
    def __get_total_value(self):
        total = (
            self.__conn.session.query(self.__conn.func.sum(ProcessamentoPedido.valor))
            .join(Pedido, ProcessamentoPedido.fk_pedido_id == Pedido.id)
            .filter(
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
                ProcessamentoPedido.status_processamento == 1,
                Pedido.contabilizar_doacao == 1,
            )
            .scalar()
        )
        
        return total
    
    
    def __get_donations_recurrence(self):
        recorrente_results = (
            self.__conn.session.query(
                self.__conn.func.coalesce(self.__conn.func.sum(ProcessamentoPedido.valor), 0),
                self.__conn.func.count(Pedido.id),
                Campanha.titulo.label("campanha"),
                Campanha.id.label("campanha_id"),
            )
            .join(Pedido, ProcessamentoPedido.fk_pedido_id == Pedido.id)
            .outerjoin(Campanha, Pedido.fk_campanha_id == Campanha.id)
            .filter(
                Pedido.contabilizar_doacao == 1,
                Campanha.id.in_(self.__filter_campanha) if self.__filter_campanha else True,
                self.__conn.or_(Campanha.contabilizar_doacoes == 1, Campanha.id.is_(None)),
                Pedido.contabilizar_doacao == True,
                ProcessamentoPedido.contabilizar_doacao == True,
                Pedido.periodicidade == 2,
                ProcessamentoPedido.status_processamento == 1,
                Campanha.id.in_(self.__filter_campanha) if self.__filter_campanha else True,
                (
                    Pedido.fk_forma_pagamento_id == self.__forma_pagamento
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
            )
            .group_by(Campanha.titulo, Campanha.id)
            .all()
        )
        
        if recorrente_results is None:
            raise NotFoundError("Nenhum doação recorrente encontrada")         
        
        return recorrente_results
        
    def __format_recorrentes(self, recorrente_results: tuple, avulsa_results: tuple):
        
        total_arrecadado = sum([result[0] for result in recorrente_results]) + sum(
            [result[0] for result in avulsa_results]
        )
        
        recorrente_percentage = (
            (sum([result[0] for result in recorrente_results]) / total_arrecadado) * 100
            if total_arrecadado != 0
            else 0
        )
        
        donations_recurrent = {
            "recorrente_total": round(
                sum([result[0] for result in recorrente_results]), 2
            ),
            "recorrente_count": sum([result[1] for result in recorrente_results]),
            "recorrente_percentage": round(recorrente_percentage, 2),
        }
        
        return donations_recurrent
        
    def __format_avulsas(self, avulsa_results: tuple, recorrente_results: tuple):
        
        total_arrecadado = sum([result[0] for result in recorrente_results]) + sum(
            [result[0] for result in avulsa_results]
        )
        
        avulsa_percentage = (
            (sum([result[0] for result in avulsa_results]) / total_arrecadado) * 100
            if total_arrecadado != 0
            else 0
        )
        
        donations_avulsas = {
            "avulsa_total": round(sum([result[0] for result in avulsa_results]), 2),
            "avulsa_count": sum([result[1] for result in avulsa_results]),
            "avulsa_percentage": round(avulsa_percentage, 2),
        }
        
        return donations_avulsas
    
    def __format_response(self, donations_avulsas: dict, donations_recurrent: dict, campanhas: tuple) -> tuple:
        total = self.__get_total_value()
        response = {
            "donations_one_time": donations_avulsas,
            "donations_recurrent": donations_recurrent,
            "total_arrecadado": str(round(total, 2)) if total else 0,
            "campaigns": campanhas,
        }
        
        return response, 200
    