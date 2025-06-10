import uuid

from acutis_api.domain.entities.membro_agape import MembroAgape
from acutis_api.domain.repositories.agape import AgapeRepositoryInterface
from acutis_api.exception.errors.not_found import HttpNotFoundError


class DeletarMembroAgapeUseCase:
    def __init__(self, repository: AgapeRepositoryInterface):
        self.__repository = repository

    def execute(self, membro_agape_id: uuid.UUID) -> None:
        membro: MembroAgape | None = (
            self.__repository.buscar_membro_familia_por_id(
                membro_id=membro_agape_id
            )
        )

        if membro is None:
            raise HttpNotFoundError(
                f'Membro Ágape com ID {membro_agape_id} não encontrado.'
            )

        self.__repository.deletar_membro(membro_id=membro_agape_id)

        self.__repository.salvar_alteracoes()
