import uuid
from http import HTTPStatus

from acutis_api.communication.requests.agape import (
    EditarMembroAgapeRequestData,
)
from acutis_api.communication.responses.padrao import ResponsePadraoSchema
from acutis_api.exception.errors.not_found import HttpNotFoundError
from acutis_api.infrastructure.repositories.agape import (
    AgapeRepository,
)


class EditarMembroAgapeUseCase:
    """
    Caso de uso para editar um membro ágape existente.
    """

    def __init__(self, agape_repository: AgapeRepository):
        self.agape_repository = agape_repository

    def execute(
        self,
        membro_agape_id: uuid.UUID,
        dados_edicao: EditarMembroAgapeRequestData,
    ) -> tuple[ResponsePadraoSchema, HTTPStatus]:
        membro_existente = self.agape_repository.buscar_membro_agape_por_id(
            membro_agape_id=membro_agape_id
        )

        if not membro_existente:
            raise HttpNotFoundError(
                f'Membro Ágape com ID {membro_agape_id} não encontrado.'
            )

        dados_para_atualizar = dados_edicao.model_dump(exclude_unset=True)

        for campo, valor in dados_para_atualizar.items():
            if hasattr(membro_existente, campo):
                setattr(membro_existente, campo, valor)

        self.agape_repository.atualizar_membro_agape(
            membro_agape=membro_existente
        )

        return ResponsePadraoSchema(
            msg='Membro Ágape atualizado com sucesso.'
        ), HTTPStatus.OK
