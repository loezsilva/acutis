import uuid
from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Date, asc, between, cast, desc, distinct, func, or_

from acutis_api.domain.entities.benfeitor import Benfeitor
from acutis_api.domain.entities.doacao import Doacao
from acutis_api.domain.entities.lead import Lead
from acutis_api.domain.entities.lead_campanha import LeadCampanha
from acutis_api.domain.entities.membro import Membro
from acutis_api.domain.entities.pagamento_doacao import PagamentoDoacao
from acutis_api.domain.entities.processamento_doacao import (
    ProcessamentoDoacao,
    StatusProcessamentoEnum,
)
from acutis_api.domain.repositories.admin_membros import (
    AdminMembrosRepositoryInterface,
)
from acutis_api.domain.repositories.enums import TipoOrdenacaoEnum
from acutis_api.domain.repositories.enums.admin_membros import (
    TipoCadastroEnum,
)
from acutis_api.domain.repositories.schemas.admin_membros import (
    BuscarEstatisticasDoacoesMembroSchema,
    ListarLeadsMembrosFiltros,
    ListarLeadsMembrosSchema,
)


class AdminMembrosRepository(AdminMembrosRepositoryInterface):
    def __init__(self, database: SQLAlchemy):
        self._database = database

    def listar_leads_e_membros(  # NOSONAR
        self, filtros: ListarLeadsMembrosFiltros
    ) -> tuple[list[ListarLeadsMembrosSchema], int]:
        query = self._database.session.query(
            Lead.id.label('lead_id'),
            Lead.nome,
            Lead.email,
            Lead.telefone,
            Lead.pais,
            Lead.status.label('status_conta_lead'),
            func.format(Lead.ultimo_acesso, 'dd/MM/yyyy HH:mm').label(
                'ultimo_acesso'
            ),
            func.format(Lead.criado_em, 'dd/MM/yyyy HH:mm').label(
                'data_cadastro_lead'
            ),
            func.format(Lead.atualizado_em, 'dd/MM/yyyy HH:mm').label(
                'lead_atualizado_em'
            ),
            Membro.id.label('membro_id'),
            Membro.fk_benfeitor_id.label('benfeitor_id'),
            Membro.fk_endereco_id.label('endereco_id'),
            Membro.nome_social,
            func.format(Membro.data_nascimento, 'dd/MM/yyyy').label(
                'data_nascimento'
            ),
            Membro.numero_documento,
            Membro.sexo,
            Membro.foto,
            func.format(Membro.criado_em, 'dd/MM/yyyy HH:mm').label(
                'data_cadastro_membro'
            ),
            func.format(Membro.atualizado_em, 'dd/MM/yyyy HH:mm').label(
                'membro_atualizado_em'
            ),
            func.format(
                Membro.cadastro_atualizado_em, 'dd/MM/yyyy HH:mm'
            ).label('cadastro_membro_atualizado_em'),
        ).select_from(Lead)

        if filtros.ordenar_por:
            coluna = filtros.ordenar_por
            if filtros.tipo_ordenacao == TipoOrdenacaoEnum.decrescente:
                query = query.order_by(desc(coluna))
            else:
                query = query.order_by(asc(coluna))

        if filtros.tipo_cadastro == TipoCadastroEnum.lead:
            query = query.outerjoin(
                Membro, Lead.id == Membro.fk_lead_id
            ).where(Membro.id.is_(None))

        elif filtros.tipo_cadastro == TipoCadastroEnum.membro:
            query = query.join(Membro, Lead.id == Membro.fk_lead_id)
        else:
            query = query.outerjoin(Membro, Lead.id == Membro.fk_lead_id)

        if filtros.nome_email_documento:
            query = query.where(
                Lead.nome.contains(filtros.nome_email_documento)
                | Lead.email.contains(filtros.nome_email_documento)
                | Membro.numero_documento.contains(
                    filtros.nome_email_documento
                )
            )

        if filtros.telefone:
            query = query.where(Lead.telefone.contains(filtros.telefone))

        if filtros.campanha_origem:
            query = query.join(
                LeadCampanha, Lead.id == LeadCampanha.fk_lead_id
            )
            query = query.where(
                LeadCampanha.fk_campanha_id == filtros.campanha_origem
            )

        if filtros.data_cadastro_inicial:
            if filtros.tipo_cadastro == TipoCadastroEnum.lead:
                query = query.where(
                    between(
                        cast(Lead.criado_em, Date),
                        filtros.data_cadastro_inicial,
                        filtros.data_cadastro_final,
                    )
                )
            else:
                query = query.where(
                    between(
                        cast(Membro.criado_em, Date),
                        filtros.data_cadastro_inicial,
                        filtros.data_cadastro_final,
                    )
                )

        if filtros.ultimo_acesso_inicial:
            query = query.where(
                between(
                    cast(Lead.ultimo_acesso, Date),
                    filtros.ultimo_acesso_inicial,
                    filtros.ultimo_acesso_final,
                )
            )

        if filtros.status is not None:
            query = query.where(Lead.status == filtros.status)

        if filtros.filtro_dinamico:
            pesquisa = f'%{filtros.filtro_dinamico}%'
            query = query.where(
                or_(
                    Lead.nome.ilike(pesquisa),
                    Lead.email.ilike(pesquisa),
                    Lead.telefone.ilike(pesquisa),
                    Lead.pais.ilike(pesquisa),
                    Membro.nome_social.ilike(pesquisa),
                    Membro.numero_documento.ilike(pesquisa),
                    Membro.sexo.ilike(pesquisa),
                )
            )

        paginacao = query.paginate(
            page=filtros.pagina,
            per_page=filtros.por_pagina,
            error_out=False,
        )

        leads_membros, total = paginacao.items, paginacao.total

        return leads_membros, total

    def buscar_lead_por_id(self, id: uuid.UUID) -> Lead | None:
        lead = self._database.session.get(Lead, id)
        return lead

    def excluir_conta(self, lead: Lead) -> None:
        self._database.session.delete(lead)
        self._database.session.commit()

    def buscar_total_leads(self) -> int:
        total_leads = self._database.session.query(
            func.count(Lead.id)
        ).scalar()
        return total_leads

    def buscar_total_membros(self) -> int:
        total_membros = self._database.session.query(
            func.count(Membro.id)
        ).scalar()
        return total_membros

    def buscar_leads_periodo(self, inicio: datetime, fim: datetime) -> int:
        return (
            self._database.session.query(func.count(Lead.id))
            .filter(
                Lead.criado_em.between(inicio, fim),
            )
            .scalar()
        )

    def buscar_membros_periodo(self, inicio: datetime, fim: datetime) -> int:
        return (
            self._database.session.query(func.count(Membro.id))
            .filter(
                Membro.criado_em.between(inicio, fim),
            )
            .scalar()
        )

    def buscar_estatisticas_doacoes_do_membro(
        self, membro_id: uuid.UUID
    ) -> BuscarEstatisticasDoacoesMembroSchema:
        query = (
            self._database.session.query(
                func.count(distinct(Doacao.id)).label('quantidade_doacoes'),
                func.coalesce(func.sum(PagamentoDoacao.valor), 0.0).label(
                    'valor_total_doacoes'
                ),
                func.max(ProcessamentoDoacao.criado_em).label('ultima_doacao'),
            )
            .join(Doacao, Doacao.id == PagamentoDoacao.fk_doacao_id)
            .join(Benfeitor, Doacao.fk_benfeitor_id == Benfeitor.id)
            .join(
                ProcessamentoDoacao,
                ProcessamentoDoacao.fk_pagamento_doacao_id
                == PagamentoDoacao.id,
            )
            .filter(
                Benfeitor.membro.has(id=membro_id),
                Benfeitor.contabilizar == True,
                Doacao.contabilizar == True,
                ProcessamentoDoacao.status == StatusProcessamentoEnum.pago,
                PagamentoDoacao.anonimo == False,
            )
        )

        resultado = query.first()
        return resultado

    def buscar_numero_de_campanhas_do_membro(
        self, membro_id: uuid.UUID
    ) -> int:
        num_campanhas = (
            self._database.session.query(func.count(LeadCampanha.id))
            .join(Membro, Membro.fk_lead_id == LeadCampanha.fk_lead_id)
            .filter(Membro.id == membro_id)
            .scalar()
        )

        return num_campanhas
