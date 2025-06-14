import logging  # For logging errors
import uuid
from http import HTTPStatus

from acutis_api.communication.requests.agape import (
    EditarEnderecoFamiliaAgapeRequest,
)
from acutis_api.communication.responses.padrao import ResponsePadraoSchema
from acutis_api.domain.entities.familia_agape import FamiliaAgape
from acutis_api.domain.repositories.agape import AgapeRepositoryInterface
from acutis_api.domain.repositories.schemas.agape import CoordenadasSchema
from acutis_api.domain.services.google_maps_service import (
    GoogleMapsAPI,
    GoogleMapsGeocode,
)
from acutis_api.exception.errors.not_found import HttpNotFoundError

logger = logging.getLogger(__name__)


class EditarEnderecoFamiliaAgapeUseCase:
    def __init__(
        self,
        repository: AgapeRepositoryInterface,
        gmaps_service: GoogleMapsAPI,
    ):
        self.__repository = repository
        self.__gmaps_service = gmaps_service

    def execute(
        self,
        familia_id: uuid.UUID,
        dados_endereco: EditarEnderecoFamiliaAgapeRequest,
    ) -> tuple[ResponsePadraoSchema, HTTPStatus]:
        familia: FamiliaAgape | None = self.__repository.buscar_familia_por_id(
            familia_id=familia_id
        )

        if familia is None:
            raise HttpNotFoundError('Familia não encontada.')
        endereco_familia = self.__repository.buscar_endereco_por_id(
            endereco_id=familia.fk_endereco_id
        )

        if familia is None:
            raise HttpNotFoundError(
                f'Família com ID {familia_id} não encontrada ou já deletada.'
            )

        str_endereco = f"""{dados_endereco.rua}, {dados_endereco.numero},
            {dados_endereco.bairro}, {dados_endereco.cidade},
            {dados_endereco.estado}, {dados_endereco.cep}
        """

        try:
            geolocalizacao_gmaps_obj: GoogleMapsGeocode = (
                self.__gmaps_service.get_geolocation(endereco=str_endereco)
            )

            self.__repository.atualizar_coordenadas(
                coordenada=endereco_familia.coordenada,
                dados_coordenada=CoordenadasSchema(
                    latitude=geolocalizacao_gmaps_obj.latitude,
                    longitude=geolocalizacao_gmaps_obj.longitude,
                    latitude_ne=geolocalizacao_gmaps_obj.latitude_ne,
                    longitude_ne=geolocalizacao_gmaps_obj.longitude_ne,
                    latitude_so=geolocalizacao_gmaps_obj.latitude_so,
                    longitude_so=geolocalizacao_gmaps_obj.longitude_so,
                ),
            )

        except HttpNotFoundError:
            raise HttpNotFoundError(
                'Endereço não pôde ser \
                geolocalizado ou é inválido.'
            )

        self.__repository.atualizar_endereco_familia(
            familia=familia,
            dados_endereco=dados_endereco,
        )

        self.__repository.salvar_alteracoes()
