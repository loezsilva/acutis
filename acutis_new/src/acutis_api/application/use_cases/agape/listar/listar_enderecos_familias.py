from http import HTTPStatus

from acutis_api.communication.responses.agape import (
    EnderecoFamiliaAgapeResponse,
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
    ) -> tuple[ListarEnderecosFamiliasAgapeResponse, HTTPStatus]:
        familias_com_enderecos = (
            self.agape_repository.listar_familias_com_enderecos()
        )

        enderecos_response_list = []
        if familias_com_enderecos:
            for familia_entity in familias_com_enderecos:
                if familia_entity.fk_endereco_id:
                    endereco_entity = (
                        self.agape_repository.buscar_endereco_por_id(
                            familia_entity.fk_endereco_id
                        )
                    )

                    enderecos_response_list.append(
                        EnderecoFamiliaAgapeResponse(
                            familia_id=familia_entity.id,
                            nome_familia=familia_entity.nome_familia,
                            endereco_id=endereco_entity.id,
                            codigo_postal=getattr(
                                endereco_entity, 'codigo_postal', None
                            ),
                            logradouro=getattr(
                                endereco_entity, 'logradouro', None
                            ),
                            bairro=getattr(endereco_entity, 'bairro', None),
                            cidade=getattr(endereco_entity, 'cidade', None),
                            estado=getattr(endereco_entity, 'estado', None),
                            numero=getattr(endereco_entity, 'numero', None),
                            complemento=getattr(
                                endereco_entity, 'complemento', None
                            ),
                        )
                    )

        return ListarEnderecosFamiliasAgapeResponse(
            root=enderecos_response_list
        ), HTTPStatus.OK
