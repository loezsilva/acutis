from http import HTTPStatus

from acutis_api.application.utils.enderecos import generate_address_string
from acutis_api.communication.requests.agape import (
    RegistrarOuEditarCicloAcaoAgapeFormData,
)
from acutis_api.domain.repositories.agape import AgapeRepositoryInterface
from acutis_api.domain.repositories.schemas.agape import (
    RegistrarCicloAcaoAgapeScheme,
)
from acutis_api.domain.services.google_maps_service import GoogleMapsAPI
from acutis_api.exception.errors_handler import errors_handler


class RegistrarCicloAcaoAgapeUseCase:
    """
    Caso de uso para cadastrar um ciclo de ação Ágape completo:
    - Salva endereço com geolocalização
    - Cria instância de ciclo
    - Registra itens do ciclo e ajusta estoque
    """

    def __init__(
        self,
        agape_repository: AgapeRepositoryInterface,
        gmaps,
    ):
        self.__agape_repository = agape_repository
        self.__gmaps: GoogleMapsAPI = gmaps

    def execute(
        self, dados: RegistrarOuEditarCicloAcaoAgapeFormData
    ) -> tuple[dict, HTTPStatus]:
        try:
            nome_acao = self.__agape_repository.buscar_nome_acao_por_id(
                dados.nome_acao_id
            )

            abrangencia = dados.abrangencia
            dados_endereco = dados.endereco

            str_endereco = generate_address_string(dados_endereco, abrangencia)
            endereco = self.__agape_repository.registrar_endereco(
                dados_endereco
            )
            self.__agape_repository.registrar_coordenada(
                endereco.id, self.__gmaps.get_geolocation(str_endereco)
            )

            ciclo_acao_agape = (
                self.__agape_repository.registrar_ciclo_acao_agape(
                    RegistrarCicloAcaoAgapeScheme(
                        nome_acao_id=nome_acao.id,
                        abrangencia=abrangencia,
                        endereco_id=endereco.id,
                    )
                )
            )

            for doacao in dados.doacoes:
                self.__agape_repository.registrar_item_ciclo_acao_agape(
                    ciclo_acao_agape.id, doacao
                )

            self.__agape_repository.salvar_alteracoes()
            return (
                {'msg': 'Ciclo da ação Ágape cadastrado com sucesso.'},
                HTTPStatus.CREATED,
            )

        except Exception as e:
            return errors_handler(e)
