from acutis_api.communication.enums.lives import TipoProgramacaoLiveEnum
from acutis_api.communication.requests.lives import (
    DeletarProgramacaoLiveRequest,
)
from acutis_api.communication.responses.padrao import ResponsePadraoSchema
from acutis_api.domain.entities.live_avulsa import LiveAvulsa
from acutis_api.domain.entities.live_recorrente import LiveRecorrente
from acutis_api.domain.repositories.lives import LivesRepositoryInterface
from acutis_api.exception.errors.not_found import HttpNotFoundError


class DeletarProgramacaoLiveUseCase:
    def __init__(self, repository: LivesRepositoryInterface):
        self.repository = repository

    def execute(self, request: DeletarProgramacaoLiveRequest):
        MAP_PROGRAMACAO = {
            TipoProgramacaoLiveEnum.AVULSA: LiveAvulsa,
            TipoProgramacaoLiveEnum.RECORRENTE: LiveRecorrente,
        }

        model = MAP_PROGRAMACAO.get(request.tipo_programacao)
        if model is None:
            raise ValueError('Tipo de programação inválido.')

        programacao = self.repository.buscar_programacao_por_id(
            programacao_id=request.programacao_id, model=model
        )

        if not programacao:
            raise HttpNotFoundError('Programação da live não encontrada.')

        self.repository.deletar_programacao_live(programacao)
        self.repository.salvar_dados()

        return ResponsePadraoSchema(
            msg='Programação da live deletada com sucesso.'
        ).model_dump()
