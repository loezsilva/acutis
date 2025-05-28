from acutis_api.communication.requests.membros import (
    AtualizarDadosMembroRequest,
)
from acutis_api.communication.responses.padrao import ResponsePadraoSchema
from acutis_api.domain.entities.lead import Lead
from acutis_api.domain.repositories.membros import (
    MembrosRepositoryInterface,
)


class AtualizarDadosMembroUseCase:
    def __init__(self, repository: MembrosRepositoryInterface):
        self._repository = repository

    def execute(
        self, request: AtualizarDadosMembroRequest, usuario_logado: Lead
    ) -> ResponsePadraoSchema:
        self._repository.atualizar_dados_membro(request, usuario_logado.membro)

        self._repository.salvar_alteracoes()

        return ResponsePadraoSchema(msg='Membro atualizado com sucesso.')
