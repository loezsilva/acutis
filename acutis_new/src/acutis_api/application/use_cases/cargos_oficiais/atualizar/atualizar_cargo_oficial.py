import uuid

from acutis_api.communication.requests.cargos_oficiais import (
    RegistrarCargosOficiaisRequest,
)
from acutis_api.communication.responses.cargos_oficiais import (
    RegistrarNovoCargoficialResponse,
)
from acutis_api.domain.repositories.cargos_oficiais import (
    CargosOficiaisRepositoryInterface,
)
from acutis_api.exception.errors.conflict import HttpConflictError
from acutis_api.exception.errors.not_found import HttpNotFoundError


class AtualizarCargoOficialUseCase:
    def __init__(self, repository: CargosOficiaisRepositoryInterface):
        self.__repository = repository

    def execute(
        self,
        request: RegistrarCargosOficiaisRequest,
        fk_cargo_oficial_id: uuid.UUID,
    ) -> RegistrarNovoCargoficialResponse:
        cargo_para_atualizar = self.__repository.busca_cargo_oficial_por_id(
            fk_cargo_oficial_id
        )
        nome_cargo_ja_cadastrado = self.__repository.busca_cargo_por_nome(
            request.nome_cargo
        )

        if cargo_para_atualizar is None:
            raise HttpNotFoundError('Cargo oficial não encontrado')

        if (
            nome_cargo_ja_cadastrado is not None
            and nome_cargo_ja_cadastrado.id != fk_cargo_oficial_id
        ):
            raise HttpConflictError('Já existe um cargo com mesmo nome')

        cargo_atualizado = self.__repository.atualizar_cargo_oficial(
            cargo_para_atualizar, request
        )

        self.__repository.salvar_dados()

        return RegistrarNovoCargoficialResponse.model_validate(
            cargo_atualizado
        ).model_dump()
