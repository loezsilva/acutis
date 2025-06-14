from acutis_api.communication.responses.agape import (
    EnderecoComCoordenadasResponse,
    ListarEnderecosFamiliasAgapeResponse,
)
from acutis_api.domain.repositories.agape import AgapeRepositoryInterface


class ListarEnderecosFamiliasAgapeUseCase:
    """
    Caso de uso para listar todos os endereços das famílias ágape.
    """

    def __init__(self, agape_repository: AgapeRepositoryInterface):
        self.agape_repository = agape_repository

    def execute(
        self,
    ) -> ListarEnderecosFamiliasAgapeResponse:
        familias_com_enderecos = (
            self.agape_repository.listar_familias_com_enderecos()
        )

        lista_enderecos = []
        for familia in familias_com_enderecos:
            endereco = self.agape_repository.buscar_endereco_por_id(
                familia.fk_endereco_id
            )

            endereco_response = EnderecoComCoordenadasResponse.model_validate(
                endereco
            ).model_dump()

            if endereco.coordenada:
                endereco_response['latitude'] = endereco.coordenada.latitude
                endereco_response['longitude'] = endereco.coordenada.longitude

            lista_enderecos.append(endereco_response)

        return ListarEnderecosFamiliasAgapeResponse(
            resultados=lista_enderecos
        ).model_dump()
