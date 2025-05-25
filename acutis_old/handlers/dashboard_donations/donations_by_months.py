from flask import request
from flask_sqlalchemy import SQLAlchemy
from dateutil.relativedelta import relativedelta
from exceptions.error_types.http_bad_request import BadRequestError
from models.campanha import Campanha
from models.pedido import Pedido
from models.processamento_pedido import ProcessamentoPedido
from utils.functions import get_current_time


class DonationsByMonth:
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
            return self.__visualizar_por_total()
        
        if type == "campanha":
            return self.__visualization_per_campaings()
        
        
    def __visualizar_por_total(self):
        
        campanhas = self.__get_campaigns()
        
        current_date = get_current_time()
        start_date = current_date.replace(year=current_date.year - 1)
        end_date = current_date

        result = (
            self.__conn.session.query(
                self.__conn.func.year(ProcessamentoPedido.data_processamento).label("ano"),
                self.__conn.func.month(ProcessamentoPedido.data_processamento).label("mes"),
                Pedido.fk_forma_pagamento_id,
                self.__conn.func.sum(ProcessamentoPedido.valor).label("total_arrecadado"),
                self.__conn.func.sum(ProcessamentoPedido.valor).label("total_arrecadado"),
            )
            .join(Pedido, ProcessamentoPedido.fk_pedido_id == Pedido.id)
            .outerjoin(Campanha, Pedido.fk_campanha_id == Campanha.id)
            .filter(
                self.__conn.or_(Campanha.contabilizar_doacoes == 1, Campanha.id.is_(None)),
                ProcessamentoPedido.status_processamento == 1,
                Pedido.contabilizar_doacao == True,
                ProcessamentoPedido.contabilizar_doacao == True,
                (
                    Pedido.fk_campanha_id == self.__campanha_id
                    if self.__campanha_id
                    else True
                ),
                (
                    Pedido.fk_forma_pagamento_id == self.__forma_pagamento
                    if self.__forma_pagamento
                    else True
                ),
                ProcessamentoPedido.data_processamento >= start_date,
                ProcessamentoPedido.data_processamento <= end_date,  
            )
            .group_by(
                self.__conn.func.year(ProcessamentoPedido.data_processamento),
                self.__conn.func.month(ProcessamentoPedido.data_processamento),
                Pedido.fk_forma_pagamento_id,
                ProcessamentoPedido.fk_forma_pagamento_id,
            )
            .all()
        )

        payment_methods = {1: "Cartão de Crédito", 2: "PIX", 3: "Boleto"}

        if self.__forma_pagamento:
            payment_methods = {self.__forma_pagamento: payment_methods[self.__forma_pagamento]}

        monthly_donations = {}
        date_iterator = start_date
        while date_iterator <= end_date:
            mes_ano = "{:04d}-{:02d}".format(
                date_iterator.year, date_iterator.month
            )
            monthly_donations[mes_ano] = {
                "total_arrecadado": 0,
                "metodos_pagamento": {
                    method: 0 for method in payment_methods.values()
                },
            }
            date_iterator += relativedelta(months=1)

        for row in result:
            mes_ano = "{:04d}-{:02d}".format(row.ano, row.mes)
            monthly_donations[mes_ano]["total_arrecadado"] += row.total_arrecadado

            payment_method_name = payment_methods.get(
                row.fk_forma_pagamento_id, "Outro"
            )
            monthly_donations[mes_ano]["metodos_pagamento"][payment_method_name] += row.total_arrecadado

        for month_data in monthly_donations.values():
            total_monthly_donations = month_data["total_arrecadado"]
            if total_monthly_donations != 0:
                month_data["total_arrecadado"] = round(total_monthly_donations, 2)
                for method_name, method_amount in month_data["metodos_pagamento"].items():
                    method_percentage = (method_amount / total_monthly_donations) * 100
                    month_data["metodos_pagamento"][method_name] = {
                        "total_arrecadado": round(method_amount, 2),
                        "porcentagem": round(method_percentage, 2),
                    }
            else:
                for method_name in month_data["metodos_pagamento"]:
                    month_data["metodos_pagamento"][method_name] = {
                        "total_arrecadado": 0,
                        "porcentagem": 0,
                    }

        formatted_data = []
        for month, data in monthly_donations.items():
            formatted_entry = {"mês": month}
            for method, amount_data in data["metodos_pagamento"].items():
                formatted_entry[method] = amount_data["total_arrecadado"]
            formatted_data.append(formatted_entry)
        
        response = {"data": formatted_data, "campaigns": campanhas}
        
        return response

    def __visualization_per_campaings(self):
        subquery_totais = (
            self.__conn.session.query(
                self.__conn.func.extract(
                    "year", ProcessamentoPedido.data_processamento
                ).label("ano"),
                self.__conn.func.extract(
                    "month", ProcessamentoPedido.data_processamento
                ).label("mes"),
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
            )
            .group_by(
                self.__conn.func.extract("year", ProcessamentoPedido.data_processamento),
                self.__conn.func.extract("month", ProcessamentoPedido.data_processamento),
            )
            .subquery()
        )

        query = (
            self.__conn.session.query(
                Campanha.titulo,
                self.__conn.func.sum(ProcessamentoPedido.valor).label("valor_campanha"),
                self.__conn.func.count(ProcessamentoPedido.id).label("quantidade_pedidos"),
                self.__conn.func.extract(
                    "year", ProcessamentoPedido.data_processamento
                ).label("ano"),
                self.__conn.func.extract(
                    "month", ProcessamentoPedido.data_processamento
                ).label("mes"),
                subquery_totais.c.valor_total,
                subquery_totais.c.quantidade_total,
            )
            .join(Pedido, Pedido.id == ProcessamentoPedido.fk_pedido_id)
            .outerjoin(Campanha, Campanha.id == Pedido.fk_campanha_id)
            .join(
                subquery_totais,
                (
                    subquery_totais.c.ano
                    == self.__conn.func.extract(
                        "year", ProcessamentoPedido.data_processamento
                    )
                )
                & (
                    subquery_totais.c.mes
                    == self.__conn.func.extract(
                        "month", ProcessamentoPedido.data_processamento
                    )
                ),
            )
            .filter(
                self.__conn.or_(Campanha.contabilizar_doacoes == 1, Campanha.id.is_(None)),
                ProcessamentoPedido.contabilizar_doacao == 1,
                Pedido.contabilizar_doacao == 1,
                ProcessamentoPedido.status_processamento == 1,
                Campanha.contabilizar_doacoes == 1,
            )
            .group_by(
                Campanha.titulo,
                self.__conn.func.extract("year", ProcessamentoPedido.data_processamento),
                self.__conn.func.extract("month", ProcessamentoPedido.data_processamento),
                subquery_totais.c.valor_total,
                subquery_totais.c.quantidade_total,
            )
            .order_by(
                self.__conn.func.extract("year", ProcessamentoPedido.data_processamento),
                self.__conn.func.extract("month", ProcessamentoPedido.data_processamento),
            )
        )

        results = query.all()

        return self.__format_response_campaigns(results)


    def __format_response_campaigns(self, results):
        result_dict = {}

        for result in results:
            mes_ano = f"{result.ano}-{result.mes:02}"
            percentual = (
                (result.valor_campanha / result.valor_total) * 100
                if result.valor_total > 0
                else 0
            )

            if mes_ano not in result_dict:
                result_dict[mes_ano] = []

            result_dict[mes_ano].append(
                {
                    "campanha": result.titulo,
                    "valor_campanha": round(result.valor_campanha, 2),
                    "quantidade_pedidos": result.quantidade_pedidos,
                    "valor_total": round(result.valor_total, 2),
                    "quantidade_total": result.quantidade_total,
                    "percentual": round(percentual, 2),
                }
            )
            
        return result_dict
            
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