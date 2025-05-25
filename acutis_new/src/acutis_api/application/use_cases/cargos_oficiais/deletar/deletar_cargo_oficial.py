from acutis_api.domain.repositories.cargos_oficiais import (
    CargosOficiaisRepositoryInterface,
)
from acutis_api.exception.errors.not_found import HttpNotFoundError


class ExcluirCargoOficialUseCase:
    def __init__(self, repository: CargosOficiaisRepositoryInterface) -> dict:
        self.__repository = repository

    def execute(self, fk_cargo_id):
        cargo_para_deletar = self.__repository.busca_cargo_oficial_por_id(
            fk_cargo_id
        )

        if cargo_para_deletar is None:
            raise HttpNotFoundError('Cargo oficial não encontrado')

        self.__repository.buscar_oficiais_com_cargo_a_ser_deletado(fk_cargo_id)
        self.__repository.admin_deleta_cargo_oficial(fk_cargo_id)

        self.__repository.salvar_dados()

        return {'msg': 'Cargo oficial deletado com sucesso.'}
