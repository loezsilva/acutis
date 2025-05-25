from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Date, asc, between, cast, desc

from acutis_api.domain.entities import (
    Benfeitor,
    Campanha,
    CampanhaDoacao,
    Doacao,
    Lead,
    Membro,
    PagamentoDoacao,
    ProcessamentoDoacao,
)
from acutis_api.domain.repositories.admin_doacoes import (
    AdminDoacoesRepositoryInterface,
)
from acutis_api.domain.repositories.enums import TipoOrdenacaoEnum
from acutis_api.domain.repositories.schemas.admin_doacoes import (
    ListarDoacoesQuery,
    ListarDoacoesSchema,
)


class AdminDoacoesRepository(AdminDoacoesRepositoryInterface):
    def __init__(self, database: SQLAlchemy):
        self._database = database

    def listar_doacoes(  # NOSONAR
        self, filtros: ListarDoacoesQuery
    ) -> tuple[list[ListarDoacoesSchema], int]:
        query = (
            self._database.session.query(
                Benfeitor.id.label('benfeitor_id'),
                Benfeitor.nome.label('benfeitor_nome'),
                Lead.id.label('lead_id'),
                Membro.id.label('membro_id'),
                Campanha.id.label('campanha_id'),
                Campanha.nome.label('campanha_nome'),
                Doacao.id.label('doacao_id'),
                Doacao.criado_em.label('doacao_criada_em'),
                Doacao.cancelado_em.label('doacao_cancelada_em'),
                PagamentoDoacao.id.label('pagamento_doacao_id'),
                PagamentoDoacao.valor.label('valor_doacao'),
                PagamentoDoacao.recorrente,
                PagamentoDoacao.forma_pagamento,
                PagamentoDoacao.codigo_ordem_pagamento,
                PagamentoDoacao.anonimo,
                PagamentoDoacao.gateway,
                PagamentoDoacao.ativo,
                ProcessamentoDoacao.id.label('processamento_doacao_id'),
                ProcessamentoDoacao.processado_em,
                ProcessamentoDoacao.codigo_referencia,
                ProcessamentoDoacao.codigo_transacao,
                ProcessamentoDoacao.codigo_comprovante,
                ProcessamentoDoacao.nosso_numero,
                ProcessamentoDoacao.status,
            )
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
        )

        if filtros.ordenar_por:
            coluna = filtros.ordenar_por
            if filtros.tipo_ordenacao == TipoOrdenacaoEnum.decrescente:
                query = query.order_by(desc(coluna))
            else:
                query = query.order_by(asc(coluna))

        if filtros.nome_email_documento:
            query = query.where(
                Benfeitor.nome.contains(filtros.nome_email_documento)
                | Lead.email.contains(filtros.nome_email_documento)
                | Benfeitor.numero_documento.contains(
                    filtros.nome_email_documento
                )
            )

        if filtros.campanha_id:
            query = query.where(Campanha.id == filtros.campanha_id)

        if filtros.campanha_nome:
            query = query.where(Campanha.nome.contains(filtros.campanha_nome))

        if filtros.data_doacao_criada_em_inicial:
            query = query.where(
                between(
                    cast(Doacao.criado_em, Date),
                    filtros.data_doacao_criada_em_inicial,
                    filtros.data_doacao_criada_em_final,
                )
            )

        if filtros.data_doacao_cancelada_em_inicial:
            query = query.where(
                between(
                    cast(Doacao.cancelado_em, Date),
                    filtros.data_doacao_cancelada_em_inicial,
                    filtros.data_doacao_cancelada_em_final,
                )
            )

        if filtros.recorrente is not None:
            query = query.where(
                PagamentoDoacao.recorrente == filtros.recorrente
            )

        if filtros.forma_pagamento:
            query = query.where(
                PagamentoDoacao.forma_pagamento == filtros.forma_pagamento
            )

        if filtros.codigo_ordem_pagamento:
            query = query.where(
                PagamentoDoacao.codigo_ordem_pagamento.contains(
                    filtros.codigo_ordem_pagamento
                )
            )

        if filtros.anonimo is not None:
            query = query.where(PagamentoDoacao.anonimo == filtros.anonimo)

        if filtros.gateway:
            query = query.where(PagamentoDoacao.gateway == filtros.gateway)

        if filtros.ativo is not None:
            query = query.where(PagamentoDoacao.ativo == filtros.ativo)

        if filtros.doacao_processada_em_inicial:
            query = query.where(
                between(
                    cast(ProcessamentoDoacao.processado_em, Date),
                    filtros.doacao_processada_em_inicial,
                    filtros.doacao_processada_em_final,
                )
            )

        if filtros.codigo_transacao:
            query = query.where(
                ProcessamentoDoacao.codigo_transacao.contains(
                    filtros.codigo_transacao
                )
            )

        if filtros.codigo_comprovante:
            query = query.where(
                ProcessamentoDoacao.codigo_comprovante.contains(
                    filtros.codigo_comprovante
                )
            )

        if filtros.nosso_numero:
            query = query.where(
                ProcessamentoDoacao.nosso_numero.contains(filtros.nosso_numero)
            )

        if filtros.status:
            query = query.where(ProcessamentoDoacao.status == filtros.status)

        query = query.where(
            Benfeitor.contabilizar,
            Doacao.contabilizar,
        )

        paginacao = query.paginate(
            page=filtros.pagina,
            per_page=filtros.por_pagina,
            error_out=False,
        )

        doacoes, total = paginacao.items, paginacao.total

        return doacoes, total
