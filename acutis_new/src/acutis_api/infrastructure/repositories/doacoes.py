import uuid
from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import select

from acutis_api.domain.entities import (
    Benfeitor,
    Campanha,
    Doacao,
    Lead,
    Membro,
    PagamentoDoacao,
    ProcessamentoDoacao,
)
from acutis_api.domain.entities.processamento_doacao import (
    StatusProcessamentoEnum,
)
from acutis_api.domain.repositories.doacoes import DoacoesRepositoryInterface
from acutis_api.domain.repositories.schemas.doacoes import (
    RegistrarDoacaoSchema,
)


class DoacoesRepository(DoacoesRepositoryInterface):
    def __init__(self, database: SQLAlchemy):
        self._database = database

    def salvar_alteracoes(self):
        self._database.session.commit()

    def buscar_campanha_por_id(self, id: uuid.UUID) -> Campanha | None:
        campanha = self._database.session.get(Campanha, id)
        return campanha

    def buscar_benfeitor_por_numero_documento(
        self, numero_documento: str
    ) -> Benfeitor | None:
        benfeitor = self._database.session.scalar(
            select(Benfeitor).where(
                Benfeitor.numero_documento == numero_documento
            )
        )
        return benfeitor

    def registrar_membro_benfeitor(
        self, membro: Membro, numero_documento: str, nome: str
    ) -> Benfeitor:
        benfeitor = Benfeitor(
            numero_documento=numero_documento,
            nome=nome,
        )
        self._database.session.add(benfeitor)

        membro.fk_benfeitor_id = benfeitor.id
        self._database.session.add(membro)
        self._database.session.flush()
        self._database.session.refresh(membro)

    def vincular_membro_benfeitor(self, membro: Membro, benfeitor: Benfeitor):
        membro.fk_benfeitor_id = benfeitor.id
        self._database.session.add(membro)
        self._database.session.flush()
        self._database.session.refresh(membro)

    def registrar_doacao(self, dados_doacao: RegistrarDoacaoSchema):
        doacao = Doacao(
            fk_benfeitor_id=dados_doacao.benfeitor_id,
            fk_campanha_doacao_id=dados_doacao.campanha_doacao_id,
        )
        self._database.session.add(doacao)

        pagamento_doacao = PagamentoDoacao(
            fk_doacao_id=doacao.id,
            valor=dados_doacao.valor_doacao,
            recorrente=dados_doacao.recorrente,
            forma_pagamento=dados_doacao.forma_pagamento,
            codigo_ordem_pagamento=dados_doacao.codigo_ordem_pagamento,
            anonimo=dados_doacao.anonimo,
            gateway=dados_doacao.gateway,
        )
        self._database.session.add(pagamento_doacao)

        processamento_doacao = ProcessamentoDoacao(
            fk_pagamento_doacao_id=pagamento_doacao.id,
            forma_pagamento=dados_doacao.forma_pagamento,
            codigo_referencia=dados_doacao.codigo_referencia,
            codigo_transacao=dados_doacao.codigo_transacao,
            nosso_numero=dados_doacao.nosso_numero,
            processado_em=dados_doacao.processado_em,
            status=dados_doacao.status,
        )
        self._database.session.add(processamento_doacao)
        self._database.session.flush()

    def buscar_doacao_por_id(self, id: uuid.UUID) -> Doacao | None:
        doacao = self._database.session.get(Doacao, id)
        return doacao

    def cancelar_doacao_recorrente(self, doacao: Doacao, lead: Lead):
        doacao.cancelado_em = datetime.now()
        doacao.cancelado_por = lead.membro.id

        doacao.pagamento_doacao.ativo = False
        self._database.session.add(doacao.pagamento_doacao)
        self._database.session.flush()

    def buscar_processamento_doacao_por_id(
        self, id: uuid.UUID
    ) -> ProcessamentoDoacao | None:
        processamento_doacao = self._database.session.get(
            ProcessamentoDoacao, id
        )
        return processamento_doacao

    def estornar_processamento_doacao_recorrente(
        self, processamento_doacao: ProcessamentoDoacao
    ):
        processamento_doacao.status = StatusProcessamentoEnum.estornado
        self._database.session.add(processamento_doacao)
        self._database.session.flush()

    def estornar_processamento_doacao_unica(
        self, processamento_doacao: ProcessamentoDoacao
    ):
        processamento_doacao.status = StatusProcessamentoEnum.estornado
        self._database.session.add(processamento_doacao)

        processamento_doacao.pagamento_doacao.ativo = False
        self._database.session.add(processamento_doacao)
        self._database.session.flush()
