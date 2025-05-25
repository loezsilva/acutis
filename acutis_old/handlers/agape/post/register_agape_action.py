from http import HTTPStatus
from typing import List
from flask import request as flask_request
from flask_sqlalchemy import SQLAlchemy

from exceptions.error_types.http_unprocessable_entity import (
    HttpUnprocessableEntity,
)
from models.agape.estoque_agape import EstoqueAgape
from models.agape.historico_movimentacao_agape import (
    HistoricoMovimentacaoAgape,
    TipoMovimentacaoEnum,
)
from models.agape.instancia_acao_agape import (
    AbrangenciaInstanciaAcaoAgapeEnum,
    InstanciaAcaoAgape,
)
from models.agape.item_instancia_agape import ItemInstanciaAgape
from models.endereco import Endereco
from models.schemas.agape.post.register_agape_action import (
    DonationSchema,
    RegisterAgapeActionRequest,
)
from services.google_maps_service import GoogleMapsAPI
from utils.regex import format_string


class RegisterAgapeAction:
    def __init__(self, database: SQLAlchemy, gmaps: GoogleMapsAPI) -> None:
        self.__database = database
        self.__gmaps = gmaps

    def execute(self):
        request = RegisterAgapeActionRequest.parse_obj(flask_request.json)
        request.endereco.cep = format_string(
            request.endereco.cep, only_digits=True
        )
        try:
            endereco = self.__register_agape_action_address(
                request.endereco, request.abrangencia
            )
            instancia_acao_agape = self.__register_agape_action_instance(
                endereco.id, request.fk_acao_agape_id, request.abrangencia
            )
            self.__register_item_agape_instance(
                request.doacoes, instancia_acao_agape.id
            )
        except Exception as exception:
            self.__database.session.rollback()
            raise exception

        return {
            "msg": "Ação ágape cadastrada com sucesso."
        }, HTTPStatus.CREATED

    def __generate_address_string(
        self,
        endereco: Endereco,
        abrangencia: AbrangenciaInstanciaAcaoAgapeEnum,
    ) -> str:
        pais = "Brasil"
        mappings = {
            "sem_restricao": pais,
            "cidade": f"{endereco.cidade}, {endereco.estado}, {pais}",
            "bairro": f"{endereco.bairro}, {endereco.cidade}, {endereco.estado}, {pais}",
            "estado": f"{endereco.estado}, {pais}",
            "cep": f"{endereco.cep}, {pais}",
            "rua": f"{endereco.rua}, {endereco.bairro}, {endereco.cidade}, {endereco.estado}, {endereco.cep}",
        }

        return mappings[abrangencia]

    def __register_agape_action_address(
        self,
        endereco: Endereco,
        abrangencia: AbrangenciaInstanciaAcaoAgapeEnum,
    ) -> Endereco:
        str_endereco = self.__generate_address_string(endereco, abrangencia)
        geolocalidade = self.__gmaps.get_geolocation(str_endereco)

        db_endereco = Endereco(
            cep=endereco.cep,
            rua=endereco.rua,
            bairro=endereco.bairro,
            cidade=endereco.cidade,
            estado=endereco.estado,
            numero=endereco.numero,
            complemento=endereco.complemento,
            latitude=geolocalidade.latitude,
            longitude=geolocalidade.longitude,
            latitude_nordeste=geolocalidade.latitude_nordeste,
            longitude_nordeste=geolocalidade.longitude_nordeste,
            latitude_sudoeste=geolocalidade.latitude_sudoeste,
            longitude_sudoeste=geolocalidade.longitude_sudoeste,
        )
        self.__database.session.add(db_endereco)
        self.__database.session.flush()

        return db_endereco

    def __register_agape_action_instance(
        self, endereco_id: int, acao_agape_id: int, abrangencia: str
    ) -> InstanciaAcaoAgape:
        instancia_acao_agape = InstanciaAcaoAgape(
            fk_endereco_id=endereco_id,
            fk_acao_agape_id=acao_agape_id,
            abrangencia=abrangencia,
        )
        self.__database.session.add(instancia_acao_agape)
        self.__database.session.flush()

        return instancia_acao_agape

    def __register_item_agape_instance(
        self, doacoes: List[DonationSchema], instancia_acao_agape_id: int
    ) -> None:
        for doacao in doacoes:
            estoque: EstoqueAgape = EstoqueAgape.query.filter_by(
                id=doacao.fk_estoque_agape_id
            ).first()
            if doacao.quantidade > estoque.quantidade:
                raise HttpUnprocessableEntity(
                    f"Quantidade insuficiente em estoque do item {estoque.item}."
                )
            estoque.quantidade -= doacao.quantidade

            item_instancia = ItemInstanciaAgape(
                fk_estoque_agape_id=estoque.id,
                fk_instancia_acao_agape_id=instancia_acao_agape_id,
                quantidade=doacao.quantidade,
            )
            self.__database.session.add(item_instancia)

            historico_movimentacao = HistoricoMovimentacaoAgape(
                fk_estoque_agape_id=estoque.id,
                quantidade=doacao.quantidade,
                tipo_movimentacao=TipoMovimentacaoEnum.saida,
            )
            self.__database.session.add(historico_movimentacao)
        self.__database.session.commit()
