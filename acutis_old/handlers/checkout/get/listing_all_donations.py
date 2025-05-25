import logging
from flask import request
from flask_jwt_extended import current_user
from flask_sqlalchemy import SQLAlchemy

from exceptions.error_types.http_bad_request import BadRequestError
from models.campanha import Campanha
from models.clifor import Clifor
from models.forma_pagamento import FormaPagamento
from models.gateway_pagamento import GatewayPagamento
from models.pedido import Pedido
from models.perfil import ProfilesEnum
from models.processamento_pedido import ProcessamentoPedido
from models.usuario import Usuario


class ListingAllDonations:

    def __init__(self, conn: SQLAlchemy) -> None:
        self.__conn = conn
        self.__http_request = request.args
        self.__filter_multiple = self.__http_request.get(
            "filter_multiple", None, type=str
        )

        self.__search_cpf = None
        self.__search_email = None
        self.__search_nome = None

        self.__page = self.__http_request.get("page", 1, type=int)
        self.__per_page = self.__http_request.get("per_page", 10, type=int)

        self.__tipo_pagamento = self.__http_request.get(
            "tipo_pagamento", None, type=int
        )
        self.__campanha_id = self.__http_request.get(
            "campanha_id", None, type=int
        )
        self.__status = self.__http_request.get("status")
        self.__data_inicial = self.__http_request.get(
            "data_inicial", None, type=str
        )
        self.__data_final = self.__http_request.get(
            "data_final", None, type=str
        )
        self.__nome_cliente = self.__http_request.get(
            "nome_cliente", None, type=str
        )
        self.__recorrencia = self.__http_request.get(
            "recorrencia", None, type=str
        )
        self.__doacao_anonima = self.__http_request.get(
            "doacao_anonima", None, type=int
        )
        self.__cpf = self.__http_request.get("cpf", None, type=int)
        self.__transaction_id = self.__http_request.get(
            "transaction_id", None, type=str
        )
        self.__codigo_referencial = self.__http_request.get(
            "codigo_referencial", None, type=str
        )
        self.__email = self.__http_request.get("email", None, type=str)
        self.__status_recorrencia = self.__http_request.get(
            "status_recorrencia", None
        )
        self.__fk_gateway_pagamento_id = self.__http_request.get(
            "fk_gateway_pagamento_id", None, type=int
        )
        self.__pedido_id = self.__http_request.get("pedido_id", type=int)

        if self.__data_inicial and self.__data_final is None:
            raise BadRequestError(
                "Para filtrar por datas, a data inicial e final devem ser informadas."
            )

    def execute(self):
        self.__filter_multiple_define(self.__filter_multiple)
        donations, valor_total = self.__query_all_donations()

        return self.__format_response(donations, valor_total)

    def __filter_multiple_define(self, filter: str | int) -> None:

        if filter:

            is_cpf_query = self.__conn.session.query(Clifor).filter(
                Clifor.cpf_cnpj.ilike(f"%{filter}%")
            )
            if is_cpf_query.first() is not None:
                self.__search_cpf = filter

            is_email_query = self.__conn.session.query(Clifor).filter(
                Clifor.email.like(f"%{filter}%")
            )
            if is_email_query.first() is not None:
                self.__search_email = filter

            is_nome_query = self.__conn.session.query(Clifor).filter(
                Clifor.nome.like(f"%{filter}%")
            )
            if is_nome_query.first() is not None:
                self.__search_nome = filter

    def __query_all_donations(self) -> tuple:
        selected_columns = [
            Usuario.deleted_at,
            Pedido.anonimo,
            Clifor.id,
            Clifor.nome,
            Clifor.fk_usuario_id,
            Campanha.descricao,
            Campanha.id.label("fk_campanha_id"),
            Campanha.titulo,
            Campanha.filename,
            ProcessamentoPedido.data_processamento,
            FormaPagamento.descricao.label("forma_pagamento"),
            Pedido.id.label("fk_pedido_id"),
            Pedido.order_id,
            ProcessamentoPedido.id_transacao_gateway,
            ProcessamentoPedido.id.label("fk_processamento_pedido_id"),
            ProcessamentoPedido.status_processamento,
            ProcessamentoPedido.transaction_id,
            ProcessamentoPedido.id_pagamento,
            Pedido.periodicidade,
            Pedido.recorrencia_ativa,
            Pedido.valor_total_pedido,
            Pedido.contabilizar_doacao,
            Pedido.fk_gateway_pagamento_id,
            Pedido.cancelada_em,
            Pedido.status_pedido,
            GatewayPagamento.descricao.label("gateway_pagamento_nome"),
        ]

        filters = [
            (
                Pedido.fk_gateway_pagamento_id
                == self.__fk_gateway_pagamento_id
                if self.__fk_gateway_pagamento_id
                else True
            ),
            (
                ProcessamentoPedido.transaction_id.ilike(
                    f"%{self.__transaction_id}%"
                )
                if self.__transaction_id
                else True
            ),
            (
                ProcessamentoPedido.id_transacao_gateway.ilike(
                    f"%{self.__codigo_referencial}%"
                )
                if self.__codigo_referencial is not None
                else True
            ),
            Clifor.cpf_cnpj.ilike(f"%{self.__cpf}%") if self.__cpf else True,
            Clifor.email.ilike(f"%{self.__email}%") if self.__email else True,
            (
                Clifor.email.ilike(f"%{self.__search_email}%")
                if self.__search_email
                else True
            ),
            (
                Clifor.nome.ilike(f"%{self.__search_nome}%")
                if self.__search_nome
                else True
            ),
            (
                Clifor.nome.ilike(f"%{self.__nome_cliente}%")
                if self.__nome_cliente
                else True
            ),
            (
                Clifor.cpf_cnpj.ilike(f"%{self.__search_cpf}%")
                if self.__search_cpf
                else True
            ),
            (
                ProcessamentoPedido.data_processamento >= self.__data_inicial
                if self.__data_inicial
                else True
            ),
            (
                ProcessamentoPedido.data_processamento <= self.__data_final
                if self.__data_final
                else True
            ),
            (
                FormaPagamento.id == self.__tipo_pagamento
                if self.__tipo_pagamento
                else True
            ),
            Pedido.contabilizar_doacao == True,
            ProcessamentoPedido.contabilizar_doacao == True,
            (
                ProcessamentoPedido.status_processamento == self.__status
                if self.__status
                else True
            ),
            (
                Pedido.status_pedido == 2
                if self.__status_recorrencia == "canceladas"
                else True
            ),
            (
                Pedido.status_pedido == 1
                if self.__status_recorrencia == "ativas"
                else True
            ),
            (
                Pedido.periodicidade == 2
                if self.__recorrencia == "recorrente"
                else True
            ),
            (
                Pedido.periodicidade == 1
                if self.__recorrencia == "nao_recorrente"
                else True
            ),
            (
                ProcessamentoPedido.fk_pedido_id == self.__pedido_id
                if self.__pedido_id
                else True
            ),
            Campanha.id == self.__campanha_id if self.__campanha_id else True,
        ]

        donations_query = (
            self.__conn.session.query(*selected_columns)
            .select_from(Pedido)
            .join(
                ProcessamentoPedido,
                Pedido.id == ProcessamentoPedido.fk_pedido_id,
            )
            .join(
                FormaPagamento,
                Pedido.fk_forma_pagamento_id == FormaPagamento.id,
            )
            .join(Campanha, Pedido.fk_campanha_id == Campanha.id, isouter=True)
            .join(Clifor, Clifor.id == Pedido.fk_clifor_id)
            .join(Usuario, Clifor.fk_usuario_id == Usuario.id, isouter=True)
            .join(
                GatewayPagamento,
                GatewayPagamento.id == Pedido.fk_gateway_pagamento_id,
            )
            .filter(*filters)
            .distinct()
            .order_by(ProcessamentoPedido.data_processamento.desc())
        )

        if (
            self.__doacao_anonima
            and str(current_user["nome_perfil"]).lower()
            != ProfilesEnum.GESTOR_DOACOES.lower()
        ):
            donations_query = donations_query.filter(
                Pedido.anonimo == self.__doacao_anonima
            )
        elif (
            str(current_user["nome_perfil"]).lower()
            == ProfilesEnum.GESTOR_DOACOES.lower()
        ):
            donations_query = donations_query.filter(Pedido.anonimo == False)

        paginate = donations_query.paginate(
            per_page=self.__per_page, page=self.__page, error_out=False
        )

        total_doado_query = (
            self.__conn.session.query(
                self.__conn.func.sum(ProcessamentoPedido.valor)
            )
            .select_from(Pedido)
            .join(
                ProcessamentoPedido,
                Pedido.id == ProcessamentoPedido.fk_pedido_id,
            )
            .join(
                FormaPagamento,
                Pedido.fk_forma_pagamento_id == FormaPagamento.id,
            )
            .join(Campanha, Pedido.fk_campanha_id == Campanha.id, isouter=True)
            .join(Clifor, Clifor.id == Pedido.fk_clifor_id)
            .join(Usuario, Clifor.fk_usuario_id == Usuario.id, isouter=True)
            .join(
                GatewayPagamento,
                GatewayPagamento.id == Pedido.fk_gateway_pagamento_id,
            )
            .filter(*filters)
        )

        if (
            self.__doacao_anonima
            and str(current_user["nome_perfil"]).lower()
            != ProfilesEnum.GESTOR_DOACOES.lower()
        ):
            total_doado_query = total_doado_query.filter(
                Pedido.anonimo == self.__doacao_anonima
            )
        elif (
            str(current_user["nome_perfil"]).lower()
            == ProfilesEnum.GESTOR_DOACOES.lower()
        ):
            total_doado_query = total_doado_query.filter(
                Pedido.anonimo == False
            )

        total_doado = total_doado_query.scalar() or 0

        return (paginate, total_doado)

    def __format_response(self, data: tuple, valor_total) -> tuple:

        STATUS_PROCESSAMENTO_MAP = {
            0: "Em processamento",
            1: "Pago",
            2: "Não efetuado",
        }

        result = {
            "total_doado": str(round(valor_total, 2)),
            "page": self.__page,
            "pages": data.pages,
            "total": data.total,
            "data": [
                {
                    "benfeitor": {
                        "deleted_at": (
                            donation.deleted_at.strftime("%d/%m/%Y %H:%M:%S")
                            if donation.deleted_at
                            else None
                        ),
                        "user_id": donation.fk_usuario_id,
                        "fk_clifor_id": donation.id,
                        "nome": (
                            "----"
                            if donation.fk_gateway_pagamento_id == 2
                            and donation.fk_usuario_id is None
                            else donation.nome
                        ),
                    },
                    "campanha": {
                        "descricao": donation.descricao,
                        "fk_campanha_id": donation.fk_campanha_id,
                        "imagem": donation.filename,
                        "titulo": donation.titulo,
                    },
                    "pedido": {
                        "anonimo": donation.anonimo,
                        "data_doacao": (
                            donation.data_processamento.strftime(
                                "%d/%m/%Y %H:%M:%S"
                            )
                            if donation.data_processamento
                            else None
                        ),
                        "fk_pedido_id": donation.fk_pedido_id,
                        "forma_pagamento": donation.forma_pagamento,
                        "recorrencia": (
                            True if donation.periodicidade == 2 else False
                        ),
                        "recorrencia_ativa": donation.recorrencia_ativa,
                        "cancelada_em": (
                            donation.cancelada_em.strftime("%d/%m/%Y %H:%M:%S")
                            if donation.cancelada_em
                            else None
                        ),
                        "order_id": donation.order_id,
                        "valor_doacao": str(
                            round(donation.valor_total_pedido, 2)
                        ),
                        "contabilizar_doacao": donation.contabilizar_doacao,
                        "status_pedido": donation.status_pedido,
                        "gateway_pagamento": {
                            "id": donation.fk_gateway_pagamento_id,
                            "nome": donation.gateway_pagamento_nome,
                        },
                    },
                    "processamento": {
                        "codigo_referencia": donation.id_transacao_gateway,
                        "fk_processamento_pedido_id": donation.fk_processamento_pedido_id,
                        "status": STATUS_PROCESSAMENTO_MAP[
                            donation.status_processamento
                        ],
                        "transaction_id": donation.transaction_id,
                        "id_pagamento": donation.id_pagamento,
                    },
                }
                for donation in data
            ],
        }

        return result, 200
