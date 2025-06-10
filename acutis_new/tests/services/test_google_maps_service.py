from unittest.mock import MagicMock, patch

import pytest

from acutis_api.domain.services.google_maps_service import (
    GoogleMapsAPI,
    GoogleMapsGeocode,
)
from acutis_api.exception.errors.not_found import HttpNotFoundError


def test_get_geolocation_em_teste_ou_dev(monkeypatch):
    monkeypatch.setattr(
        'acutis_api.domain.services.google_maps_service.settings.ENVIRONMENT',
        'teste',  # noqa
    )

    service = GoogleMapsAPI()
    resultado = service.get_geolocation('Rua Exemplo, 123, São Paulo, SP')

    assert isinstance(resultado, GoogleMapsGeocode)
    assert resultado.latitude == 0
    assert resultado.longitude == 0


@patch('googlemaps.Client')
def test_get_geolocation_sucesso(mock_gmaps_client, monkeypatch):
    monkeypatch.setattr(
        'acutis_api.domain.services.google_maps_service.settings.ENVIRONMENT',
        'production',  # noqa
    )
    monkeypatch.setattr(
        'acutis_api.domain.services.google_maps_service.settings.GOOGLE_MAPS_API_KEY',
        'fake-key',  # noqa
    )

    # Simula retorno da API do Google Maps
    mock_geocode_result = [
        {
            'geometry': {
                'location': {'lat': -23.5, 'lng': -46.6},
                'viewport': {
                    'northeast': {'lat': -23.4, 'lng': -46.5},
                    'southwest': {'lat': -23.6, 'lng': -46.7},
                },
            }
        }
    ]
    mock_client_instance = MagicMock()
    mock_client_instance.geocode.return_value = mock_geocode_result
    mock_gmaps_client.return_value = mock_client_instance

    service = GoogleMapsAPI()
    resultado = service.get_geolocation('Rua Exemplo, 123, São Paulo, SP')

    assert resultado.latitude == -23.5
    assert resultado.longitude == -46.6
    assert resultado.latitude_ne == -23.4
    assert resultado.longitude_ne == -46.5
    assert resultado.latitude_so == -23.6
    assert resultado.longitude_so == -46.7


@patch('googlemaps.Client')
def test_get_geolocation_endereco_nao_encontrado(
    mock_gmaps_client, monkeypatch
):
    monkeypatch.setattr(
        'acutis_api.domain.services.google_maps_service.settings.ENVIRONMENT',
        'production',  # noqa
    )
    monkeypatch.setattr(
        'acutis_api.domain.services.google_maps_service.settings.GOOGLE_MAPS_API_KEY',
        'fake-key',  # noqa
    )

    mock_client_instance = MagicMock()
    mock_client_instance.geocode.return_value = []
    mock_gmaps_client.return_value = mock_client_instance

    service = GoogleMapsAPI()

    with pytest.raises(HttpNotFoundError):
        service.get_geolocation('Rua Exemplo, 123, São Paulo, SP')
