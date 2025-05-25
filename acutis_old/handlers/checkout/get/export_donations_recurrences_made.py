from flask import request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from models import Pedido, Clifor, Campanha, ProcessamentoPedido, FormaPagamento
from datetime import datetime
from utils.export_excel import export_excel

class ExportDonationsRecurrencesMade:
    def __init__(self, conn: SQLAlchemy) -> None:
        self.__conn = conn

    def execute(self):
        now = datetime.now()
        filters = self.__make_filters()
        
        query = self.__query_donations_made(filters, now)
        data = query.all()
        
        return self.__generate_csv(data)

    def __query_donations_made(self, filters: list, now: datetime):
        query = (
            self.__conn.session.query(
                Pedido.id.label("pedido_id"),
                Clifor.id.label("clifor_id"),
                Clifor.nome,
                Clifor.cpf_cnpj,
                Pedido.data_pedido,
                ProcessamentoPedido.data_processamento,
                Pedido.valor_total_pedido,
                Campanha.titulo.label("nome_campanha"),
                Campanha.descricao,
                FormaPagamento.descricao.label("metodo_pagamento")
            )
            .join(Clifor, Clifor.id == Pedido.fk_clifor_id)
            .join(FormaPagamento, FormaPagamento.id == Pedido.fk_forma_pagamento_id)
            .join(ProcessamentoPedido, ProcessamentoPedido.fk_pedido_id == Pedido.id)
            .outerjoin(Campanha, Campanha.id == Pedido.fk_campanha_id)
            .filter(
                Pedido.contabilizar_doacao == 1,
                ProcessamentoPedido.status_processamento == 1,
                Pedido.periodicidade == 2,
                Pedido.recorrencia_ativa == 1,
                func. extract('month', ProcessamentoPedido.data_processamento) == now.month,
                func.extract('year', ProcessamentoPedido.data_processamento) == now.year
            )
        )

        for filter_condition in filters:
            query = query.filter(filter_condition)

        return query.order_by(self.__conn.desc(ProcessamentoPedido.data_processamento))

    def __make_filters(self):
        filter_mapping = {
            "nome": lambda value: Clifor.nome.ilike(f"%{value}%"),
            "data_inicio": lambda value: func.cast(ProcessamentoPedido.data_processamento, self.__conn.Date) >= func.cast(value, self.__conn.Date),
            "data_fim": lambda value: func.cast(ProcessamentoPedido.data_processamento, self.__conn.Date) <= func.cast(value, self.__conn.Date),
            "forma_pagamento": lambda value: FormaPagamento.id == value,
            "campanha_id": lambda value: Campanha.id == value
        }

        filters = []
        for key, func_filter in filter_mapping.items():
            value = request.args.get(key)
            if value:
                if key in ["data_inicio", "data_fim"]:
                    try:
                        value = datetime.strptime(value, "%Y-%m-%d")
                    except ValueError:
                        continue

                filters.append(func_filter(value))

        return filters

    def __generate_csv(self, data: list):
        res = [
            {
                "Pedido_id": str(donations.pedido_id),
                "Clifor_id": str(donations.clifor_id),
                "Nome": donations.nome or "N/A",
                "CPF/CNPJ": donations.cpf_cnpj,
                "Campanha": donations.nome_campanha or "N/A",
                "Data": donations.data_processamento.strftime('%d-%m-%Y') if donations.data_processamento else "N/A",
                "Metodo": donations.metodo_pagamento or "N/A",
                "Valor": round(donations.valor_total_pedido, 2) if donations.valor_total_pedido is not None else 0.0
            } for donations in data
        ]

        return export_excel(res, 'doacoes-recorrentes-efetuadas')