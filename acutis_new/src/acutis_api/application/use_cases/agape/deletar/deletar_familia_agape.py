import uuid
from http import HTTPStatus

from acutis_api.domain.repositories.agape import AgapeRepositoryInterface
from acutis_api.exception.errors.not_found import HttpNotFoundError


class DeletarFamiliaAgapeUseCase:
    def __init__(self, repository: AgapeRepositoryInterface):
        self.__repository = repository

    def execute(self, familia_id: uuid.UUID) -> tuple[None, HTTPStatus]:
        familia = self.__repository.buscar_familia_por_id(familia_id)

        if familia is None:
            raise HttpNotFoundError(
                f"""Família com ID {familia_id}
                não encontrada ou já foi deletada."""
            )

        self.__repository.deletar_familia_e_membros(familia=familia)

        self.__repository.salvar_alteracoes()

        # Não há corpo na resposta, apenas o status.
        return None, HTTPStatus.NO_CONTENT
