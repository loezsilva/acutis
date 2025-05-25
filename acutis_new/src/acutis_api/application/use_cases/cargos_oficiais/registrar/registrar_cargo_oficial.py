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


class RegistraNovoCargoOficialUseCase:
    def __init__(
        self, cargos_oficiais_repository: CargosOficiaisRepositoryInterface
    ):
        self.__repository = cargos_oficiais_repository

    def execute(self, request: RegistrarCargosOficiaisRequest) -> dict:
        verificar_se_ja_cadastrado = self.__repository.busca_cargo_por_nome(
            request.nome_cargo
        )

        if verificar_se_ja_cadastrado is not None:
            raise HttpConflictError('Já existe um cargo com este nome.')

        cargo_oficial = self.__repository.registrar_novo_cargo_vocacional(
            nome_cargo=request.nome_cargo,
            fk_cargo_superior_id=request.fk_cargo_superior_id,
        )

        self.__repository.salvar_dados()

        return RegistrarNovoCargoficialResponse.model_validate(
            cargo_oficial
        ).model_dump()
