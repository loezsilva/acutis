import uuid

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Date, Function, Label, between, cast, func, or_, select

from acutis_api.domain.entities.benfeitor import Benfeitor
from acutis_api.domain.entities.campanha import Campanha
from acutis_api.domain.entities.campanha_doacao import CampanhaDoacao
from acutis_api.domain.entities.cargo_oficial import CargosOficiais
from acutis_api.domain.entities.doacao import Doacao
from acutis_api.domain.entities.lead import Lead
from acutis_api.domain.entities.lead_campanha import LeadCampanha
from acutis_api.domain.entities.membro import Membro
from acutis_api.domain.entities.oficial import Oficial
from acutis_api.domain.entities.pagamento_doacao import PagamentoDoacao
from acutis_api.domain.entities.processamento_doacao import ProcessamentoDoacao
from acutis_api.domain.repositories.admin_exportar_dados import (
    ExportarDadosRepositoryInterface,
)
from acutis_api.domain.repositories.schemas.admin_exportar_dados import (
    ExportaLeadsSchema,
    ExportarBenfeitoresSchema,
    ExportarDoacoesSchema,
    ExportarMembrosSchema,
    ExportMembrosOficiaisSchema,
)


class ExportarDadosRepository(ExportarDadosRepositoryInterface):
    def __init__(self, database: SQLAlchemy):
        self.__database = database

    def buscar_nome_usuario_superior(
        self, membro_superior_id: uuid.UUID
    ) -> str | None:
        return self.__database.session.scalar(
            select(Membro).where(Membro.id == membro_superior_id)
        )

    def buscar_nome_cargo_oficial(
        self, cargo_oficial_id: uuid.UUID
    ) -> str | None:
        return self.__database.session.scalar(
            select(CargosOficiais).where(CargosOficiais.id == cargo_oficial_id)
        )

    def exportar_leads(self, colunas, requisicao: ExportaLeadsSchema) -> Lead:
        filtros_leads = []

        if requisicao.id is not None:
            filtros_leads.append(Lead.id == requisicao.id)

        if requisicao.campanha is not None:
            filtros_leads.append(
                LeadCampanha.fk_campanha_id == requisicao.campanha
            )

        if requisicao.pais is not None:
            filtros_leads.append(Lead.pais == requisicao.pais)

        if requisicao.email is not None:
            filtros_leads.append(Lead.email.ilike(f'%{requisicao.email}%'))

        if requisicao.nome is not None:
            filtros_leads.append(Lead.nome.ilike(f'%{requisicao.nome}%'))

        if requisicao.telefone is not None:
            filtros_leads.append(
                Lead.telefone.ilike(f'%{requisicao.telefone}%')
            )

        if requisicao.status is not None:
            filtros_leads.append(Lead.status == requisicao.status)

        if requisicao.origem_cadastro is not None:
            filtros_leads.append(
                Lead.origem_cadastro == requisicao.origem_cadastro
            )

        if requisicao.data_inicio is not None:
            filtros_leads.append(
                cast(Lead.criado_em, Date) >= requisicao.data_inicio
            )

        if requisicao.data_fim is not None:
            filtros_leads.append(
                cast(Lead.criado_em, Date) <= requisicao.data_fim
            )

        return (
            self.__database.session.query(*colunas)
            .select_from(Lead)
            .outerjoin(LeadCampanha, LeadCampanha.fk_lead_id == Lead.id)
            .filter(*filtros_leads)
            .distinct()
            .yield_per(3000)
        )

    def exportar_membros(self, colunas, requisicao: ExportarMembrosSchema):
        filtros_membros = []

        if requisicao.id is not None:
            filtros_membros.append(Membro.id == requisicao.id)

        if requisicao.campanha is not None:
            filtros_membros.append(
                LeadCampanha.fk_campanha_id == requisicao.campanha
            )

        if requisicao.email is not None:
            filtros_membros.append(Lead.email.ilike(f'%{requisicao.email}%'))

        if requisicao.nome is not None:
            filtros_membros.append(Lead.nome.ilike(f'%{requisicao.nome}%'))

        if requisicao.telefone is not None:
            filtros_membros.append(
                Lead.telefone.ilike(f'%{requisicao.telefone}%')
            )

        if requisicao.status is not None:
            filtros_membros.append(Lead.status == requisicao.status)

        if requisicao.origem_cadastro is not None:
            filtros_membros.append(
                Lead.origem_cadastro == requisicao.origem_cadastro
            )

        if requisicao.data_inicio is not None:
            filtros_membros.append(
                cast(Membro.criado_em, Date) >= requisicao.data_inicio
            )

        if requisicao.data_fim is not None:
            filtros_membros.append(
                cast(Membro.criado_em, Date) <= requisicao.data_fim
            )

        if requisicao.numero_documento is not None:
            filtros_membros.append(
                Membro.numero_documento.ilike(
                    f'%{requisicao.numero_documento}%'
                )
            )

        if requisicao.fk_lead_id is not None:
            filtros_membros.append(Membro.fk_lead_id == requisicao.fk_lead_id)

        if requisicao.sexo is not None:
            filtros_membros.append(Membro.sexo == requisicao.sexo)

        return (
            self.__database.session.query(*colunas)
            .select_from(Membro)
            .join(Lead, Membro.fk_lead_id == Lead.id)
            .outerjoin(LeadCampanha, LeadCampanha.fk_lead_id == Lead.id)
            .filter(*filtros_membros)
            .distinct()
            .yield_per(3000)
        )

    def exportar_membros_oficiais(
        self, colunas, requisicao: ExportMembrosOficiaisSchema
    ):
        filtros_oficiais = []

        if requisicao.id is not None:
            filtros_oficiais.append(Oficial.id == requisicao.id)

        if requisicao.email is not None:
            filtros_oficiais.append(Lead.email.ilike(f'%{requisicao.email}%'))

        if requisicao.nome is not None:
            filtros_oficiais.append(Lead.nome.ilike(f'%{requisicao.nome}%'))

        if requisicao.telefone is not None:
            filtros_oficiais.append(
                Lead.telefone.ilike(f'%{requisicao.telefone}%')
            )

        if requisicao.status is not None:
            filtros_oficiais.append(Oficial.status == requisicao.status)

        if requisicao.data_inicio is not None:
            filtros_oficiais.append(
                cast(Oficial.criado_em, Date) >= requisicao.data_inicio
            )

        if requisicao.data_fim is not None:
            filtros_oficiais.append(
                cast(Oficial.criado_em, Date) <= requisicao.data_fim
            )

        if requisicao.numero_documento is not None:
            filtros_oficiais.append(
                Membro.numero_documento.ilike(
                    f'%{requisicao.numero_documento}%'
                )
            )

        if requisicao.fk_superior_id is not None:
            filtros_oficiais.append(
                Membro.fk_superior_id == requisicao.fk_superior_id
            )

        if requisicao.fk_lead_id is not None:
            filtros_oficiais.append(Membro.fk_lead_id == requisicao.fk_lead_id)

        if requisicao.sexo is not None:
            filtros_oficiais.append(Membro.sexo == requisicao.sexo)

        return (
            self.__database.session.query(*colunas)
            .select_from(Oficial)
            .join(Membro, Oficial.fk_membro_id == Membro.id)
            .join(Lead, Lead.id == Membro.fk_lead_id)
            .filter(*filtros_oficiais)
            .yield_per(3000)
        )

    def exportar_doacoes(  # NOSONAR
        self, colunas, request: ExportarDoacoesSchema
    ):
        filtros_doacoes = []

        if request.nome_email_documento:
            filtros_doacoes.append(
                or_(
                    Benfeitor.nome.contains(request.nome_email_documento),
                    Lead.email.contains(request.nome_email_documento),
                    Benfeitor.numero_documento.contains(
                        request.nome_email_documento
                    ),
                )
            )

        if request.campanha_id:
            filtros_doacoes.append(Campanha.id == request.campanha_id)

        if request.campanha_nome:
            filtros_doacoes.append(
                Campanha.nome.contains(request.campanha_nome)
            )

        if request.data_doacao_cancelada_em_inicial:
            filtros_doacoes.append(
                between(
                    cast(Doacao.cancelado_em, Date),
                    request.data_doacao_cancelada_em_inicial,
                    request.data_doacao_cancelada_em_final,
                )
            )

        if request.data_doacao_criada_em_inicial:
            filtros_doacoes.append(
                between(
                    cast(Doacao.criado_em, Date),
                    request.data_doacao_criada_em_inicial,
                    request.data_doacao_criada_em_final,
                )
            )

        if request.recorrente is not None:
            filtros_doacoes.append(
                PagamentoDoacao.recorrente == request.recorrente
            )

        if request.forma_pagamento:
            filtros_doacoes.append(
                PagamentoDoacao.forma_pagamento == request.forma_pagamento
            )

        if request.codigo_ordem_pagamento:
            filtros_doacoes.append(
                PagamentoDoacao.codigo_ordem_pagamento.contains(
                    request.codigo_ordem_pagamento
                )
            )

        if request.anonimo is not None:
            filtros_doacoes.append(PagamentoDoacao.anonimo == request.anonimo)

        if request.gateway:
            filtros_doacoes.append(PagamentoDoacao.gateway == request.gateway)

        if request.ativo is not None:
            filtros_doacoes.append(PagamentoDoacao.ativo == request.ativo)

        if request.doacao_processada_em_inicial:
            filtros_doacoes.append(
                between(
                    cast(ProcessamentoDoacao.processado_em, Date),
                    request.doacao_processada_em_inicial,
                    request.doacao_processada_em_final,
                )
            )

        if request.codigo_transacao:
            filtros_doacoes.append(
                ProcessamentoDoacao.codigo_transacao.contains(
                    request.codigo_transacao
                )
            )

        if request.codigo_comprovante:
            filtros_doacoes.append(
                ProcessamentoDoacao.codigo_comprovante.contains(
                    request.codigo_comprovante
                )
            )

        if request.nosso_numero:
            filtros_doacoes.append(
                ProcessamentoDoacao.nosso_numero.contains(request.nosso_numero)
            )

        if request.status:
            filtros_doacoes.append(
                ProcessamentoDoacao.status == request.status
            )

        return (
            self.__database.session.query(*colunas)
            .select_from(Benfeitor)
            .outerjoin(Membro, Benfeitor.id == Membro.fk_benfeitor_id)
            .outerjoin(Lead, Membro.fk_lead_id == Lead.id)
            .join(Doacao, Benfeitor.id == Doacao.fk_benfeitor_id)
            .join(
                CampanhaDoacao,
                Doacao.fk_campanha_doacao_id == CampanhaDoacao.id,
            )
            .join(
                Campanha,
                CampanhaDoacao.fk_campanha_id == Campanha.id,
            )
            .join(PagamentoDoacao, Doacao.id == PagamentoDoacao.fk_doacao_id)
            .join(
                ProcessamentoDoacao,
                PagamentoDoacao.id
                == ProcessamentoDoacao.fk_pagamento_doacao_id,
            )
            .filter(*filtros_doacoes)
            .yield_per(3000)
        )

    def exportar_benfeitores(
        self, colunas, request: ExportarBenfeitoresSchema
    ):
        colunas_normais = [
            coluna
            for coluna in colunas
            if (
                not (
                    isinstance(coluna, Label)
                    and isinstance(coluna.element, Function)
                )
            )
        ]

        query = (
            self.__database.session.query(*colunas)
            .select_from(Benfeitor)
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
            .group_by(*colunas_normais)
        )

        if request.nome_documento is not None:
            query = query.where(
                or_(
                    Benfeitor.nome.contains(request.nome_documento),
                    Benfeitor.numero_documento.contains(
                        request.nome_documento
                    ),
                )
            )

        if request.campanha_id:
            query = query.where(Campanha.id == request.campanha_id)

        if request.campanha_nome:
            query = query.where(Campanha.nome.contains(request.campanha_nome))

        if request.registrado_em_inicio is not None:
            query = query.where(
                between(
                    cast(Benfeitor.criado_em, Date),
                    request.registrado_em_inicio,
                    request.registrado_em_fim,
                )
            )

        if request.ultima_doacao_inicio is not None:
            query = query.having(
                between(
                    cast(func.max(PagamentoDoacao.criado_em), Date),
                    request.ultima_doacao_inicio,
                    request.ultima_doacao_fim,
                )
            )

        return query.yield_per(3000)
