from acutis_api.application.use_cases.admin.exportar_dados import (
    BaseExportarUseCase,
)
from acutis_api.communication.requests.admin_exportar_dados import (
    ExportarMembrosRequest,
)
from acutis_api.domain.entities.lead import Lead
from acutis_api.domain.entities.membro import Membro
from acutis_api.domain.repositories.admin_exportar_dados import (
    ExportarDadosRepositoryInterface,
)


class ExportarMembrosUseCase(BaseExportarUseCase):
    @property
    def colunas_map(self):
        return {
            'id': Lead.id,
            'nome': Lead.nome,
            'email': Lead.email,
            'status': Lead.status,
            'origem_cadastro': Lead.origem_cadastro,
            'criado_em': Lead.criado_em,
            'ultimo_acesso': Lead.ultimo_acesso,
            'pais': Lead.pais,
            'telefone': Lead.telefone,
            'numero_documento': Membro.numero_documento,
            'data_nascimento': Membro.data_nascimento,
            'fk_lead_id': Membro.fk_lead_id,
            'sexo': Membro.sexo,
        }

    def __init__(
        self,
        repository: ExportarDadosRepositoryInterface,
    ):
        super().__init__(repository)

    def execute(self, request: ExportarMembrosRequest):
        return super().execute(request)

    def _executar_consulta(self, colunas_para_consulta, request):
        return self._repository.exportar_membros(
            colunas_para_consulta, request
        )

    def _nome_arquivo_exportacao(self):
        return 'exportar_membros'

    def _formatar_coluna(self, valor, *, coluna=None):
        if coluna == 'status':
            return 'ativo' if valor else 'inativo'
        return super()._formatar_coluna(valor, coluna=coluna)
