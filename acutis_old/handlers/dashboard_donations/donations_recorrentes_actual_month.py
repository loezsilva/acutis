from flask import request
from flask_sqlalchemy import SQLAlchemy
from models.campanha import Campanha
from models.pedido import Pedido
from models.processamento_pedido import ProcessamentoPedido
from models.forma_pagamento import FormaPagamento
from utils.functions import get_current_time

class DonationsMesAtualApuradas:
    def __init__(self, conn: SQLAlchemy):
        self.__conn = conn
        self.__filter_campanha = request.args.get("fk_campanha_id", None, type=str)
        self.__filter_forma_pagamento = request.args.get("forma_pagamento", None, type=int)

    def execute(self):
        """Executa a lógica para consultar as doações e formatar resposta"""
        campanhas = self.__get_campaigns()   
        paid_donations = self.__query_paid_donations()
        unpaid_donations = self.__query_unpaid_donations()
        return self.__format_response(paid_donations, unpaid_donations, campanhas)   

    def __get_campaigns(self) -> list:
        """Obtém as campanhas de doação que são recorrentes no mês atual"""
        query_campaigns = (
            self.__conn.session.query(
                Campanha.titulo.label("campanha_titulo"),
                Campanha.id.label("campanha_id"),
            )
            .join(Pedido, Pedido.fk_campanha_id == Campanha.id)
            .join(ProcessamentoPedido, ProcessamentoPedido.fk_pedido_id == Pedido.id)
            .filter(
                Campanha.objetivo == "doacao",
                Pedido.recorrencia_ativa == 1,
                self.__conn.func.month(ProcessamentoPedido.data_processamento)
                == get_current_time().month,
                self.__conn.func.year(ProcessamentoPedido.data_processamento)
                == get_current_time().year,
            )
            .distinct(Campanha.id)
        )

        return [
            {"id": item.campanha_id, "titulo": item.campanha_titulo}
            for item in query_campaigns
        ]
    
    def __query_paid_donations(self):
        """Consulta as doações recorrentes pagas apuradas mês a mês"""
        resultados = (
            self.__conn.session.query(
                self.__conn.func.year(ProcessamentoPedido.data_processamento).label("ano"),
                self.__conn.func.month(ProcessamentoPedido.data_processamento).label("mes"),
                self.__conn.func.day(ProcessamentoPedido.data_processamento).label("day"),
                self.__conn.func.sum(ProcessamentoPedido.valor).label("total_doacoes"),
            )
            .join(Pedido, ProcessamentoPedido.fk_pedido_id == Pedido.id)
            .join(
                FormaPagamento,
                FormaPagamento.id == ProcessamentoPedido.fk_forma_pagamento_id,
            )
            .outerjoin(Campanha, Pedido.fk_campanha_id == Campanha.id)
            .filter(
                self.__conn.or_(Campanha.contabilizar_doacoes == 1, Campanha.id.is_(None)),
                ProcessamentoPedido.status_processamento == 1,  # Apenas pagos
                Pedido.contabilizar_doacao == 1,
                Pedido.periodicidade == 2,
                (
                    FormaPagamento.id == self.__filter_forma_pagamento
                    if self.__filter_forma_pagamento
                    else True
                ),
                (Campanha.id == self.__filter_campanha if self.__filter_campanha else True),
                self.__conn.func.month(ProcessamentoPedido.data_processamento)
                == self.__conn.func.month(get_current_time()),
                self.__conn.func.year(ProcessamentoPedido.data_processamento)
                == self.__conn.func.year(get_current_time()),
            )
            .group_by(
                self.__conn.func.year(ProcessamentoPedido.data_processamento),
                self.__conn.func.month(ProcessamentoPedido.data_processamento),
                self.__conn.func.day(ProcessamentoPedido.data_processamento),
            )
            .order_by(
                self.__conn.func.year(ProcessamentoPedido.data_processamento).asc(),
                self.__conn.func.month(ProcessamentoPedido.data_processamento).asc(),
                self.__conn.func.day(ProcessamentoPedido.data_processamento).asc(),
            )
        )

        return resultados

    def __query_unpaid_donations(self):
        """Consulta doações recorrentes não efetuadas do mês atual agrupadas por dia"""
        current_date = get_current_time()
        mes = f"{current_date.month:02d}"
        ano = current_date.year

        query = self.__conn.text("""
            SELECT
                DAY(p.data_pedido) AS dia,
                COALESCE(SUM(p.valor_total_pedido), 0) AS valor_total
            FROM
                pedido p
            WHERE
                p.contabilizar_doacao = 1
                AND p.periodicidade = 2
                AND p.recorrencia_ativa = 1
                AND p.data_pedido < DATEFROMPARTS(:ano, :mes, DAY(GETDATE()))
                AND (
                    MONTH(GETDATE()) != :mes
                    OR YEAR(GETDATE()) != :ano
                    OR DAY(p.data_pedido) < DAY(GETDATE())
                )
                AND p.id NOT IN (
                    SELECT pp.fk_pedido_id
                    FROM processamento_pedido pp
                    JOIN pedido p2 ON pp.fk_pedido_id = p2.id
                    WHERE
                        MONTH(pp.data_processamento) = :mes
                        AND YEAR(pp.data_processamento) = :ano
                        AND pp.status_processamento = 1
                        AND p2.contabilizar_doacao = 1
                        AND p2.periodicidade = 2
                )
            GROUP BY
                DAY(p.data_pedido)
        """)

        results = self.__conn.session.execute(
            query,
            {'mes': mes, 'ano': ano}
        )

        unpaid_donations = []
        for row in results:
            unpaid_donations.append({
                'ano': ano,
                'mes': int(mes),
                'day': row.dia,
                'total_doacoes': str(round(row.valor_total, 2))
            })

        return unpaid_donations

    def __format_response(self, paid_donations, unpaid_donations, campanhas) -> dict:
        """Formata a resposta com as doações apuradas"""
        response = {
            "recorrentes_efetuadas": [],
            "recorrentes_nao_efetuadas": [],
            "campaigns": campanhas,
        }

        for row in paid_donations:
            date_str = f"{row.ano}-{str(row.mes).zfill(2)}-{row.day:02d}"
            donation_data = {"dia": date_str, "valor": str(round(row.total_doacoes, 2))}
            response["recorrentes_efetuadas"].append(donation_data)

        for row in unpaid_donations:
            date_str = f"{row['ano']}-{str(row['mes']).zfill(2)}-{row['day']:02d}"
            donation_data = {"dia": date_str, "valor": row['total_doacoes']}
            response["recorrentes_nao_efetuadas"].append(donation_data)

        return response 

