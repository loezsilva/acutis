import uuid
from datetime import datetime, timedelta

import pytest
from dateutil.relativedelta import relativedelta

from acutis_api.domain.entities.campanha import Campanha
from acutis_api.domain.entities.doacao import Doacao
from acutis_api.domain.entities.lead import Lead
from acutis_api.domain.entities.processamento_doacao import (
    StatusProcessamentoEnum,
)
from acutis_api.infrastructure.extensions import database
from tests.factories import (
    BenfeitorFactory,
    DoacaoFactory,
    EnderecoFactory,
    LeadFactory,
    MembroFactory,
    PagamentoDoacaoFactory,
    ProcessamentoDoacaoFactory,
)


@pytest.fixture
def seed_gera_4_doacoes():
    def _dados_doacao(
        *,
        campanha: Campanha,
        doacao_ativa: bool = True,
        doacao_recorrente: bool = True,
        status_doacao: StatusProcessamentoEnum = StatusProcessamentoEnum.pago,
        anonimo: bool = False,
    ) -> tuple[Lead, Doacao]:
        endereco = EnderecoFactory()
        database.session.add(endereco)
        lead = LeadFactory(status=True)
        lead.senha = '@Teste;1234'
        database.session.add(lead)
        benfeitor = BenfeitorFactory(
            nome='Yan da Pororoca', numero_documento='14069799334'
        )
        database.session.add(benfeitor)
        membro = MembroFactory(
            fk_lead_id=lead.id,
            fk_endereco_id=endereco.id,
            fk_benfeitor_id=benfeitor.id,
        )
        database.session.add(membro)
        for i in range(4):
            doacao = DoacaoFactory(
                fk_benfeitor_id=benfeitor.id,
                fk_campanha_doacao_id=campanha.campanha_doacao.id,
            )
            doacao.data_criacao = datetime.now() - timedelta(days=3 - i)
            database.session.add(doacao)
            pagamento_doacao = PagamentoDoacaoFactory(
                fk_doacao_id=doacao.id,
                codigo_ordem_pagamento=str(uuid.uuid4()),
                recorrente=doacao_recorrente,
                ativo=doacao_ativa,
                anonimo=anonimo,
            )
            pagamento_doacao.criado_em = datetime.now() - timedelta(days=3 - i)
            database.session.add(pagamento_doacao)

            processamento_doacao = ProcessamentoDoacaoFactory(
                fk_pagamento_doacao_id=pagamento_doacao.id,
                codigo_referencia=str(uuid.uuid4()),
                status=status_doacao,
            )
            processamento_doacao.criado_em = datetime.now() - timedelta(
                days=3 - i
            )
            database.session.add(processamento_doacao)
            database.session.commit()

        return lead, doacao

    return _dados_doacao


@pytest.fixture
def seed_gera_4_doacoes_mensais():
    def _dados_doacao(  # noqa: PLR0913
        *,
        campanha: Campanha,
        doacao_ativa: bool = True,
        doacao_recorrente: bool = True,
        status_doacao: StatusProcessamentoEnum = StatusProcessamentoEnum.pago,
        anonimo: bool = False,
        criado_em: datetime = None,
    ) -> tuple[Lead, Doacao]:
        endereco = EnderecoFactory()
        database.session.add(endereco)
        lead = LeadFactory(status=True)
        lead.senha = '@Teste;1234'
        database.session.add(lead)
        benfeitor = BenfeitorFactory(
            nome='Yan da Pororoca', numero_documento='14069725334'
        )
        database.session.add(benfeitor)
        membro = MembroFactory(
            fk_lead_id=lead.id,
            fk_endereco_id=endereco.id,
            fk_benfeitor_id=benfeitor.id,
        )
        database.session.add(membro)
        for i in range(4):
            doacao = DoacaoFactory(
                fk_benfeitor_id=benfeitor.id,
                fk_campanha_doacao_id=campanha.campanha_doacao.id,
            )
            doacao.data_criacao = datetime.now() - relativedelta(
                months=(3 - i)
            )

            if criado_em:
                doacao.data_criacao = criado_em
            database.session.add(doacao)
            pagamento_doacao = PagamentoDoacaoFactory(
                fk_doacao_id=doacao.id,
                codigo_ordem_pagamento=str(uuid.uuid4()),
                recorrente=doacao_recorrente,
                ativo=doacao_ativa,
                anonimo=anonimo,
            )
            pagamento_doacao.criado_em = datetime.now() - relativedelta(
                months=(3 - i)
            )

            if criado_em:
                pagamento_doacao.criado_em = criado_em
            database.session.add(pagamento_doacao)

            processamento_doacao = ProcessamentoDoacaoFactory(
                fk_pagamento_doacao_id=pagamento_doacao.id,
                codigo_referencia=str(uuid.uuid4()),
                status=status_doacao,
            )
            processamento_doacao.criado_em = datetime.now() - relativedelta(
                months=(3 - i)
            )

            if criado_em:
                processamento_doacao.criado_em = criado_em
            database.session.add(processamento_doacao)
            database.session.commit()

        return lead, doacao

    return _dados_doacao
