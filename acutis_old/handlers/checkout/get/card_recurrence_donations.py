from builder import db
from models import Pedido


class CardRecurrenceDonations:
    def __init__(self) -> None:
        pass

    def execute(self):
        infos = self.__infos_donaitons_recurrences()

        return self.__format_response(infos)

    def __infos_donaitons_recurrences(self):
        query = (
            db.session.query(
                db.func.sum(Pedido.valor_total_pedido).label(
                    "total_em_doacoes"
                ),
                db.func.count(db.distinct(Pedido.fk_clifor_id)).label(
                    "quantidade_doadores"
                ),
                db.func.count(Pedido.id).label(
                    "quantidade_pedidos_recorrentes"
                ),
            )
            .filter(
                Pedido.periodicidade == 2,
                Pedido.recorrencia_ativa == 1,
                Pedido.contabilizar_doacao == True,
            )
            .all()
        )

        return query

    def __format_response(self, data: tuple):

        (
            valor_recorrencia_prospectado,
            quantidade_doadores,
            quantidade_doacoes_recorrentes,
        ) = data[0]

        return {
            "quantidade_doadores": quantidade_doadores,
            "quantidade_doacoes_recorrentes": quantidade_doacoes_recorrentes,
            "valor_recorrencia_prospectado": str(
                round(valor_recorrencia_prospectado, 2)
            ),
        }, 200
