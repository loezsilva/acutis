from acutis_api.application.utils.funcoes_auxiliares import valida_cpf_cnpj
from acutis_api.application.utils.vocacional import (
    verifica_etapa_aprovada,
)
from acutis_api.communication.enums.vocacional import PassosVocacionalEnum
from acutis_api.communication.requests.vocacional import (
    RegistrarCadastroVocacionalRequest,
)
from acutis_api.domain.repositories.vocacional import (
    InterfaceVocacionalRepository,
)
from acutis_api.exception.errors_handler import (
    HttpConflictError,
    HttpNotFoundError,
)


class RegistrarCadastroVocacionalUseCase:
    def __init__(self, vocacional_repository: InterfaceVocacionalRepository):
        self.__vocacional_repository = vocacional_repository

    def execute(self, request: RegistrarCadastroVocacionalRequest):
        usuario_vocacional = (
            self.__vocacional_repository.verifica_usuario_vocacional(
                request.fk_usuario_vocacional_id
            )
        )
        if usuario_vocacional is None:
            raise HttpNotFoundError('Usuário vocacional não encontrado.')

        if usuario_vocacional.pais == 'brasil':
            valida_cpf_cnpj(request.documento_identidade, 'cpf')

        etapa = PassosVocacionalEnum.pre_cadastro.value

        busca_pre_cadastro = self.__vocacional_repository.busca_etapa_vocacional_por_usuario_e_etapa(  # noqa: E501
            request.fk_usuario_vocacional_id, etapa
        )

        verifica_etapa_aprovada(busca_pre_cadastro, etapa)

        if (
            self.__vocacional_repository.verifica_cadastro_vocacional(
                request.fk_usuario_vocacional_id
            )
            is not None
        ):
            raise HttpConflictError(
                'Cadastro vocacional já registrado anteriormente.'
            )

        if (
            self.__vocacional_repository.verifica_cpf_cadastrado(
                request.documento_identidade
            )
            is not None
        ):
            raise HttpConflictError(
                'Número do documento de identificação já cadastrado.'
            )
        self.__vocacional_repository.registrar_cadastro_vocacional(request)

        self.__vocacional_repository.salvar_alteracoes()
