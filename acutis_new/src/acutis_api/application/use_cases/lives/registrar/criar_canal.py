from acutis_api.communication.requests.lives import RegistrarCanalRequest
from acutis_api.communication.responses.padrao import ResponsePadraoSchema
from acutis_api.domain.repositories.lives import LivesRepositoryInterface
from acutis_api.exception.errors.conflict import HttpConflictError


class CriarCanalUseCase:
    def __init__(self, lives_repository: LivesRepositoryInterface):
        self.lives_repository = lives_repository

    def execute(self, request: RegistrarCanalRequest):
        if self.lives_repository.checar_existencia_canal(
            request.tag, request.rede_social
        ):
            raise HttpConflictError('Canal já cadastrado.')

        self.lives_repository.criar_canal(request)
        self.lives_repository.salvar_dados()

        return ResponsePadraoSchema(
            msg='Canal criado com sucesso.'
        ).model_dump()
