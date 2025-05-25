from typing import Dict 
from flask import request 
from sqlalchemy import func, or_

from models.campanha import Campanha
from models.forma_pagamento import FormaPagamento
from models.pedido import Pedido
from models.processamento_pedido import ProcessamentoPedido

class DonationsCampaign:
    def __init__(self, db):
        self.__db = db
        self.__http_args = request.args
        self.__data_inicio = self.__http_args.get("data_inicio")
        self.__data_fim = self.__http_args.get("data_fim")
        self.__forma_pagamento = self.__http_args.get("forma_pagamento")

    def execute(self) -> tuple:
        """Retrieve campaign donations without filters"""
        mp_donations = self.__fetch_mp_donations()
            
        total_donations = self.__calculate_total_donations()
            
        campaigns_data = self.__process_campaigns(total_donations)
        
        data_mp_qurey = self.__create_mp_campaign_entry(mp_donations)
        
        if data_mp_qurey["quant_doacoes"] > 0:
            campaigns_data["pix@institutohesed.org.br"] = self.__create_mp_campaign_entry(mp_donations)
            
        return {
            "campaigns_data": list(campaigns_data.values())
        }, 200     

    def __fetch_mp_donations(self):
        """Fetch Mercado Pago donations"""
        mp_query = (
            self.__db.session.query(
                func.sum(ProcessamentoPedido.valor).label("valor_arrecadado"),
                func.count(ProcessamentoPedido.id).label("quant_processamento")
            )
            .join(Pedido, Pedido.id == ProcessamentoPedido.fk_pedido_id)
            .outerjoin(Campanha, Campanha.id == Pedido.fk_campanha_id)
            .join(FormaPagamento, FormaPagamento.id == Pedido.fk_forma_pagamento_id)
            .filter(
                FormaPagamento.id == self.__forma_pagamento if self.__forma_pagamento else True,
                self.__db.cast(ProcessamentoPedido.data_processamento, self.__db.Date) >= self.__db.cast(self.__data_inicio, self.__db.Date) if self.__data_inicio else True,
                self.__db.cast(ProcessamentoPedido.data_processamento, self.__db.Date) <= self.__db.cast(self.__data_fim, self.__db.Date) if self.__data_fim else True,
                Pedido.fk_gateway_pagamento_id == 2,
                ProcessamentoPedido.status_processamento == 1,
                ProcessamentoPedido.contabilizar_doacao == 1,
                Pedido.contabilizar_doacao == 1,
                or_(Campanha.contabilizar_doacoes == 1, Campanha.id.is_(None))
            )
            .group_by(Pedido.fk_gateway_pagamento_id)
            .first()
        )
        
        if mp_query is None:
            return (0.00, 0)
        
        return (float(mp_query.valor_arrecadado), int(mp_query.quant_processamento))

    def __calculate_total_donations(self) -> float:
        """Calculate total donations"""
        return (
            self.__db.session.query(func.sum(Pedido.valor_total_pedido))
            .join(ProcessamentoPedido, ProcessamentoPedido.fk_pedido_id == Pedido.id)
            .join(FormaPagamento, ProcessamentoPedido.fk_forma_pagamento_id == FormaPagamento.id)
            .outerjoin(Campanha, Pedido.fk_campanha_id == Campanha.id)
            .filter(
                FormaPagamento.id == self.__forma_pagamento if self.__forma_pagamento else True,
                self.__db.cast(ProcessamentoPedido.data_processamento, self.__db.Date) >= self.__db.cast(self.__data_inicio, self.__db.Date) if self.__data_inicio else True,
                self.__db.cast(ProcessamentoPedido.data_processamento, self.__db.Date) <= self.__db.cast(self.__data_fim, self.__db.Date) if self.__data_fim else True,
                or_(Campanha.contabilizar_doacoes == 1, Campanha.id.is_(None)),
                Pedido.contabilizar_doacao == True,
                ProcessamentoPedido.contabilizar_doacao == True,
                ProcessamentoPedido.status_processamento == 1,
            )
            .scalar() or 0.00
        )


    def __process_campaigns(self, total_donations: float) -> Dict:
        """Process campaigns and calculate donation metrics"""
        campaigns_data = {}
        
        all_campaigns = (
            self.__db.session.query(
                Campanha.titulo.label("titulo"),
                func.count(Pedido.id).label("quant_donations")
            )
            .join(Pedido, Pedido.fk_campanha_id == Campanha.id)
            .join(ProcessamentoPedido, ProcessamentoPedido.fk_pedido_id == Pedido.id)
            .join(FormaPagamento, ProcessamentoPedido.fk_forma_pagamento_id == FormaPagamento.id)
            .filter(
                FormaPagamento.id == self.__forma_pagamento if self.__forma_pagamento else True,
                self.__db.cast(ProcessamentoPedido.data_processamento, self.__db.Date) >= self.__db.cast(self.__data_inicio, self.__db.Date) if self.__data_inicio else True,
                self.__db.cast(ProcessamentoPedido.data_processamento, self.__db.Date) <= self.__db.cast(self.__data_fim, self.__db.Date) if self.__data_fim else True,
                or_(Campanha.contabilizar_doacoes == 1, Campanha.id.is_(None)),
                Pedido.contabilizar_doacao == True,
                ProcessamentoPedido.contabilizar_doacao == True,
                ProcessamentoPedido.status_processamento == 1,
            )
            .group_by(Campanha.titulo)
            .all()
        )

        for campaign_info in all_campaigns:
            campaign_donations = self.__calculate_campaign_donations(
                campaign_info.titulo, total_donations, campaign_info.quant_donations
            )
            campaigns_data[campaign_info.titulo] = campaign_donations

        return campaigns_data

    def __calculate_campaign_donations(self, titulo: str, total_donations: float, quant_donations: int):
        """Calculate detailed donations for a specific campaign"""
        valor_arrecadado = (
            self.__db.session.query(func.sum(ProcessamentoPedido.valor))
            .select_from(Pedido)
            .join(ProcessamentoPedido, ProcessamentoPedido.fk_pedido_id == Pedido.id)
            .join(FormaPagamento, ProcessamentoPedido.fk_forma_pagamento_id == FormaPagamento.id)
            .join(Campanha, Pedido.fk_campanha_id == Campanha.id)
            .filter(
                FormaPagamento.id == self.__forma_pagamento if self.__forma_pagamento else True,
                self.__db.cast(ProcessamentoPedido.data_processamento, self.__db.Date) >= self.__db.cast(self.__data_inicio, self.__db.Date) if self.__data_inicio else True,
                self.__db.cast(ProcessamentoPedido.data_processamento, self.__db.Date) <= self.__db.cast(self.__data_fim, self.__db.Date) if self.__data_fim else True,
                Pedido.fk_campanha_id == Campanha.id,
                ProcessamentoPedido.status_processamento == 1,
                Pedido.contabilizar_doacao == True,
                ProcessamentoPedido.contabilizar_doacao == True,
                Campanha.titulo == titulo,
                or_(Campanha.contabilizar_doacoes == 1, Campanha.id.is_(None)),
            )
            .scalar() or 0
        )

        percentual_meta_alcancada = (
            (valor_arrecadado / total_donations * 100) if total_donations else 0
        )

        return {
            "titulo": titulo,
            "valor_arrecadado": str(round(valor_arrecadado, 2)),
            "quant_doacoes": quant_donations,
            "percentual_meta_alcancada": str(round(percentual_meta_alcancada, 2)),
        }

    def __create_mp_campaign_entry(self, mp_donations):
        """Create Mercado Pago campaign entry"""
        return {
            "titulo": "pix@institutohesed.org.br",
            "valor_arrecadado": str(round(mp_donations[0], 2)),
            "quant_doacoes": mp_donations[1],
            "percentual_meta_alcancada": None,
        }
