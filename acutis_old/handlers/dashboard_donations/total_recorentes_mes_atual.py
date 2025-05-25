from dateutil.relativedelta import relativedelta
from flask_sqlalchemy import SQLAlchemy
from models.pedido import Pedido
from models.processamento_pedido import ProcessamentoPedido
from utils.functions import get_current_time, last_day_of_month

class DonationsMesRecorrente:
    def __init__(self, conn: SQLAlchemy):
        self.__conn = conn

    def execute(self):
        """Executa a lógica para listar as doações recorrentes mês a mês"""
        recorrentes_efetuadas = self.__get_efetuadas()   
        recorrentes_nao_efetuadas = self.__get_nao_efetuadas()   
        return self.__format_response(recorrentes_efetuadas, recorrentes_nao_efetuadas)

    def __get_efetuadas(self) -> list:
        """Consulta doações recorrentes efetuadas"""
        query_efetuadas = (
            self.__conn.session.query(
                self.__conn.func.year(ProcessamentoPedido.data_processamento).label("ano"),
                self.__conn.func.month(ProcessamentoPedido.data_processamento).label("mes"),
                self.__conn.func.sum(ProcessamentoPedido.valor).label("total_doacoes"),
            )
            .join(Pedido, ProcessamentoPedido.fk_pedido_id == Pedido.id)
            .filter(
                ProcessamentoPedido.status_processamento == 1,
                Pedido.contabilizar_doacao == 1,
                Pedido.periodicidade == 2,
            )
            .group_by(
                self.__conn.func.year(ProcessamentoPedido.data_processamento),
                self.__conn.func.month(ProcessamentoPedido.data_processamento),
            )
            .order_by(
                self.__conn.func.year(ProcessamentoPedido.data_processamento).desc(),
                self.__conn.func.month(ProcessamentoPedido.data_processamento).desc(),
            )
        )

        return query_efetuadas.all()

    def __get_nao_efetuadas(self) -> list:
        """Consulta doações recorrentes não efetuadas dos últimos 12 meses"""
        recorrentes_nao_efetuadas = []
        
        current_date = get_current_time()
        current_day = current_date.day
        
        for i in range(12):
            target_date = current_date - relativedelta(months=i)
            mes = f"{target_date.month:02d}"
            ano = target_date.year
            
            ultimo_dia_mes = last_day_of_month(ano, target_date.month)
            dia_seguro = min(current_day, ultimo_dia_mes)
            
            query_params = {
                'mes': mes, 
                'ano': ano,
                'dia': dia_seguro   
            }
            
            query = self.__conn.text("""
                SELECT
                    COALESCE(SUM(p.valor_total_pedido), 0) AS valor_total
                FROM
                    pedido p
                WHERE
                    p.contabilizar_doacao = 1
                    AND p.periodicidade = 2
                    AND p.recorrencia_ativa = 1
                    AND p.data_pedido < DATEFROMPARTS(:ano, :mes, :dia)
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
            """)
            
            result = self.__conn.session.execute(query, query_params).scalar()
            
            recorrentes_nao_efetuadas.append({
                "mes_ano": f"{ano}-{mes}",
                "valor_apurado": f"{result:.2f}"
            })
        
        return recorrentes_nao_efetuadas

    def __format_response(self, efetuadas, nao_efetuadas) -> dict:
        """Formata a resposta com as doações recorrentes"""
        recorrentes_efetuadas = [
            {
                "mes_ano": f"{row.ano}-{row.mes:02d}",
                "valor_apurado": f"{row.total_doacoes:.2f}",
            }
            for row in efetuadas
        ]

        return {
            "recorrentes_efetuadas": recorrentes_efetuadas,
            "recorrentes_nao_efetuadas": nao_efetuadas,
        }
