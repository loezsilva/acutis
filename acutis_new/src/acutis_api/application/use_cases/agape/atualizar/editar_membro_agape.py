import uuid
from http import HTTPStatus

from acutis_api.communication.requests.agape import (
    EditarMembroAgapeRequestData
)
from acutis_api.communication.responses.padrao import ResponsePadraoSchema
from acutis_api.infrastructure.repositories.agape import (
    AgapeRepository,
)
from acutis_api.exception.errors.not_found import HttpNotFoundError

class EditarMembroAgapeUseCase:
    """
    Caso de uso para editar um membro ágape existente.
    """

    def __init__(self, agape_repository: AgapeRepository):
        self.agape_repository = agape_repository

    def execute(
        self, 
        membro_agape_id: uuid.UUID, 
        dados_edicao: EditarMembroAgapeRequestData
    ) -> tuple[ResponsePadraoSchema, HTTPStatus]:
        """
        Executa a lógica de edição do membro ágape.

        Args:
            membro_agape_id: O ID do membro ágape a ser editado.
            dados_edicao: Os dados para atualização do membro.

        Returns:
            Uma tupla contendo a mensagem de sucesso e o status HTTP.

        Raises:
            HttpNotFoundError: Se o membro ágape não for encontrado.
        """
        membro_existente = self.agape_repository.buscar_membro_agape_por_id(
            membro_agape_id=membro_agape_id
        )

        if not membro_existente:
            raise HttpNotFoundError(
                f'Membro Ágape com ID {membro_agape_id} não encontrado.'
            )

        # Atualiza apenas os campos fornecidos nos dados_edicao
        # O método model_dump com exclude_unset=True garante que apenas os campos
        # explicitamente enviados na requisição sejam considerados para atualização.
        dados_para_atualizar = dados_edicao.model_dump(exclude_unset=True)

        for campo, valor in dados_para_atualizar.items():
            if hasattr(membro_existente, campo):
                setattr(membro_existente, campo, valor)
            # Adicionar tratamento específico para campos se necessário,
            # por exemplo, se 'foto_documento' precisar de processamento especial.

        membro_atualizado = self.agape_repository.atualizar_membro_agape(
            membro_agape=membro_existente
        )

        # Se o repositório não retornar o membro atualizado ou se não for necessário,
        # pode-se remover a atribuição a 'membro_atualizado' e apenas chamar o método.
        # A linha acima é apenas um exemplo. A implementação exata do repositório
        # definirá como os dados são persistidos.

        return ResponsePadraoSchema(
            msg='Membro Ágape atualizado com sucesso.'
        ), HTTPStatus.OK
