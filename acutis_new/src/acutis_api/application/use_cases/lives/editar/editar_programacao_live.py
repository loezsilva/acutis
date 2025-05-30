from uuid import UUID

from acutis_api.communication.requests.lives import (
    EditarProgramacaoLiveRequest,
)
from acutis_api.communication.responses.padrao import ResponsePadraoSchema
from acutis_api.domain.repositories.lives import LivesRepositoryInterface
from acutis_api.exception.errors.not_found import HttpNotFoundError


class EditarProgramacaoLiveUseCase:
    def __init__(
        self, lives_repository: LivesRepositoryInterface
    ) -> list[ResponsePadraoSchema]:
        self.repository = lives_repository

    def execute(
        self, request: EditarProgramacaoLiveRequest, programacao_id: UUID
    ):
        tipo = request.tipo_programacao.lower()

        programacao_atualizada = self.repository.editar_programacao_live(
            programacao_id,
            tipo,
            data_hora_inicio=request.data_hora_inicio,
            dia_semana=request.dia_semana,
            hora_inicio=request.hora_inicio,
        )

        if not programacao_atualizada:
            raise HttpNotFoundError('Não foram encontradas lives programadas.')

        self.repository.salvar_dados()

        return ResponsePadraoSchema(
            msg='Programação da live atualizada com sucesso.'
        )
