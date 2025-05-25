from acutis_api.application.use_cases.admin.exportar_dados import (
    BaseExportarUseCase,
)
from acutis_api.domain.entities.lead import Lead
from acutis_api.domain.entities.membro import Membro
from acutis_api.domain.entities.oficial import Oficial
from acutis_api.domain.repositories.admin_exportar_dados import (
    ExportarDadosRepositoryInterface,
)


class ExportarMembrosOficiaisUseCase(BaseExportarUseCase):
    @property
    def colunas_map(self):
        return {
            'id': Oficial.id,
            'nome': Lead.nome,
            'email': Lead.email,
            'status': Oficial.status,
            'criado_em': Oficial.criado_em,
            'pais': Lead.pais,
            'telefone': Lead.telefone,
            'numero_documento': Membro.numero_documento,
            'data_nascimento': Membro.data_nascimento,
            'fk_lead_id': Membro.fk_lead_id,
            'sexo': Membro.sexo,
            'fk_superior_id': Oficial.fk_superior_id,
            'atualizado_por': Oficial.atualizado_por,
            'fk_membro_id': Oficial.fk_membro_id,
            'fk_cargo_oficial_id': Oficial.fk_cargo_oficial_id,
            'atualizado_em': Oficial.atualizado_em,
        }

    def __init__(self, repository: ExportarDadosRepositoryInterface):
        super().__init__(repository)

    def _executar_consulta(self, colunas_para_consulta, request):
        return self._repository.exportar_membros_oficiais(
            colunas_para_consulta, request
        )

    def _nome_arquivo_exportacao(self):
        return 'exportar_membros_oficiais'

    def _formatar_coluna(self, valor, *, coluna=None):
        if coluna == 'fk_superior_id':
            return (
                self._repository.buscar_nome_usuario_superior(valor).lead.nome
                if valor
                else None
            )
        elif coluna == 'fk_cargo_oficial_id':
            return (
                self._repository.buscar_nome_cargo_oficial(valor).nome_cargo
                if valor
                else None
            )
        return super()._formatar_coluna(valor, coluna=coluna)

    def execute(self, request):
        return super().execute(request)
