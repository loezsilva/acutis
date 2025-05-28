from sqlalchemy import func

from acutis_api.application.use_cases.admin.exportar_dados import (
    BaseExportarUseCase,
)
from acutis_api.communication.requests.admin_exportar_dados import (
    ExportarBenfeitoresQuery,
)
from acutis_api.domain.entities.benfeitor import Benfeitor
from acutis_api.domain.entities.campanha import Campanha
from acutis_api.domain.entities.pagamento_doacao import PagamentoDoacao
from acutis_api.domain.repositories.admin_exportar_dados import (
    ExportarDadosRepositoryInterface,
)


class ExportarBenfeitoresUseCase(BaseExportarUseCase):
    @property
    def colunas_map(self):
        return {
            'benfeitor_id': Benfeitor.id,
            'nome': Benfeitor.nome,
            'registrado_em': Benfeitor.criado_em,
            'numero_documento': Benfeitor.numero_documento,
            'nome_campanha': Campanha.nome,
            'quantidade_doacoes': func.count(PagamentoDoacao.id).label(
                'quantidade_doacoes'
            ),
            'montante': func.coalesce(
                func.sum(PagamentoDoacao.valor), 0.0
            ).label('montante'),
            'ultima_doacao': func.max(PagamentoDoacao.criado_em).label(
                'ultima_doacao'
            ),
        }

    def __init__(self, repository: ExportarDadosRepositoryInterface):
        super().__init__(repository)

    def execute(self, request: ExportarBenfeitoresQuery):
        return super().execute(request)

    def _executar_consulta(self, colunas_para_consulta, request):
        return self._repository.exportar_benfeitores(
            colunas_para_consulta, request
        )

    def _nome_arquivo_exportacao(self):
        return 'exportar_benfeitores'
