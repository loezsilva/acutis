import uuid

from acutis_api.communication.responses.padrao import ResponsePadraoSchema
from acutis_api.domain.repositories.membros_oficiais import (
    MembrosOficiaisRepositoryInterface,
)
from acutis_api.exception.errors.not_found import HttpNotFoundError


class ExcluirMembroOficialUseCase:
    def __init__(self, repository: MembrosOficiaisRepositoryInterface):
        self.__repository = repository

    def execute(
        self, fk_membro_oficial_id: uuid.UUID
    ) -> dict[ResponsePadraoSchema]:
        membro_oficial_para_deletar = (
            self.__repository.buscar_membro_oficial_por_id(
                fk_membro_oficial_id
            )
        )

        if membro_oficial_para_deletar is None:
            raise HttpNotFoundError('Membro oficial não encontrado')

        self.__repository.remover_vinculos_de_superior(
            membro_oficial_para_deletar.fk_membro_id
        )

        self.__repository.admin_excluir_oficial(membro_oficial_para_deletar)

        self.__repository.salvar_dados()
