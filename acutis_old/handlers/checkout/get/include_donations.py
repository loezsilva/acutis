from models import ProcessamentoPedido, Pedido
from exceptions.error_types.http_not_found import NotFoundError
from builder import db


class IncludeDonations:

    def __init__(self, fk_processamento_pedido: int) -> None:
        self.__fk_processamento_pedido = fk_processamento_pedido

    def execute(self):
        data_processamento = self.__get_processamento_pedido()
        self.__update_processamento_pedido(data_processamento)

        return {}, 204

    def __get_processamento_pedido(self) -> tuple:

        processamento_pedido = ProcessamentoPedido.query.filter_by(
            id=self.__fk_processamento_pedido
        ).first()

        if processamento_pedido is None:
            raise NotFoundError("Processamento pedido não encontrado")

        return processamento_pedido

    def __update_processamento_pedido(self, process_pedido: tuple) -> None:

        try:
            processamento_pedido = process_pedido

            pedido = db.session.get(Pedido, processamento_pedido.fk_pedido_id)

            if processamento_pedido.contabilizar_doacao:
                processamentos_contabilizados = (
                    db.session.query(ProcessamentoPedido.id).filter(
                        ProcessamentoPedido.contabilizar_doacao == 1,
                        ProcessamentoPedido.fk_pedido_id == pedido.id,
                    )
                ).count()

                if (
                    processamentos_contabilizados <= 1
                    and pedido.contabilizar_doacao
                ):
                    pedido.contabilizar_doacao = False

            else:
                if not pedido.contabilizar_doacao:
                    pedido.contabilizar_doacao = True

            processamento_pedido.contabilizar_doacao = (
                not processamento_pedido.contabilizar_doacao
            )

            db.session.commit()
        except Exception:
            db.session.rollback()
            return
