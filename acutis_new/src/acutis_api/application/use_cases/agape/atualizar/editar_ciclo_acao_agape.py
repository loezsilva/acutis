from acutis_api.application.utils.enderecos import generate_address_string
from acutis_api.communication.requests.agape import (
    RegistrarOuEditarCicloAcaoAgapeRequest,
)
from acutis_api.domain.entities.instancia_acao_agape import StatusAcaoAgapeEnum
from acutis_api.domain.repositories.agape import AgapeRepositoryInterface
from acutis_api.domain.repositories.schemas.agape import CoordenadasSchema
from acutis_api.domain.services.google_maps_service import GoogleMapsAPI
from acutis_api.exception.errors.bad_request import HttpBadRequestError
from acutis_api.exception.errors.not_found import HttpNotFoundError


class EditarCicloAcaoAgapeUseCase:
    """
    Caso de uso para editar um ciclo de ação Ágape:
    - Atualiza dados da instância (ação e abrangência)
    - Atualiza endereço e coordenadas
    - Atualiza itens do ciclo ajustando estoque
    """

    def __init__(
        self, repository: AgapeRepositoryInterface, gmaps: GoogleMapsAPI
    ):
        self.__repository = repository
        self.__gmaps = gmaps

    def execute(
        self, acao_agape_id, dados: RegistrarOuEditarCicloAcaoAgapeRequest
    ) -> None:
        # Busca a instância do ciclo
        ciclo_acao_agape = self.__repository.buscar_ciclo_acao_agape_por_id(
            acao_agape_id
        )

        if ciclo_acao_agape is None:
            raise HttpNotFoundError('Ciclo de ação não encontrado')

        # Só ciclos não iniciados podem ser editados
        if ciclo_acao_agape.status != StatusAcaoAgapeEnum.nao_iniciado:
            raise HttpBadRequestError(
                'Somente ciclos não iniciados podem ser atualizados.'
            )
        # Atualiza abrangência
        ciclo_acao_agape.abrangencia = dados.abrangencia

        # Atualiza endereço
        endereco = self.__repository.buscar_endereco_ciclo_acao_agape(
            acao_agape_id
        )
        str_endereco = generate_address_string(
            dados.endereco, dados.abrangencia
        )

        self.__repository.atualizar_endereco(
            endereco=endereco, dados_endereco=dados.endereco
        )

        # Atualiza coordenadas existentes
        if coordenada := endereco.coordenada:
            geolocalidade = self.__gmaps.get_geolocation(str_endereco)
            self.__repository.atualizar_coordenadas(
                coordenada=coordenada,
                dados_coordenada=CoordenadasSchema(
                    latitude=geolocalidade.latitude,
                    longitude=geolocalidade.longitude,
                    latitude_ne=geolocalidade.latitude_ne,
                    longitude_ne=geolocalidade.longitude_ne,
                    latitude_so=geolocalidade.latitude_so,
                    longitude_so=geolocalidade.longitude_so,
                ),
            )
        else:
            self.__repository.registrar_coordenada(
                endereco.id, self.__gmaps.get_geolocation(str_endereco)
            )

        # Restaura estoque dos itens
        itens_ciclo_acao = self.__repository.listar_itens_ciclo_acao_agape(
            ciclo_acao_agape.id
        )

        for item_ciclo in itens_ciclo_acao:
            self.__repository.retorna_item_estoque_ciclo_acao_agape(
                item_ciclo.id
            )

            self.__repository.deletar_item_ciclo_acao_agape(item_ciclo)

        # Registra novos itens do ciclo
        for doacao in dados.doacoes:
            item = self.__repository.buscar_item_estoque_por_id(doacao.item_id)

            if item is None:
                raise HttpNotFoundError(
                    f'Item {doacao.item_id} não encontrado.'
                )

            if int(doacao.quantidade) > int(item.quantidade):
                raise HttpNotFoundError(
                    f'Quantidade insuficiente em estoque para {item.item}.'
                )

            self.__repository.registrar_item_ciclo_acao_agape(
                ciclo_acao_id=str(ciclo_acao_agape.id), dados=doacao
            )

        # Persiste alterações
        self.__repository.salvar_alteracoes()
