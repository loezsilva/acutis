from acutis_api.communication.requests.admin_membros_oficiais import (
    AlterarCargoOficialRequest,
)
from acutis_api.domain.repositories.membros_oficiais import (
    MembrosOficiaisRepositoryInterface,
)
from acutis_api.exception.errors.bad_request import HttpBadRequestError
from acutis_api.exception.errors.not_found import HttpNotFoundError


class AlterarCargoMembroOficialUseCase:
    def __init__(self, repository: MembrosOficiaisRepositoryInterface):
        self.__repository = repository

    def execute(self, requisicao: AlterarCargoOficialRequest):
        busca_membro_oficial = self.__repository.buscar_membro_oficial_por_id(
            requisicao.fk_membro_oficial
        )

        busca_cargo_oficial = self.__repository.busca_cargo_oficial_por_id(
            requisicao.fk_cargo_oficial_id
        )

        if requisicao.fk_cargo_oficial_id is not None and (
            busca_cargo_oficial is None
        ):
            raise HttpNotFoundError('Cargo oficial não encontrado')

        if busca_membro_oficial is None:
            raise HttpNotFoundError('Membro oficial não encontrado')

        if busca_membro_oficial.fk_cargo_oficial_id == (
            requisicao.fk_cargo_oficial_id
        ):
            raise HttpBadRequestError('Membro Oficial já possui este cargo.')

        self.__repository.admin_alterar_cargo_oficial(
            busca_membro_oficial, requisicao
        )

        self.__repository.salvar_dados()
