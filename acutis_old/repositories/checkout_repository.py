from datetime import date
from http import HTTPStatus
from typing import Optional
from click import Option
from flask import Request, request
from flask_jwt_extended import current_user
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Date, between, desc, func, or_

from models.campanha import Campanha
from models.clifor import Clifor
from models.forma_pagamento import FormaPagamento
from models.gateway_pagamento import GatewayPagamento
from models.pedido import Pedido
from models.perfil import ProfilesEnum
from models.processamento_pedido import ProcessamentoPedido
from models.schemas.checkout.get.get_donors_ranking import (
    DonorRankingSchema,
    GetDonorsRankingQueryFilter,
)
from models.schemas.checkout.get.get_regular_donors import (
    GetRegularDonorsQueryFilter,
)
from models.schemas.checkout.get.get_top_regular_donors import (
    FilterTypesEnum,
    GetTopRegularDonorsQueryFilter,
    TopRegularDonorSchema,
)
from models.schemas.checkout.get.listar_doacoes_schema import ListarDoacoesQuery
from models.schemas.checkout.schema_recurrence_not_paid import ListagemDeRecorreciaEmLapsosRequest
from models.usuario import Usuario
from repositories.interfaces.checkout_repository_interface import (
    CheckoutRepositoryInterface,
)


class CheckoutRepository(CheckoutRepositoryInterface):
    def __init__(self, database: SQLAlchemy) -> None:
        self.__database = database

    def get_top_regular_donors(
        self,
        filtros: GetTopRegularDonorsQueryFilter,
        mes_inicial: date,
        mes_final: date,
    ) -> list[TopRegularDonorSchema]:
        top_doadores_query = (
            self.__database.session.query(
                Clifor.nome,
                Usuario.id.label("fk_usuario_id"),
                Usuario.avatar,
                func.count(ProcessamentoPedido.id).label("quantidade_doacoes"),
                func.sum(ProcessamentoPedido.valor).label("valor_total_doacoes"),
            )
            .select_from(Clifor)
            .join(Pedido, Clifor.id == Pedido.fk_clifor_id)
            .join(
                ProcessamentoPedido,
                Pedido.id == ProcessamentoPedido.fk_pedido_id,
            )
            .outerjoin(Usuario, Clifor.fk_usuario_id == Usuario.id)
            .filter(
                between(
                    func.cast(ProcessamentoPedido.data_processamento, Date),
                    mes_inicial,
                    mes_final,
                ),
                ProcessamentoPedido.status_processamento == 1,
                Clifor.cpf_cnpj.isnot(None),
                Pedido.contabilizar_doacao == 1,
                or_(Usuario.id.is_(None), Usuario.id != 2),  # Admin
            )
            .group_by(Clifor.nome, Usuario.id, Usuario.avatar)
        )

        if filtros.tipo_doacao:
            doacao_mapping = {
                "avulsa": 1,
                "recorrente": 2,
            }
            top_doadores_query = top_doadores_query.filter(
                Pedido.periodicidade == doacao_mapping[filtros.tipo_doacao]
            )

        if filtros.fk_campanhas_ids:
            top_doadores_query = top_doadores_query.filter(
                Pedido.fk_campanha_id.in_(
                    list(map(int, filtros.fk_campanhas_ids.split(",")))
                )
            )

        if filtros.tipo_ordenacao == FilterTypesEnum.FREQUENCIA:
            order_by_criteria = [
                desc("quantidade_doacoes"),
                desc("valor_total_doacoes"),
            ]
        elif filtros.tipo_ordenacao == FilterTypesEnum.VALOR:
            order_by_criteria = [
                desc("valor_total_doacoes"),
                desc("quantidade_doacoes"),
            ]

        if (
            str(current_user["nome_perfil"]).lower()
            == ProfilesEnum.GESTOR_DOACOES.lower()
        ):
            top_doadores_query = top_doadores_query.filter(Pedido.anonimo == False)

        top_doadores_query = top_doadores_query.order_by(*order_by_criteria)

        top_doadores = top_doadores_query.limit(filtros.limite_top_doadores).all()

        return top_doadores

    def get_donors_ranking(
        self,
        filtros: GetDonorsRankingQueryFilter,
        mes_inicial: date,
        mes_final: date,
    ) -> tuple[list[DonorRankingSchema], int]:
        ranking_doadores_query = (
            self.__database.session.query(
                Clifor.nome.label("benfeitor"),
                Usuario.id.label("fk_usuario_id"),
                func.count(ProcessamentoPedido.id).label("quantidade_doacoes"),
                func.sum(ProcessamentoPedido.valor).label("valor_total_doacoes"),
            )
            .select_from(Clifor)
            .join(Pedido, Clifor.id == Pedido.fk_clifor_id)
            .join(
                ProcessamentoPedido,
                Pedido.id == ProcessamentoPedido.fk_pedido_id,
            )
            .outerjoin(Usuario, Clifor.fk_usuario_id == Usuario.id)
            .filter(
                between(
                    func.cast(ProcessamentoPedido.data_processamento, Date),
                    mes_inicial,
                    mes_final,
                ),
                ProcessamentoPedido.status_processamento == 1,
                Clifor.cpf_cnpj.isnot(None),
                Pedido.contabilizar_doacao == 1,
                or_(Usuario.id.is_(None), Usuario.id != 2),  # Admin
            )
            .group_by(Clifor.nome, Usuario.id)
            .order_by(desc("valor_total_doacoes"))
        )

        if filtros.tipo_doacao:
            doacao_mapping = {
                "avulsa": 1,
                "recorrente": 2,
            }
            ranking_doadores_query = ranking_doadores_query.filter(
                Pedido.periodicidade == doacao_mapping[filtros.tipo_doacao]
            )

        if filtros.fk_campanhas_ids:
            ranking_doadores_query = ranking_doadores_query.filter(
                Pedido.fk_campanha_id.in_(
                    list(map(int, filtros.fk_campanhas_ids.split(",")))
                )
            )

        if (
            str(current_user["nome_perfil"]).lower()
            == ProfilesEnum.GESTOR_DOACOES.lower()
        ):
            ranking_doadores_query = ranking_doadores_query.filter(
                Pedido.anonimo == False
            )

        ranking_doadores_paginated = ranking_doadores_query.paginate(
            page=filtros.page,
            per_page=filtros.per_page,
            error_out=False,
        )

        ranking_doadores, total = (
            ranking_doadores_paginated.items,
            ranking_doadores_paginated.total,
        )

        return ranking_doadores, total

    def get_regular_donors(
        self,
        filtros: GetRegularDonorsQueryFilter,
        mes_inicial: date,
        mes_final: date,
    ):
        ranking_doadores_assiduos_query = (
            self.__database.session.query(
                Clifor.nome,
                func.max(Clifor.id).label("fk_clifor_id"),
                Usuario.id.label("fk_usuario_id"),
                func.month(ProcessamentoPedido.data_processamento).label("mes"),
                func.year(ProcessamentoPedido.data_processamento).label("ano"),
                func.count(ProcessamentoPedido.id).label("doacoes_mes"),
                func.sum(ProcessamentoPedido.valor).label("valor_doacoes"),
            )
            .select_from(Pedido)
            .join(
                ProcessamentoPedido,
                Pedido.id == ProcessamentoPedido.fk_pedido_id,
            )
            .join(Clifor, Clifor.id == Pedido.fk_clifor_id)
            .outerjoin(Usuario, Usuario.id == Clifor.fk_usuario_id)
            .filter(
                between(
                    func.cast(ProcessamentoPedido.data_processamento, Date),
                    mes_inicial,
                    mes_final,
                ),
                ProcessamentoPedido.status_processamento == 1,
                Clifor.cpf_cnpj.isnot(None),
                Pedido.contabilizar_doacao == 1,
                or_(Usuario.id.is_(None), Usuario.id != 2),  # Admin
            )
            .group_by(
                Clifor.nome,
                func.month(ProcessamentoPedido.data_processamento),
                func.year(ProcessamentoPedido.data_processamento),
                Usuario.id,
            )
            .order_by(
                desc("doacoes_mes"),
                Clifor.nome,
                desc("ano"),
                desc("mes"),
            )
        )

        if filtros.tipo_doacao:
            doacao_mapping = {
                "avulsa": 1,
                "recorrente": 2,
            }
            ranking_doadores_assiduos_query = ranking_doadores_assiduos_query.filter(
                Pedido.periodicidade == doacao_mapping[filtros.tipo_doacao]
            )

        if filtros.fk_campanhas_ids:
            ranking_doadores_assiduos_query = ranking_doadores_assiduos_query.filter(
                Pedido.fk_campanha_id.in_(
                    list(map(int, filtros.fk_campanhas_ids.split(",")))
                )
            )

        if (
            str(current_user["nome_perfil"]).lower()
            == ProfilesEnum.GESTOR_DOACOES.lower()
        ):
            ranking_doadores_assiduos_query = ranking_doadores_assiduos_query.filter(
                Pedido.anonimo == False
            )

        ranking_doadores_assiduos = ranking_doadores_assiduos_query.all()

        return ranking_doadores_assiduos
    
    def exportar_doacoes(self, filtros_request): 
        busca_por_cpf = None
        busca_por_email = None
        busca_por_nome = None

        filtro_dinamico = filtros_request.filter_multiple

        if filtro_dinamico != None:
            is_cpf_query = self.__database.session.query(Clifor).filter(
                Clifor.cpf_cnpj.ilike(f"%{filtro_dinamico}%")
            )
            if is_cpf_query.first() is not None:
                busca_por_cpf = filtro_dinamico

            is_email_query = self.__database.session.query(Clifor).filter(
                Clifor.email.like(f"%{filtro_dinamico}%")
            )
            if is_email_query.first() is not None:
                busca_por_email = filtro_dinamico

            is_nome_query = self.__database.session.query(Clifor).filter(
                Clifor.nome.like(f"%{filtro_dinamico}%")
            )
            if is_nome_query.first() is not None:
                busca_por_nome = filtro_dinamico

        colunas_para_consulta = [
            Usuario.deleted_at,
            Pedido.anonimo,
            Clifor.id,
            Clifor.nome,
            Clifor.cpf_cnpj,
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
            Pedido.cancelada_por,
            GatewayPagamento.descricao.label("gateway_pagamento_nome"),
        ]

        filtros_listados = [
            (
                Pedido.fk_gateway_pagamento_id
                == filtros_request.fk_gateway_pagamento_id
                if filtros_request.fk_gateway_pagamento_id
                else True
            ),
            (
                ProcessamentoPedido.transaction_id.ilike(
                    f"%{filtros_request.transaction_id}%"
                )
                if filtros_request.transaction_id
                else True
            ),
            (
                ProcessamentoPedido.id_transacao_gateway.ilike(
                    f"%{filtros_request.codigo_referencial}%"
                )
                if filtros_request.codigo_referencial is not None
                else True
            ),
            (
                Clifor.cpf_cnpj.ilike(f"%{filtros_request.cpf}%")
                if filtros_request.cpf
                else True
            ),
            (
                Clifor.email.ilike(f"%{filtros_request.email}%")
                if filtros_request.email
                else True
            ),
            (Clifor.email.ilike(f"%{busca_por_email}%") if busca_por_email else True),
            (Clifor.nome.ilike(f"%{busca_por_nome}%") if busca_por_nome else True),
            (
                Clifor.nome.ilike(f"%{filtros_request.nome_cliente}%")
                if filtros_request.nome_cliente
                else True
            ),
            (Clifor.cpf_cnpj.ilike(f"%{busca_por_cpf}%") if busca_por_cpf else True),
            (
                ProcessamentoPedido.data_processamento >= filtros_request.data_inicial
                if filtros_request.data_inicial
                else True
            ),
            (
                ProcessamentoPedido.data_processamento <= filtros_request.data_final
                if filtros_request.data_final
                else True
            ),
            (
                ProcessamentoPedido.status_processamento == filtros_request.status
                if filtros_request.status != None
                else True
            ),
            (
                FormaPagamento.id == filtros_request.tipo_pagamento
                if filtros_request.tipo_pagamento
                else True
            ),
            Pedido.contabilizar_doacao == True,
            ProcessamentoPedido.contabilizar_doacao == True,
            (
                Pedido.status_pedido == 2
                if filtros_request.status_recorrencia == "canceladas"
                else True
            ),
            (
                Pedido.status_pedido == 1
                if filtros_request.status_recorrencia == "ativas"
                else True
            ),
            (
                Pedido.periodicidade == 2
                if filtros_request.recorrencia == "recorrente"
                else True
            ),
            (
                Pedido.periodicidade == 1
                if filtros_request.recorrencia == "nao_recorrente"
                else True
            ),
            (
                ProcessamentoPedido.fk_pedido_id == filtros_request.pedido_id
                if filtros_request.pedido_id
                else True
            ),
            (
                Campanha.id == filtros_request.campanha_id
                if filtros_request.campanha_id
                else True
            ),
            (
                Pedido.cancelada_por == filtros_request.cancelada_por
                if filtros_request.cancelada_por
                else True
            ),
        ]

        busca_todas_doacoes = (
            self.__database.session.query(*colunas_para_consulta)
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
            .filter(*filtros_listados)
            .distinct()
            .order_by(ProcessamentoPedido.data_processamento.desc())
        )

        if (
            filtros_request.doacao_anonima
            and str(current_user["nome_perfil"]).lower()
            != ProfilesEnum.GESTOR_DOACOES.lower()
        ):
            busca_todas_doacoes = busca_todas_doacoes.filter(
                Pedido.anonimo == filtros_request.doacao_anonima
            )
        elif (
            str(current_user["nome_perfil"]).lower()
            == ProfilesEnum.GESTOR_DOACOES.lower()
        ):
            busca_todas_doacoes = busca_todas_doacoes.filter(Pedido.anonimo == False)
        
        return busca_todas_doacoes.all()
        

    def get_listagem_de_doacoes(self, filtros_request: ListarDoacoesQuery) -> tuple:

        busca_por_cpf = None
        busca_por_email = None
        busca_por_nome = None

        filtro_dinamico = filtros_request.filter_multiple

        if filtro_dinamico != None:
            is_cpf_query = self.__database.session.query(Clifor).filter(
                Clifor.cpf_cnpj.ilike(f"%{filtro_dinamico}%")
            )
            if is_cpf_query.first() is not None:
                busca_por_cpf = filtro_dinamico

            is_email_query = self.__database.session.query(Clifor).filter(
                Clifor.email.like(f"%{filtro_dinamico}%")
            )
            if is_email_query.first() is not None:
                busca_por_email = filtro_dinamico

            is_nome_query = self.__database.session.query(Clifor).filter(
                Clifor.nome.like(f"%{filtro_dinamico}%")
            )
            if is_nome_query.first() is not None:
                busca_por_nome = filtro_dinamico

        colunas_para_consulta = [
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
            Pedido.cancelada_por,
            GatewayPagamento.descricao.label("gateway_pagamento_nome"),
        ]

        filtros_listados = [
            (
                Pedido.fk_gateway_pagamento_id
                == filtros_request.fk_gateway_pagamento_id
                if filtros_request.fk_gateway_pagamento_id
                else True
            ),
            (
                ProcessamentoPedido.transaction_id.ilike(
                    f"%{filtros_request.transaction_id}%"
                )
                if filtros_request.transaction_id
                else True
            ),
            (
                ProcessamentoPedido.id_transacao_gateway.ilike(
                    f"%{filtros_request.codigo_referencial}%"
                )
                if filtros_request.codigo_referencial is not None
                else True
            ),
            (
                Clifor.cpf_cnpj.ilike(f"%{filtros_request.cpf}%")
                if filtros_request.cpf
                else True
            ),
            (
                Clifor.email.ilike(f"%{filtros_request.email}%")
                if filtros_request.email
                else True
            ),
            (Clifor.email.ilike(f"%{busca_por_email}%") if busca_por_email else True),
            (Clifor.nome.ilike(f"%{busca_por_nome}%") if busca_por_nome else True),
            (
                Clifor.nome.ilike(f"%{filtros_request.nome_cliente}%")
                if filtros_request.nome_cliente
                else True
            ),
            (Clifor.cpf_cnpj.ilike(f"%{busca_por_cpf}%") if busca_por_cpf else True),
            (
                ProcessamentoPedido.data_processamento >= filtros_request.data_inicial
                if filtros_request.data_inicial
                else True
            ),
            (
                ProcessamentoPedido.data_processamento <= filtros_request.data_final
                if filtros_request.data_final
                else True
            ),
            (
                ProcessamentoPedido.status_processamento == filtros_request.status
                if filtros_request.status != None
                else True
            ),
            (
                FormaPagamento.id == filtros_request.tipo_pagamento
                if filtros_request.tipo_pagamento
                else True
            ),
            Pedido.contabilizar_doacao == True,
            ProcessamentoPedido.contabilizar_doacao == True,
            (
                Pedido.status_pedido == 2
                if filtros_request.status_recorrencia == "canceladas"
                else True
            ),
            (
                Pedido.status_pedido == 1
                if filtros_request.status_recorrencia == "ativas"
                else True
            ),
            (
                Pedido.periodicidade == 2
                if filtros_request.recorrencia == "recorrente"
                else True
            ),
            (
                Pedido.periodicidade == 1
                if filtros_request.recorrencia == "nao_recorrente"
                else True
            ),
            (
                ProcessamentoPedido.fk_pedido_id == filtros_request.pedido_id
                if filtros_request.pedido_id
                else True
            ),
            (
                Campanha.id == filtros_request.campanha_id
                if filtros_request.campanha_id
                else True
            ),
            (
                Pedido.cancelada_por == filtros_request.cancelada_por
                if filtros_request.cancelada_por
                else True
            ),
        ]

        busca_todas_doacoes = (
            self.__database.session.query(*colunas_para_consulta)
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
            .filter(*filtros_listados)
            .distinct()
            .order_by(ProcessamentoPedido.data_processamento.desc())
        )

        if (
            filtros_request.doacao_anonima
            and str(current_user["nome_perfil"]).lower()
            != ProfilesEnum.GESTOR_DOACOES.lower()
        ):
            busca_todas_doacoes = busca_todas_doacoes.filter(
                Pedido.anonimo == filtros_request.doacao_anonima
            )
        elif (
            str(current_user["nome_perfil"]).lower()
            == ProfilesEnum.GESTOR_DOACOES.lower()
        ):
            busca_todas_doacoes = busca_todas_doacoes.filter(Pedido.anonimo == False)

        paginate = busca_todas_doacoes.paginate(
            per_page=filtros_request.per_page,
            page=filtros_request.page,
            error_out=False,
        )

        total_doado_query = (
            self.__database.session.query(
                self.__database.func.sum(ProcessamentoPedido.valor)
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
            .filter(*filtros_listados)
        )

        if (
            filtros_request.doacao_anonima
            and str(current_user["nome_perfil"]).lower()
            != ProfilesEnum.GESTOR_DOACOES.lower()
        ):
            total_doado_query = total_doado_query.filter(
                Pedido.anonimo == filtros_request.doacao_anonima
            )
        elif (
            str(current_user["nome_perfil"]).lower()
            == ProfilesEnum.GESTOR_DOACOES.lower()
        ):
            total_doado_query = total_doado_query.filter(Pedido.anonimo == False)

        total_doado = total_doado_query.scalar() or 0

        return (paginate, total_doado)

    def get_listar_recorrencias_canceladas(
        self, filtros_request
    ) -> tuple[dict, HTTPStatus]:

        filtros_para_consulta = [
            Pedido.status_pedido == 2,
            Pedido.periodicidade == 2,
            Pedido.recorrencia_ativa == False,
            Pedido.contabilizar_doacao == True,
            (
                Usuario.nome.ilike(f"%{filtros_request.nome_usuario}%")
                if filtros_request.nome_usuario
                else True
            ),
            (
                Campanha.id == filtros_request.campanha_id
                if filtros_request.campanha_id
                else self.__database.true()
            ),
            (
                self.__database.cast(Pedido.data_pedido, self.__database.Date)
                >= self.__database.cast(filtros_request.data_inicial, self.__database.Date)
                if filtros_request.data_inicial
                else True
            ),
            (
                self.__database.cast(Pedido.data_pedido, self.__database.Date)
                <= self.__database.cast(filtros_request.data_final, self.__database.Date)
                if filtros_request.data_final
                else True
            ),
        ]

        doacoes_canceladas_consulta = (
            self.__database.session.query(
                Pedido.id,
                Pedido.cancelada_em,
                Clifor.nome,
                Campanha.titulo,
                Pedido.data_pedido,
                FormaPagamento.descricao.label("metodo_pagamento"),
                Pedido.valor_total_pedido,
                Pedido.cancelada_por,
            )
            .join(Clifor, Clifor.id == Pedido.fk_clifor_id)
            .join(Campanha, Campanha.id == Pedido.fk_campanha_id)
            .join(
                FormaPagamento,
                FormaPagamento.id == Pedido.fk_forma_pagamento_id,
            )
            .outerjoin(Usuario, Usuario.id == Clifor.fk_usuario_id)
            .filter(*filtros_para_consulta)
            .order_by(Pedido.data_pedido.desc())
        )

        doacoes_canceladas_paginate = doacoes_canceladas_consulta.paginate(
            page=filtros_request.page, per_page=filtros_request.per_page, error_out=False
        )

        informacoes_para_card = (
            self.__database.session.query(
                self.__database.func.count(Pedido.id),
                self.__database.func.sum(Pedido.valor_total_pedido),
            )
            .filter(
                Pedido.status_pedido == 2,
                Pedido.periodicidade == 2,
                Pedido.recorrencia_ativa == False,
                Pedido.contabilizar_doacao == True,
            )
            .all()
        )

        return doacoes_canceladas_paginate, informacoes_para_card

    def get_informacoes_sobre_usuario(self, fk_usuario_id):
        return (
            self.__database.session.query(Usuario)
            .filter(Usuario.id == fk_usuario_id)
            .first()
        )


    def query_doacoes_inadimplentes(self, filtros: ListagemDeRecorreciaEmLapsosRequest, objetivo: str):
        doacoes_nao_efetivadas_query = (
            self.__database.session.query(
                Pedido.id,
                Clifor.cpf_cnpj,
                Usuario.nome.label("benfeitor"),
                Usuario.id.label("benfeitor_id"),
                Pedido.data_pedido.label("data"),
                Pedido.valor_total_pedido.label("valor"),
                Campanha.titulo,
                Campanha.id.label("fk_campanha_id"),
            )
            .select_from(ProcessamentoPedido)
            .join(Pedido, Pedido.id == ProcessamentoPedido.fk_pedido_id)
            .join(Campanha, Campanha.id == Pedido.fk_campanha_id)
            .join(Clifor, Clifor.id == Pedido.fk_clifor_id)
            .outerjoin(Usuario, Usuario.id == Clifor.fk_usuario_id)
            .filter(
                (Campanha.id == filtros.campanha_id if filtros.campanha_id else True),
                (
                    self.__database.cast(Pedido.data_pedido, self.__database.Date) >= filtros.data_inicial if filtros.data_inicial else True  
                ),
                (
                    self.__database.cast(Pedido.data_pedido, self.__database.Date) <= filtros.data_final if filtros.data_final else True
                    
                ),
                Usuario.nome.ilike(f"%{filtros.nome}%") if filtros.nome else True,
                self.__database.text(
                    """
                        pedido.periodicidade = 2
                        AND pedido.recorrencia_ativa = 1
                        AND processamento_pedido.id IN (
                        SELECT TOP 4 sub_pp.id
                        FROM processamento_pedido sub_pp
                        WHERE sub_pp.fk_pedido_id = processamento_pedido.fk_pedido_id
                        ORDER BY sub_pp.data_processamento DESC)
                        """
                ),
            )
            .order_by(
                Pedido.data_pedido.desc(),
            )
            .group_by(
                Pedido.id,
                Usuario.nome,
                Usuario.id,
                Pedido.data_pedido,
                Pedido.valor_total_pedido,
                Campanha.titulo,
                Campanha.id,
                Clifor.cpf_cnpj
            )
            .having(
                self.__database.text(
                    """
            COUNT(*) = 4
            AND SUM(CASE WHEN processamento_pedido.status_processamento = 1 THEN 1 ELSE 0 END) = 0
            """
                )
            )
        )
        
        if objetivo == "listagem":
            return doacoes_nao_efetivadas_query.paginate(page=filtros.page, per_page=filtros.per_page, error_out=False)
        
        if objetivo == "exportar":
            return doacoes_nao_efetivadas_query.all()