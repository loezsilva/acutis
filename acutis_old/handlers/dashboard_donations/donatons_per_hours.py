from flask import request
from flask_sqlalchemy import SQLAlchemy
from typing import Dict, List, Any
from models.campanha import Campanha
from models.pedido import Pedido
from models.processamento_pedido import ProcessamentoPedido

class DonationsPerHours:
    def __init__(self, conn: SQLAlchemy) -> None:
        self.__conn = conn
        self.__http_args = request.args
        self.__campanha_id = self.__http_args.get("fk_campanha_id", type=int)
        self.__forma_pagamento = self.__http_args.get("forma_pagamento", type=int)
        self.__data_inicio = self.__http_args.get("data_inicio")
        self.__data_fim = self.__http_args.get("data_fim")

    def execute(self) -> tuple:

        donations_by_hour = self.__query_donations_by_hour()       
        campaigns = self.__get_related_campaigns(donations_by_hour)
        total_donations = sum(hour_data['doacoes'] for hour_data in donations_by_hour.values())
        self.__calculate_percentages(donations_by_hour, total_donations)    
        return self.__format_response(campaigns, donations_by_hour)

    def __query_donations_by_hour(self) -> Dict[str, Dict[str, Any]]:

        query = (
            self.__conn.session.query(
                self.__conn.func.extract('hour', Pedido.data_pedido).label('hora'),
                self.__conn.func.count().label('total_doacoes')
            )
            .join(ProcessamentoPedido, ProcessamentoPedido.fk_pedido_id == Pedido.id)
            .filter(
                Pedido.contabilizar_doacao == True,
                ProcessamentoPedido.contabilizar_doacao == True,
                ProcessamentoPedido.status_processamento == 1,
                (Pedido.fk_campanha_id == self.__campanha_id if self.__campanha_id else True),
                (Pedido.fk_forma_pagamento_id == self.__forma_pagamento if self.__forma_pagamento else True),
                (ProcessamentoPedido.data_processamento >= self.__data_inicio if self.__data_inicio else True),
                (self.__conn.cast(ProcessamentoPedido.data_processamento, self.__conn.Date) <= 
                 self.__conn.cast(self.__data_fim, self.__conn.Date) if self.__data_fim else True)
            )
            .group_by(self.__conn.func.extract('hour', Pedido.data_pedido))
            .all()
        )

        donations_by_hour = {
            f"{hora:02d}": {
                "doacoes": total_doacoes,
                "porcentagem": 0.0
            } for hora, total_doacoes in query
        }

        for hora in range(24):
            hora_str = f"{hora:02d}"
            if hora_str not in donations_by_hour:
                donations_by_hour[hora_str] = {
                    "doacoes": 0,
                    "porcentagem": 0.0
                }

        return donations_by_hour

    def __get_related_campaigns(self, donations_by_hour: Dict[str, Dict[str, Any]]) -> List[Dict[int, str]]:

        campaign_ids = set()
        for hora_data in donations_by_hour.values():
            if hora_data['doacoes'] > 0:
                campaign_query = (
                    self.__conn.session.query(Pedido.fk_campanha_id)
                    .join(ProcessamentoPedido, ProcessamentoPedido.fk_pedido_id == Pedido.id)
                    .filter(
                        (ProcessamentoPedido.data_processamento >= self.__data_inicio if self.__data_inicio else True),
                        (self.__conn.cast(ProcessamentoPedido.data_processamento, self.__conn.Date) <= 
                        self.__conn.cast(self.__data_fim, self.__conn.Date) if self.__data_fim else True),
                        ProcessamentoPedido.status_processamento == 1,
                        Pedido.contabilizar_doacao == True,
                        ProcessamentoPedido.contabilizar_doacao == True
                    )
                    .distinct()
                    .all()
                )
                campaign_ids.update(campaign_id for (campaign_id,) in campaign_query if campaign_id)

        if campaign_ids:
            campaigns = (
                Campanha.query
                .filter(
                    Campanha.id.in_(campaign_ids), 
                    Campanha.contabilizar_doacoes == 1
                )
                .all()
            )
            return [{"id": campaign.id, "titulo": campaign.titulo} for campaign in campaigns]
        
        return []

    def __calculate_percentages(self, donations_by_hour: Dict[str, Dict[str, Any]], total_donations: int):

        for hora in donations_by_hour:
            if total_donations > 0:
                donations_by_hour[hora]['porcentagem'] = round(
                    (donations_by_hour[hora]['doacoes'] / total_donations) * 100, 2
                )
                
    def __format_response(self, campaigns: tuple, donations_by_hour: tuple) -> tuple:
        return {
            "donations_by_hour": donations_by_hour,
            "campaigns": campaigns
        }, 200
