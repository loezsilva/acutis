import googlemaps
from pydantic import BaseModel

from acutis_api.exception.errors.not_found import HttpNotFoundError
from acutis_api.infrastructure.settings import settings


class GoogleMapsGeocode(BaseModel):
    latitude: float
    longitude: float
    latitude_ne: float
    longitude_ne: float
    latitude_so: float
    longitude_so: float


class GoogleMapsAPI:
    def __init__(self) -> None:
        if settings.ENVIRONMENT not in set(['teste', 'development']):
            self.__gmaps = googlemaps.Client(key=settings.GOOGLE_MAPS_API_KEY)

    def get_geolocation(self, endereco: str) -> GoogleMapsGeocode:
        if settings.ENVIRONMENT in set(['teste', 'development']):
            return GoogleMapsGeocode(
                latitude=0,
                longitude=0,
                latitude_ne=0,
                longitude_ne=0,
                latitude_so=0,
                longitude_so=0,
            )

        geocode_result = self.__gmaps.geocode(endereco)

        if not geocode_result:
            raise HttpNotFoundError('O endereço informado não foi encontrado.')

        geometry = geocode_result[0]['geometry']
        location = geometry['location']
        bounds_or_viewport = geometry.get('bounds', geometry['viewport'])

        return GoogleMapsGeocode(
            latitude=location['lat'],
            longitude=location['lng'],
            latitude_ne=bounds_or_viewport['northeast']['lat'],
            longitude_ne=bounds_or_viewport['northeast']['lng'],
            latitude_so=bounds_or_viewport['southwest']['lat'],
            longitude_so=bounds_or_viewport['southwest']['lng'],
        )
