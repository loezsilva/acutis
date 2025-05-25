from flask_sqlalchemy import SQLAlchemy
from models import (
    Pedido,
    Clifor,
    Campanha,
    ProcessamentoPedido,
    FormaPagamento,
    Usuario,
    GatewayPagamento,
)
from utils.export_excel import export_excel


class ExportDonationsDesconsideradas:
    def __init__(self, conn: SQLAlchemy) -> None:
        self.__conn = conn
    
    def execute(self):
        data = self.__query_donations_desconsideradas()
        return self.__generate_csv(data)

    def __query_donations_desconsideradas(self):

        selected_columns = [
            Usuario.deleted_at,
            Pedido.anonimo,
            Clifor.id,
            Clifor.nome,
            Clifor.fk_usuario_id,
            Campanha.descricao,
            Campanha.id.label("fk_campanha_id"),
            Campanha.filename,
            Campanha.titulo,
            ProcessamentoPedido.data_processamento,
            FormaPagamento.descricao.label("forma_pagamento"),
            Pedido.id.label("fk_pedido_id"),
            Pedido.order_id,
            ProcessamentoPedido.id_transacao_gateway,
            ProcessamentoPedido.id.label("fk_processamento_pedido_id"),
            ProcessamentoPedido.status_processamento,
            ProcessamentoPedido.transaction_id,
            Pedido.periodicidade,
            Pedido.recorrencia_ativa,
            Pedido.valor_total_pedido,
            Pedido.contabilizar_doacao,
            Pedido.fk_gateway_pagamento_id,
            Pedido.cancelada_em,
            Pedido.status_pedido,
            GatewayPagamento.descricao.label("gateway_pagamento_nome"),
        ]

        donations_query = (
            self.__conn.session.query(*selected_columns)
            .select_from(Pedido)
            .join(ProcessamentoPedido, Pedido.id == ProcessamentoPedido.fk_pedido_id)
            .join(FormaPagamento, Pedido.fk_forma_pagamento_id == FormaPagamento.id)
            .join(Campanha, Pedido.fk_campanha_id == Campanha.id, isouter=True)
            .join(Clifor, Clifor.id == Pedido.fk_clifor_id)
            .join(Usuario, Clifor.fk_usuario_id == Usuario.id, isouter=True)
            .join(
                GatewayPagamento, GatewayPagamento.id == Pedido.fk_gateway_pagamento_id
            )
            .filter(Pedido.contabilizar_doacao == False)
            .distinct().order_by(ProcessamentoPedido.data_processamento.desc()
            )
        )

        return donations_query

    def __generate_csv(self, data: tuple):
        STATUS_PROCESSAMENTO_MAP = {
            0: "Em processamento",
            1: "Pago",
            2: "Não efetuado",
            3: "Expirado",
        }

        list_donations_desconsideradas = [
            {
                "Pedido_id": donation.fk_pedido_id,
                "metodo": donation.forma_pagamento,
                "Referencia": donation.id_transacao_gateway,
                "Transacao_id": donation.transaction_id,
                "Cliente": donation.nome,
                "Data": donation.data_processamento.strftime("%Y-%m-%d %H:%M:%S"),
                "Valor": round(donation.valor_total_pedido, 2),
                "Status": STATUS_PROCESSAMENTO_MAP[donation.status_processamento],
                "Gateway": donation.gateway_pagamento_nome,
                "Campanha": donation.titulo
            }
            for donation in data
        ]

        return export_excel(list_donations_desconsideradas, 'donations_desconsideradas')