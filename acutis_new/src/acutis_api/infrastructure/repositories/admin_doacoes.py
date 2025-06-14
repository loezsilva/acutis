import uuid
from datetime import datetime

from dateutil.relativedelta import relativedelta
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Date, asc, between, cast, desc, func

from acutis_api.communication.enums.admin_doacoes import (
    StatusProcessamentoEnum,
)
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
from acutis_api.domain.entities.lembrete_doacao_recorrente import (
    LembreteDoacaoRecorrente,
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

    def salvar_alteracoes(self):
        self._database.session.commit()

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
                Doacao.contabilizar,
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

        valor_total = (
            query.order_by(None)
            .with_entities(func.sum(PagamentoDoacao.valor))
            .scalar()
            or 0
        )

        response = query.paginate(
            page=filtros.pagina,
            per_page=filtros.por_pagina,
            error_out=False,
        )

        return response, valor_total

    def busca_doacao_por_id(self, fk_doacao_id: uuid.UUID):
        return (
            self._database.session.query(Doacao)
            .where(Doacao.id == fk_doacao_id)
            .scalar()
        )

    def alterar_considerar_doacao(self, doacao: Doacao):
        doacao.contabilizar = not doacao.contabilizar

        return doacao

    def card_doacoes_dia_atual(self):
        quantidade_hoje = (
            self._database.session.query(func.count(PagamentoDoacao.id))
            .join(Doacao, Doacao.id == PagamentoDoacao.fk_doacao_id)
            .join(
                ProcessamentoDoacao,
                ProcessamentoDoacao.fk_pagamento_doacao_id
                == PagamentoDoacao.id,
            )
            .filter(
                Doacao.contabilizar == True,
                ProcessamentoDoacao.status == StatusProcessamentoEnum.pago,
                func.extract('month', ProcessamentoDoacao.criado_em)
                == func.extract('month', func.now()),
                func.extract('day', ProcessamentoDoacao.criado_em)
                == func.extract('day', func.now()),
                func.extract('year', ProcessamentoDoacao.criado_em)
                == func.extract('year', func.now()),
            )
            .scalar()
            or 0
        )

        consulta_base = (
            self._database.session.query(func.sum(PagamentoDoacao.valor))
            .join(Doacao, Doacao.id == PagamentoDoacao.fk_doacao_id)
            .join(
                ProcessamentoDoacao,
                ProcessamentoDoacao.fk_pagamento_doacao_id
                == PagamentoDoacao.id,
            )
            .filter(Doacao.contabilizar == True)
        )

        total_hoje = (
            consulta_base.filter(
                ProcessamentoDoacao.status == StatusProcessamentoEnum.pago,
                func.extract('month', ProcessamentoDoacao.criado_em)
                == func.extract('month', func.now()),
                func.extract('day', ProcessamentoDoacao.criado_em)
                == func.extract('day', func.now()),
                func.extract('year', ProcessamentoDoacao.criado_em)
                == func.extract('year', func.now()),
            ).scalar()
            or 0
        )

        primeira_doacao = (
            self._database.session.query(ProcessamentoDoacao.criado_em)
            .filter(ProcessamentoDoacao.status == StatusProcessamentoEnum.pago)
            .order_by(ProcessamentoDoacao.criado_em)
            .first()
        )

        total_doado = (
            consulta_base.filter(
                ProcessamentoDoacao.status == StatusProcessamentoEnum.pago,
            ).scalar()
            or 0
        )

        return (
            round(total_hoje, 2),
            primeira_doacao,
            round(total_doado, 2),
            quantidade_hoje,
        )

    def card_doacoes_mes_atual(self):
        quantidade_mes = (
            self._database.session.query(func.count(PagamentoDoacao.id))
            .join(Doacao, Doacao.id == PagamentoDoacao.fk_doacao_id)
            .join(
                ProcessamentoDoacao,
                ProcessamentoDoacao.fk_pagamento_doacao_id
                == PagamentoDoacao.id,
            )
            .filter(
                Doacao.contabilizar == True,
                ProcessamentoDoacao.status == StatusProcessamentoEnum.pago,
                func.extract('month', ProcessamentoDoacao.criado_em)
                == func.extract('month', func.now()),
                func.extract('year', ProcessamentoDoacao.criado_em)
                == func.extract('year', func.now()),
            )
            .scalar()
            or 0
        )

        consulta_base = (
            self._database.session.query(func.sum(PagamentoDoacao.valor))
            .join(Doacao, Doacao.id == PagamentoDoacao.fk_doacao_id)
            .join(
                ProcessamentoDoacao,
                ProcessamentoDoacao.fk_pagamento_doacao_id
                == PagamentoDoacao.id,
            )
            .filter(Doacao.contabilizar == True)
        )

        total_mes = (
            consulta_base.filter(
                ProcessamentoDoacao.status == StatusProcessamentoEnum.pago,
                func.extract('month', ProcessamentoDoacao.criado_em)
                == func.extract('month', func.now()),
                func.extract('year', ProcessamentoDoacao.criado_em)
                == func.extract('year', func.now()),
            ).scalar()
            or 0
        )

        primeira_doacao = (
            self._database.session.query(ProcessamentoDoacao.criado_em)
            .filter(ProcessamentoDoacao.status == StatusProcessamentoEnum.pago)
            .order_by(ProcessamentoDoacao.criado_em)
            .first()
        )

        total_doado = (
            consulta_base.filter(
                ProcessamentoDoacao.status == StatusProcessamentoEnum.pago,
            ).scalar()
            or 0
        )

        return (
            round(total_mes, 2),
            primeira_doacao,
            round(total_doado, 2),
            quantidade_mes,
        )

    def soma_total_doacoes(self):
        total_doacao = (
            self._database.session.query(func.sum(PagamentoDoacao.valor))
            .join(Doacao, Doacao.id == PagamentoDoacao.fk_doacao_id)
            .join(
                ProcessamentoDoacao,
                ProcessamentoDoacao.fk_pagamento_doacao_id
                == PagamentoDoacao.id,
            )
            .filter(Doacao.contabilizar == True)
            .filter(
                ProcessamentoDoacao.status == StatusProcessamentoEnum.pago,
            )
            .scalar()
            or 0
        )

        primeira_doacao = (
            self._database.session.query(ProcessamentoDoacao.criado_em)
            .filter(ProcessamentoDoacao.status == StatusProcessamentoEnum.pago)
            .order_by(ProcessamentoDoacao.criado_em)
            .first()
        )

        return (total_doacao, primeira_doacao)

    def contabilizar_recorrencia_nao_efetuada_periodo(
        self, data_inicio: datetime, data_fim: datetime
    ):
        data_limite_inicio = data_inicio - relativedelta(months=1)
        data_limite_fim = data_fim - relativedelta(months=1)

        query = (
            self._database.session.query(
                func.count(PagamentoDoacao.id),
                func.sum(PagamentoDoacao.valor),
            )
            .join(Doacao, Doacao.id == PagamentoDoacao.fk_doacao_id)
            .join(Benfeitor, Benfeitor.id == Doacao.fk_benfeitor_id)
            .join(
                ProcessamentoDoacao,
                ProcessamentoDoacao.fk_pagamento_doacao_id
                == PagamentoDoacao.id,
            )
            .filter(
                Doacao.contabilizar == True,
                Benfeitor.contabilizar == True,
                PagamentoDoacao.recorrente == True,
                ProcessamentoDoacao.status == StatusProcessamentoEnum.expirado,
                ProcessamentoDoacao.criado_em >= data_limite_inicio,
                ProcessamentoDoacao.criado_em <= data_limite_fim,
            )
            .first()
        )

        quantidade, total = query if query else (0, 0)
        return (quantidade or 0, total or 0)

    def contabilizar_recorrencia_total(self) -> tuple[int, float, int]:
        query = (
            self._database.session.query(
                func.count(PagamentoDoacao.id),
                func.sum(PagamentoDoacao.valor),
                func.count(func.distinct(Doacao.fk_benfeitor_id)),
            )
            .join(Doacao, Doacao.id == PagamentoDoacao.fk_doacao_id)
            .join(Benfeitor, Benfeitor.id == Doacao.fk_benfeitor_id)
            .join(
                ProcessamentoDoacao,
                ProcessamentoDoacao.fk_pagamento_doacao_id
                == PagamentoDoacao.id,
            )
            .filter(
                Doacao.contabilizar == True,
                Benfeitor.contabilizar == True,
                PagamentoDoacao.recorrente == True,
            )
            .first()
        )

        qtd_doacoes, total, qtd_doadores = query if query else (0, 0, 0)
        return (qtd_doacoes or 0, total or 0, qtd_doadores or 0)

    def contabilizar_recorrencia_prevista_periodo(
        self, data_inicio: datetime, data_fim: datetime
    ) -> tuple[int, float]:
        query = (
            self._database.session.query(
                func.count(PagamentoDoacao.id),
                func.sum(PagamentoDoacao.valor),
            )
            .join(Doacao, Doacao.id == PagamentoDoacao.fk_doacao_id)
            .join(Benfeitor, Benfeitor.id == Doacao.fk_benfeitor_id)
            .join(
                ProcessamentoDoacao,
                ProcessamentoDoacao.fk_pagamento_doacao_id
                == PagamentoDoacao.id,
            )
            .filter(
                Doacao.contabilizar == True,
                Benfeitor.contabilizar == True,
                PagamentoDoacao.recorrente == True,
                ProcessamentoDoacao.status != StatusProcessamentoEnum.pago,
                ProcessamentoDoacao.criado_em >= data_inicio,
                ProcessamentoDoacao.criado_em <= data_fim,
            )
            .first()
        )

        quantidade, total = query if query else (0, 0)
        return (quantidade or 0, total or 0)

    def contabilizar_lembretes_efetivos(self) -> tuple[int, float]:
        query = (
            self._database.session.query(
                func.count(PagamentoDoacao.id),
                func.sum(PagamentoDoacao.valor),
                func.count(func.distinct(Doacao.fk_benfeitor_id)),
            )
            .select_from(LembreteDoacaoRecorrente)
            .join(
                ProcessamentoDoacao,
                ProcessamentoDoacao.id
                == LembreteDoacaoRecorrente.fk_processamento_doacao_id,
            )
            .join(
                PagamentoDoacao,
                PagamentoDoacao.id
                == ProcessamentoDoacao.fk_pagamento_doacao_id,
            )
            .join(Doacao, Doacao.id == PagamentoDoacao.fk_doacao_id)
            .join(Benfeitor, Benfeitor.id == Doacao.fk_benfeitor_id)
            .filter(
                Doacao.contabilizar == True,
                Benfeitor.contabilizar == True,
                PagamentoDoacao.recorrente == True,
                ProcessamentoDoacao.status == StatusProcessamentoEnum.pago,
            )
            .first()
        )

        qtd_doacoes, total, qtd_doadores = query if query else (0, 0, 0)
        return (qtd_doacoes or 0, total or 0, qtd_doadores or 0)

    def contabilizar_recorrencias_efetuadas_periodo(
        self, data_inicio: datetime, data_fim: datetime
    ) -> tuple[int, float]:
        consulta = (
            self._database.session.query(
                func.count(PagamentoDoacao.id),
                func.sum(PagamentoDoacao.valor),
            )
            .join(
                ProcessamentoDoacao,
                ProcessamentoDoacao.fk_pagamento_doacao_id
                == PagamentoDoacao.id,
            )
            .join(Doacao, Doacao.id == PagamentoDoacao.fk_doacao_id)
            .join(Benfeitor, Benfeitor.id == Doacao.fk_benfeitor_id)
            .filter(
                Benfeitor.contabilizar == True,
                Doacao.contabilizar == True,
                ProcessamentoDoacao.status == StatusProcessamentoEnum.pago,
                PagamentoDoacao.recorrente == True,
                ProcessamentoDoacao.criado_em >= data_inicio,
                ProcessamentoDoacao.criado_em <= data_fim,
            )
            .first()
        )

        quantidade, total = consulta if consulta else (0, 0)
        return (quantidade or 0, total or 0)

    def contabilizar_recorrencias_canceladas(self) -> tuple[int, float]:
        query = (
            self._database.session.query(
                func.count(PagamentoDoacao.id),
                func.sum(PagamentoDoacao.valor),
            )
            .join(Doacao, Doacao.id == PagamentoDoacao.fk_doacao_id)
            .join(
                ProcessamentoDoacao,
                ProcessamentoDoacao.fk_pagamento_doacao_id
                == PagamentoDoacao.id,
            )
            .filter(
                Doacao.contabilizar == True,
                PagamentoDoacao.recorrente == True,
                PagamentoDoacao.ativo == False,
            )
            .first()
        )

        quantidade, total = query if query else (0, 0)
        return (quantidade or 0, total or 0)
