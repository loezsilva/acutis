from http import HTTPStatus
from flask import request as flask_request
from flask_sqlalchemy import SQLAlchemy

from exceptions.error_types.http_not_found import NotFoundError
from models.agape.familia_agape import FamiliaAgape
from models.endereco import Endereco
from models.schemas.agape.put.update_agape_family_address import (
    UpdateAgapeFamilyAddressRequest,
)
from services.google_maps_service import GoogleMapsAPI


class UpdateAgapeFamilyAddress:
    def __init__(self, database: SQLAlchemy, gmaps: GoogleMapsAPI) -> None:
        self.__database = database
        self.__gmaps = gmaps

    def execute(self, fk_familia_agape_id: int):
        endereco = UpdateAgapeFamilyAddressRequest.parse_obj(
            flask_request.get_json()
        )
        try:
            db_endereco = self.__get_family_address_data(fk_familia_agape_id)
            self.__update_family_address(db_endereco, endereco)
        except Exception as exception:
            self.__database.session.rollback()
            raise exception

        return {"msg": "Endereço atualizado com sucesso."}, HTTPStatus.OK

    def __get_family_address_data(self, fk_familia_agape_id: int) -> Endereco:
        db_endereco: Endereco = (
            Endereco.query.join(
                FamiliaAgape, Endereco.id == FamiliaAgape.fk_endereco_id
            )
            .filter(FamiliaAgape.id == fk_familia_agape_id)
            .first()
        )
        if db_endereco is None:
            raise NotFoundError("Família não encontrada.")
        return db_endereco

    def __update_family_address(
        self, db_endereco: Endereco, endereco: Endereco
    ) -> None:
        str_endereco = f"{endereco.rua}, {endereco.numero}, {endereco.bairro}, {endereco.cidade}, {endereco.estado}, {endereco.cep}"
        geolocalidade = self.__gmaps.get_geolocation(str_endereco)

        db_endereco.cep = endereco.cep
        db_endereco.rua = endereco.rua
        db_endereco.numero = endereco.numero
        db_endereco.complemento = endereco.complemento
        db_endereco.ponto_referencia = endereco.ponto_referencia
        db_endereco.bairro = endereco.bairro
        db_endereco.cidade = endereco.cidade
        db_endereco.estado = endereco.estado
        db_endereco.latitude = geolocalidade.latitude
        db_endereco.longitude = geolocalidade.longitude
        db_endereco.latitude_nordeste = geolocalidade.latitude_nordeste
        db_endereco.longitude_nordeste = geolocalidade.longitude_nordeste
        db_endereco.latitude_sudoeste = geolocalidade.latitude_sudoeste
        db_endereco.longitude_sudoeste = geolocalidade.longitude_sudoeste

        self.__database.session.commit()
