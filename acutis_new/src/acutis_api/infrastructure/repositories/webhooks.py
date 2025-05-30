from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import select

from acutis_api.domain.entities.benfeitor import Benfeitor
from acutis_api.domain.entities.campanha import Campanha
from acutis_api.domain.entities.campanha_doacao import CampanhaDoacao
from acutis_api.domain.entities.doacao import Doacao
from acutis_api.domain.entities.lead import Lead
from acutis_api.domain.entities.membro import Membro
from acutis_api.domain.entities.pagamento_doacao import (
    FormaPagamentoEnum,
    GatewayPagamentoEnum,
    PagamentoDoacao,
)
from acutis_api.domain.entities.processamento_doacao import (
    ProcessamentoDoacao,
    StatusProcessamentoEnum,
)
from acutis_api.domain.repositories.schemas.webhooks import (
    BuscarDadosDoacaoSchema,
    RegistrarDoacaoAnonimaSchema,
)
from acutis_api.domain.repositories.webhooks import WebhooksRepositoryInterface


class WebhooksRepository(WebhooksRepositoryInterface):
    def __init__(self, database: SQLAlchemy):
        self._database = database

    def salvar_alteracoes(self):
        self._database.session.commit()

    def buscar_campanha_doacao_por_chave_pix(
        self, chave_pix: str
    ) -> CampanhaDoacao | None:
        campanha_doacao = self._database.session.scalar(
            select(CampanhaDoacao).where(CampanhaDoacao.chave_pix == chave_pix)
        )

        return campanha_doacao

    def buscar_benfeitor_por_numero_documento(
        self, numero_documento: str
    ) -> Benfeitor | None:
        benfeitor = self._database.session.scalar(
            select(Benfeitor).where(
                Benfeitor.numero_documento == numero_documento
            )
        )

        return benfeitor

    def registrar_benfeitor(
        self, nome: str, numero_documento: str
    ) -> Benfeitor:
        benfeitor = Benfeitor(nome=nome, numero_documento=numero_documento)
        self._database.session.add(benfeitor)
        self._database.session.flush()

        return benfeitor

    def registrar_doacao_anonima(
        self, dados_doacao: RegistrarDoacaoAnonimaSchema
    ):
        doacao = Doacao(
            fk_benfeitor_id=dados_doacao.benfeitor_id,
            fk_campanha_doacao_id=dados_doacao.campanha_doacao_id,
        )
        self._database.session.add(doacao)

        pagamento_doacao = PagamentoDoacao(
            fk_doacao_id=doacao.id,
            valor=dados_doacao.valor_pagamento,
            recorrente=False,
            forma_pagamento=FormaPagamentoEnum.pix,
            anonimo=True,
            gateway=GatewayPagamentoEnum.itau,
        )
        self._database.session.add(pagamento_doacao)

        processamento_doacao = ProcessamentoDoacao(
            fk_pagamento_doacao_id=pagamento_doacao.id,
            forma_pagamento=FormaPagamentoEnum.pix,
            processado_em=dados_doacao.data_pagamento,
            codigo_transacao=dados_doacao.codigo_transacao,
            codigo_comprovante=dados_doacao.codigo_comprovante,
            status=StatusProcessamentoEnum.pago,
        )
        self._database.session.add(processamento_doacao)
        self._database.session.flush()

    def buscar_processamento_doacao_por_codigo_transacao(
        self, codigo_transacao: str
    ) -> ProcessamentoDoacao | None:
        processamento_doacao = self._database.session.scalar(
            select(ProcessamentoDoacao).where(
                ProcessamentoDoacao.codigo_transacao == codigo_transacao
            )
        )

        return processamento_doacao

    def atualizar_status_processamento_doacao(
        self,
        processamento_doacao: ProcessamentoDoacao,
        codigo_comprovante: str,
    ):
        processamento_doacao.status = StatusProcessamentoEnum.pago
        processamento_doacao.codigo_comprovante = codigo_comprovante
        processamento_doacao.processado_em = datetime.now()

        self._database.session.add(processamento_doacao)
        self._database.session.flush()
        self._database.session.refresh(processamento_doacao)

    def buscar_dados_doacao_por_processamento_doacao(
        self, processamento_doacao: ProcessamentoDoacao
    ) -> BuscarDadosDoacaoSchema:
        dados_doacao = self._database.session.execute(
            select(
                Lead.nome,
                Lead.email,
                Campanha.capa.label('foto_campanha'),
                Campanha.nome.label('nome_campanha'),
            )
            .select_from(ProcessamentoDoacao)
            .join(
                PagamentoDoacao,
                ProcessamentoDoacao.fk_pagamento_doacao_id
                == PagamentoDoacao.id,
            )
            .join(
                Doacao,
                PagamentoDoacao.fk_doacao_id == Doacao.id,
            )
            .join(
                CampanhaDoacao,
                Doacao.fk_campanha_doacao_id == CampanhaDoacao.id,
            )
            .join(Campanha, CampanhaDoacao.fk_campanha_id == Campanha.id)
            .join(
                Benfeitor,
                Doacao.fk_benfeitor_id == Benfeitor.id,
            )
            .join(
                Membro,
                Benfeitor.id == Membro.fk_benfeitor_id,
            )
            .join(Lead, Membro.fk_lead_id == Lead.id)
            .where(ProcessamentoDoacao.id == processamento_doacao.id)
        ).first()

        return dados_doacao

    def registrar_novo_processamento_doacao(
        self,
        pagamento_doacao_id: str,
        codigo_referencia: str,
        codigo_transacao: str,
        status_processamento: str,
    ) -> ProcessamentoDoacao:
        processamento_doacao = ProcessamentoDoacao(
            fk_pagamento_doacao_id=pagamento_doacao_id,
            processado_em=datetime.now(),
            codigo_referencia=codigo_referencia,
            codigo_transacao=codigo_transacao,
            status=status_processamento,
        )
        self._database.session.add(processamento_doacao)
        self._database.session.flush()

        return processamento_doacao

    def buscar_pagamento_doacao_por_codigo_ordem(
        self, codigo_ordem_pagamento: str
    ) -> PagamentoDoacao | None:
        pagamento_doacao = self._database.session.scalar(
            select(PagamentoDoacao).where(
                PagamentoDoacao.codigo_ordem_pagamento
                == codigo_ordem_pagamento
            )
        )

        return pagamento_doacao
