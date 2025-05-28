import uuid
from datetime import date

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Date, asc, between, cast, desc, func, select

from acutis_api.domain.entities.benfeitor import Benfeitor
from acutis_api.domain.entities.campanha import Campanha
from acutis_api.domain.entities.campanha_doacao import CampanhaDoacao
from acutis_api.domain.entities.doacao import Doacao
from acutis_api.domain.entities.membro import Membro
from acutis_api.domain.entities.pagamento_doacao import PagamentoDoacao
from acutis_api.domain.repositories.admin_benfeitores import (
    AdminBenfeitoresRepositoryInterface,
)
from acutis_api.domain.repositories.enums import TipoOrdenacaoEnum
from acutis_api.domain.repositories.schemas.admin_benfeitores import (
    BuscarCardsDoacoesBenfeitoresSchema,
    BuscarInformacoesBenfeitorSchema,
    ListarBenfeitoresFiltros,
    ListarBenfeitoresSchema,
    ListarDoacoesAnonimasBenfeitorSchema,
)
from acutis_api.domain.repositories.schemas.paginacao import PaginacaoQuery


class AdminBenfeitoresRepository(AdminBenfeitoresRepositoryInterface):
    def __init__(self, database: SQLAlchemy):
        self._database = database

    def buscar_cards_doacoes_benfeitores(  # noqa # NOSONAR
        self,
        mes_atual_inicio: date,
        mes_atual_final: date,
        mes_anterior_inicio: date,
        mes_anterior_final: date,
    ) -> BuscarCardsDoacoesBenfeitoresSchema:
        def calcular_percentual(atual: float, anterior: float) -> float | None:
            if anterior == 0:
                return 0
            return ((atual - anterior) / anterior) * 100

        def calcular_total_e_media(
            valores: list[float],
        ) -> tuple[float, float]:
            total = sum(valores)
            media = total / len(valores) if valores else 0
            return total, media

        session = self._database.session

        total_benfeitores_mes_atual = (
            session.query(func.count(Benfeitor.id))
            .filter(
                between(
                    cast(Benfeitor.criado_em, Date),
                    mes_atual_inicio,
                    mes_atual_final,
                )
            )
            .scalar()
        )

        total_benfeitores_mes_anterior = (
            session.query(func.count(Benfeitor.id))
            .filter(
                between(
                    cast(Benfeitor.criado_em, Date),
                    mes_anterior_inicio,
                    mes_anterior_final,
                )
            )
            .scalar()
        )

        doacoes_atual = (
            session.query(PagamentoDoacao.valor)
            .filter(
                PagamentoDoacao.anonimo == True,
                between(
                    cast(PagamentoDoacao.criado_em, Date),
                    mes_atual_inicio,
                    mes_atual_final,
                ),
            )
            .all()
        )

        doacoes_anterior = (
            session.query(PagamentoDoacao.valor)
            .filter(
                PagamentoDoacao.anonimo == True,
                between(
                    cast(PagamentoDoacao.criado_em, Date),
                    mes_anterior_inicio,
                    mes_anterior_final,
                ),
            )
            .all()
        )

        valores_atual = [float(d.valor) for d in doacoes_atual]
        valores_anterior = [float(d.valor) for d in doacoes_anterior]

        total_doacoes_anonimas_atual = len(valores_atual)
        total_montante_atual, media_ticket_atual = calcular_total_e_media(
            valores_atual
        )
        total_montante_anterior, media_ticket_anterior = (
            calcular_total_e_media(valores_anterior)
        )

        return BuscarCardsDoacoesBenfeitoresSchema(
            total_benfeitores=total_benfeitores_mes_atual,
            percentual_benfeitores=calcular_percentual(
                total_benfeitores_mes_atual, total_benfeitores_mes_anterior
            ),
            total_doacoes_anonimas=total_doacoes_anonimas_atual,
            percentual_quantidade_doacoes=calcular_percentual(
                total_doacoes_anonimas_atual, len(valores_anterior)
            ),
            total_montante_anonimo=total_montante_atual,
            percentual_total_valor=calcular_percentual(
                total_montante_atual, total_montante_anterior
            ),
            ticket_medio_anonimo=media_ticket_atual,
            percentual_ticket_medio=calcular_percentual(
                media_ticket_atual, media_ticket_anterior
            ),
        )

    def listar_benfeitores(
        self, filtros: ListarBenfeitoresFiltros
    ) -> tuple[list[ListarBenfeitoresSchema], int]:
        query = (
            self._database.session.query(
                Benfeitor.id,
                Benfeitor.nome,
                Benfeitor.numero_documento,
                Benfeitor.criado_em.label('registrado_em'),
                func.count(PagamentoDoacao.id).label('quantidade_doacoes'),
                func.coalesce(func.sum(PagamentoDoacao.valor), 0).label(
                    'montante_total'
                ),
                func.max(PagamentoDoacao.criado_em).label('ultima_doacao'),
            )
            .join(Doacao, Benfeitor.id == Doacao.fk_benfeitor_id)
            .join(
                CampanhaDoacao,
                Doacao.fk_campanha_doacao_id == CampanhaDoacao.id,
            )
            .join(
                Campanha,
                CampanhaDoacao.fk_campanha_id == Campanha.id,
            )
            .join(PagamentoDoacao, PagamentoDoacao.fk_doacao_id == Doacao.id)
            .where(
                PagamentoDoacao.anonimo == True,
                Doacao.contabilizar == True,
                Benfeitor.contabilizar == True,
            )
            .group_by(
                Benfeitor.id,
                Benfeitor.nome,
                Benfeitor.numero_documento,
                Benfeitor.criado_em,
            )
        )

        if filtros.ordenar_por:
            coluna = filtros.ordenar_por
            if filtros.tipo_ordenacao == TipoOrdenacaoEnum.decrescente:
                query = query.order_by(desc(coluna))
            else:
                query = query.order_by(asc(coluna))

        if filtros.id is not None:
            query = query.where(Benfeitor.id == filtros.id)

        if filtros.nome_documento is not None:
            query = query.where(
                Benfeitor.nome.contains(filtros.nome_documento)
                | Benfeitor.numero_documento.contains(filtros.nome_documento)
            )

        if filtros.registrado_em_inicio is not None:
            query = query.where(
                between(
                    cast(Benfeitor.criado_em, Date),
                    filtros.registrado_em_inicio,
                    filtros.registrado_em_fim,
                )
            )

        if filtros.ultima_doacao_inicio is not None:
            query = query.having(
                between(
                    cast(func.max(PagamentoDoacao.criado_em), Date),
                    filtros.ultima_doacao_inicio,
                    filtros.ultima_doacao_fim,
                )
            )

        if filtros.campanha_id is not None:
            query = query.where(Campanha.id == filtros.campanha_id)

        if filtros.somente_membros:
            query = query.join(Membro, Membro.fk_benfeitor_id == Benfeitor.id)

        paginacao = query.paginate(
            page=filtros.pagina,
            per_page=filtros.por_pagina,
            error_out=False,
        )

        benfeitores, total = paginacao.items, paginacao.total

        return benfeitores, total

    def buscar_informacoes_benfeitor_pelo_id(
        self, id: uuid.UUID
    ) -> BuscarInformacoesBenfeitorSchema:
        query = self._database.session.execute(
            select(
                Benfeitor.id,
                Benfeitor.nome,
                Benfeitor.numero_documento,
                Benfeitor.criado_em.label('registrado_em'),
                func.count(PagamentoDoacao.id).label('total_doacoes'),
                func.coalesce(func.sum(PagamentoDoacao.valor), 0).label(
                    'total_valor_doado'
                ),
                func.max(PagamentoDoacao.criado_em).label('ultima_doacao'),
            )
            .join(Doacao, Benfeitor.id == Doacao.fk_benfeitor_id)
            .join(PagamentoDoacao, Doacao.id == PagamentoDoacao.fk_doacao_id)
            .where(
                PagamentoDoacao.anonimo == True,
                Doacao.contabilizar == True,
                Benfeitor.contabilizar == True,
                Benfeitor.id == id,
            )
            .group_by(
                Benfeitor.id,
                Benfeitor.nome,
                Benfeitor.numero_documento,
                Benfeitor.criado_em,
            )
        )

        benfeitor = query.first()

        return benfeitor

    def listar_doacoes_anonimas_benfeitor_pelo_id(
        self, filtros: PaginacaoQuery, id: uuid.UUID
    ) -> tuple[list[ListarDoacoesAnonimasBenfeitorSchema], int]:
        query = (
            self._database.session.query(
                PagamentoDoacao.criado_em, PagamentoDoacao.valor
            )
            .select_from(Benfeitor)
            .join(Doacao, Benfeitor.id == Doacao.fk_benfeitor_id)
            .join(PagamentoDoacao, Doacao.id == PagamentoDoacao.fk_doacao_id)
            .where(
                PagamentoDoacao.anonimo == True,
                Doacao.contabilizar == True,
                Benfeitor.contabilizar == True,
                Benfeitor.id == id,
            )
            .order_by(PagamentoDoacao.criado_em.desc())
        )

        paginacao = query.paginate(
            page=filtros.pagina,
            per_page=filtros.por_pagina,
            error_out=False,
        )

        doacoes_anonimas, total = paginacao.items, paginacao.total

        return doacoes_anonimas, total
