from typing import List, Dict
from flask import request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func, extract
from models.campanha import Campanha
from models.forma_pagamento import FormaPagamento
from models.pedido import Pedido
from models.processamento_pedido import ProcessamentoPedido


class DonationsPerWeekDay:
    def __init__(self, db: SQLAlchemy) -> None:
        self.__db = db

    def execute(self) -> Dict:
        filters = self.__get_all_filters()
        campanhas = self.__fetch_campaigns(filters)
        donations_data = self.__get_donations_by_weekday(filters)
        return self.__format_response(donations_data, campanhas)

    def __get_all_filters(self) -> List:
        filter_mapping = {
            "data_inicio": lambda value: self.__db.cast(ProcessamentoPedido.data_processamento, self.__db.Date) >= self.__db.cast(value, self.__db.Date),
            "data_fim": lambda value: self.__db.cast(ProcessamentoPedido.data_processamento, self.__db.Date) <= self.__db.cast(value, self.__db.Date),
            "fk_campanha_id": lambda value: Pedido.fk_campanha_id == value,
            "forma_pagamento": lambda value: Pedido.fk_forma_pagamento_id == value
        }

        filters = []

        for key, filter_func in filter_mapping.items():
            value = request.args.get(key)
            if value:
                filters.append(filter_func(value))

        return filters

    def __fetch_campaigns(self, filters: List) -> List[Dict]:
        query_campaigns = (
            self.__db.session.query(
                Campanha.titulo.label("campanha_titulo"),
                Campanha.id.label("campanha_id")
            )
            .join(Pedido, Pedido.fk_campanha_id == Campanha.id)
            .join(ProcessamentoPedido, ProcessamentoPedido.fk_pedido_id == Pedido.id)
            .filter(
                Campanha.objetivo == "doacao",
                *filters
            )
            .distinct(Campanha.id)
        )

        return [
            {"id": item.campanha_id, "titulo": item.campanha_titulo}
            for item in query_campaigns
        ]

    def __get_donations_by_weekday(self, filters: List) -> Dict:
        dia_da_semana = self.__db.case(
            (self.__db.extract('dow', ProcessamentoPedido.data_processamento) == 1, 'Domingo'),
            (self.__db.extract('dow', ProcessamentoPedido.data_processamento) == 2, 'Segunda-feira'),
            (self.__db.extract('dow', ProcessamentoPedido.data_processamento) == 3, 'Terça-feira'),
            (self.__db.extract('dow', ProcessamentoPedido.data_processamento) == 4, 'Quarta-feira'),
            (self.__db.extract('dow', ProcessamentoPedido.data_processamento) == 5, 'Quinta-feira'),
            (self.__db.extract('dow', ProcessamentoPedido.data_processamento) == 6, 'Sexta-feira'),
            (self.__db.extract('dow', ProcessamentoPedido.data_processamento) == 7, 'Sábado'), 
        ).label('DiaDaSemana')

        query = (
            self.__db.session.query(
                dia_da_semana,
                FormaPagamento.descricao,
                func.sum(ProcessamentoPedido.valor).label('TotalValor')
            )
            .join(Pedido, Pedido.id == ProcessamentoPedido.fk_pedido_id)
            .join(FormaPagamento, FormaPagamento.id == ProcessamentoPedido.fk_forma_pagamento_id)
            .filter(
                ProcessamentoPedido.status_processamento == 1,
                ProcessamentoPedido.contabilizar_doacao == 1,
                Pedido.contabilizar_doacao == 1,
                *filters
            )
            .group_by(
                extract('dow', ProcessamentoPedido.data_processamento),
                FormaPagamento.descricao
            )
            .order_by(extract('dow', ProcessamentoPedido.data_processamento))
        )

        result = query.all()
        donations_data = {}

        dias_semana = ["Domingo", "Segunda-feira", "Terça-feira", "Quarta-feira", "Quinta-feira", "Sexta-feira", "Sábado"]
        for dia in dias_semana:
            donations_data[dia] = {
                "Boleto": 0.00,
                "Credito": 0.00,
                "Pix": 0.00
            }

        for row in result:
            dia_semana = row.DiaDaSemana
            forma_pagamento = row.descricao
            total_valor = row.TotalValor

            if dia_semana in donations_data:
                donations_data[dia_semana][forma_pagamento] = total_valor

        return donations_data

    def __format_response(self, donations_by_weekday: Dict, campanhas: List[Dict]) -> Dict:
        formatted_donations = []
        for dia, formas_pagamento in donations_by_weekday.items():
            formatted_donations.append({
                "dia": dia,
                **{forma: float(valor) for forma, valor in formas_pagamento.items()}
            })

        return {
            "campaigns": campanhas,
            "donations_by_payment_method_per_day": formatted_donations
        }