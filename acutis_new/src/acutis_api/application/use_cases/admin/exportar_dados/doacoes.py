from acutis_api.application.use_cases.admin.exportar_dados import (
    BaseExportarUseCase,
)
from acutis_api.communication.requests.admin_exportar_dados import (
    ExportarDoacoesQuery,
)
from acutis_api.domain.entities.benfeitor import Benfeitor
from acutis_api.domain.entities.campanha import Campanha
from acutis_api.domain.entities.doacao import Doacao
from acutis_api.domain.entities.lead import Lead
from acutis_api.domain.entities.membro import Membro
from acutis_api.domain.entities.pagamento_doacao import PagamentoDoacao
from acutis_api.domain.entities.processamento_doacao import ProcessamentoDoacao
from acutis_api.domain.repositories.admin_exportar_dados import (
    ExportarDadosRepositoryInterface,
)


class ExportarDoacoesUseCase(BaseExportarUseCase):
    @property
    def colunas_map(self):
        return {
            'benfeitor_id': Benfeitor.id,
            'nome': Benfeitor.nome,
            'numero_documento': Benfeitor.numero_documento,
            'lead_id': Lead.id,
            'email': Lead.email,
            'telefone': Lead.telefone,
            'pais': Lead.pais,
            'ultimo_acesso': Lead.ultimo_acesso,
            'lead_status': Lead.status,
            'origem_cadastro': Lead.origem_cadastro,
            'membro_id': Membro.id,
            'nome_social': Membro.nome_social,
            'data_nascimento': Membro.data_nascimento,
            'sexo': Membro.sexo,
            'campanha_id': Campanha.id,
            'campanha_nome': Campanha.nome,
            'doacao_id': Doacao.id,
            'doacao_criada_em': Doacao.criado_em,
            'doacao_cancelada_em': Doacao.cancelado_em,
            'pagamento_doacao_id': PagamentoDoacao.id,
            'valor_doacao': PagamentoDoacao.valor,
            'recorrente': PagamentoDoacao.recorrente,
            'forma_pagamento': PagamentoDoacao.forma_pagamento,
            'codigo_ordem_pagamento': PagamentoDoacao.codigo_ordem_pagamento,
            'anonimo': PagamentoDoacao.anonimo,
            'gateway': PagamentoDoacao.gateway,
            'ativo': PagamentoDoacao.ativo,
            'processamento_doacao_id': ProcessamentoDoacao.id,
            'processado_em': ProcessamentoDoacao.processado_em,
            'codigo_referencia': ProcessamentoDoacao.codigo_referencia,
            'codigo_transacao': ProcessamentoDoacao.codigo_transacao,
            'codigo_comprovante': ProcessamentoDoacao.codigo_comprovante,
            'nosso_numero': ProcessamentoDoacao.nosso_numero,
            'status_processamento': ProcessamentoDoacao.status,
        }

    def __init__(self, repository: ExportarDadosRepositoryInterface):
        super().__init__(repository)

    def execute(self, request: ExportarDoacoesQuery):
        return super().execute(request)

    def _executar_consulta(self, colunas_para_consulta, request):
        return self._repository.exportar_doacoes(
            colunas_para_consulta, request
        )

    def _nome_arquivo_exportacao(self):
        return 'exportar_doacoes'
