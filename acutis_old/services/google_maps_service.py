import googlemaps
from pydantic import BaseModel

from config import ENVIRONMENT, GOOGLE_MAPS_API_KEY
from exceptions.error_types.http_not_found import NotFoundError


class GoogleMapsGeocode(BaseModel):
    latitude: float
    longitude: float
    latitude_nordeste: float
    longitude_nordeste: float
    latitude_sudoeste: float
    longitude_sudoeste: float


class GoogleMapsAPI:
    def __init__(self) -> None:
        self.__gmaps = googlemaps.Client(key=GOOGLE_MAPS_API_KEY)

    def get_geolocation(self, endereco: str) -> GoogleMapsGeocode:
        if ENVIRONMENT != "production":
            return GoogleMapsGeocode(
                latitude=0,
                longitude=0,
                latitude_nordeste=0,
                longitude_nordeste=0,
                latitude_sudoeste=0,
                longitude_sudoeste=0,
            )

        geocode_result = self.__gmaps.geocode(endereco)

        if not geocode_result:
            raise NotFoundError("O endereço informado não foi encontrado.")

        geometry = geocode_result[0]["geometry"]
        location = geometry["location"]
        bounds_or_viewport = geometry.get("bounds", geometry["viewport"])

        return GoogleMapsGeocode(
            latitude=location["lat"],
            longitude=location["lng"],
            latitude_nordeste=bounds_or_viewport["northeast"]["lat"],
            longitude_nordeste=bounds_or_viewport["northeast"]["lng"],
            latitude_sudoeste=bounds_or_viewport["southwest"]["lat"],
            longitude_sudoeste=bounds_or_viewport["southwest"]["lng"],
        )
