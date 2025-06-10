from acutis_api.application.utils.enderecos import generate_address_string
from acutis_api.communication.requests.agape import (
    RegistrarOuEditarCicloAcaoAgapeRequest,
)
from acutis_api.domain.entities.instancia_acao_agape import StatusAcaoAgapeEnum
from acutis_api.domain.repositories.agape import AgapeRepositoryInterface
from acutis_api.domain.services.google_maps_service import GoogleMapsAPI
from acutis_api.exception.errors.not_found import HttpNotFoundError
from acutis_api.exception.errors.unprocessable_entity import (
    HttpUnprocessableEntityError,
)


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
            raise HttpUnprocessableEntityError(
                'Somente ciclos não iniciados podem ser atualizados.'
            )

        # Atualiza a ação relacionada
        nome_acao = self.__repository.buscar_nome_acao_por_id(
            dados.nome_acao_id
        )
        ciclo_acao_agape.fk_acao_agape_id = nome_acao.id

        # Atualiza abrangência
        ciclo_acao_agape.abrangencia = dados.abrangencia

        # Atualiza endereço
        endereco = self.__repository.buscar_endereco_ciclo_acao_agape(
            acao_agape_id
        )
        str_endereco = generate_address_string(
            dados.endereco, dados.abrangencia
        )

        endereco.codigo_postal = dados.endereco.cep
        endereco.logradouro = dados.endereco.rua
        endereco.bairro = dados.endereco.bairro
        endereco.cidade = dados.endereco.cidade
        endereco.estado = dados.endereco.estado
        endereco.numero = dados.endereco.numero
        endereco.complemento = dados.endereco.complemento

        # Atualiza coordenadas existentes
        if coordenada := endereco.coordenada:
            geolocalidade = self.__gmaps.get_geolocation(str_endereco)
            coordenada.latitude = geolocalidade.latitude
            coordenada.longitude = geolocalidade.longitude
            coordenada.latitude_ne = geolocalidade.latitude_ne
            coordenada.longitude_ne = geolocalidade.longitude_ne
            coordenada.latitude_so = geolocalidade.latitude_so
            coordenada.longitude_so = geolocalidade.longitude_so
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
            self.__repository.deletar_item_ciclo_acao_agape(item_ciclo.id)

        # Registra novos itens do ciclo
        for doacao in dados.doacoes:
            self.__repository.registrar_item_ciclo_acao_agape(
                ciclo_acao_agape.id, doacao
            )

        # Persiste alterações
        self.__repository.salvar_alteracoes()
