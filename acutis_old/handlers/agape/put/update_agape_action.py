from http import HTTPStatus
from typing import List
from flask_sqlalchemy import SQLAlchemy
from flask import request as flask_request

from exceptions.error_types.http_not_found import NotFoundError
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
    StatusAcaoAgapeEnum,
)
from models.agape.item_instancia_agape import ItemInstanciaAgape
from models.endereco import Endereco
from models.schemas.agape.put.update_agape_action import (
    DonationSchema,
    UpdateAgapeActionRequest,
)
from services.google_maps_service import GoogleMapsAPI
from utils.regex import format_string


class UpdateAgapeAction:
    def __init__(self, database: SQLAlchemy, gmaps: GoogleMapsAPI) -> None:
        self.__database = database
        self.__gmaps = gmaps

    def execute(self, fk_instancia_acao_agape_id: int):
        request = UpdateAgapeActionRequest.parse_obj(flask_request.json)
        request.endereco.cep = format_string(
            request.endereco.cep, only_digits=True
        )
        try:
            instancia_acao_agape = self.__get_agape_action_instance_data(
                fk_instancia_acao_agape_id
            )
            self.__update_agape_action_instance(
                instancia_acao_agape, request.abrangencia
            )
            self.__update_agape_action_address(
                request.endereco, instancia_acao_agape, request.abrangencia
            )
            self.__delete_agape_action_items(instancia_acao_agape.id)
            self.__update_agape_action_items(
                request.doacoes, instancia_acao_agape.id
            )
        except Exception as exception:
            self.__database.session.rollback()
            raise exception

        return {"msg": "Ciclo da ação atualizado com sucesso."}, HTTPStatus.OK

    def __get_agape_action_instance_data(
        self, fk_instancia_acao_agape_id: int
    ) -> InstanciaAcaoAgape:
        instancia_acao_agape: InstanciaAcaoAgape = self.__database.session.get(
            InstanciaAcaoAgape, fk_instancia_acao_agape_id
        )

        if instancia_acao_agape is None:
            raise NotFoundError("Ciclo da ação não encontrado.")

        if instancia_acao_agape.status != StatusAcaoAgapeEnum.nao_iniciado:
            raise HttpUnprocessableEntity(
                "Somentes ciclos nao iniciados podem ser atualizados."
            )

        return instancia_acao_agape

    def __update_agape_action_instance(
        self, instancia_acao_agape: InstanciaAcaoAgape, abrangencia: str
    ) -> None:
        instancia_acao_agape.abrangencia = abrangencia

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
            "rua": f"{endereco.rua}, {endereco.bairro}, {endereco.cidade}, {endereco.estado}, {pais}",
        }

        return mappings[abrangencia]

    def __update_agape_action_address(
        self,
        endereco: Endereco,
        instancia_acao_agape: InstanciaAcaoAgape,
        abrangencia: AbrangenciaInstanciaAcaoAgapeEnum,
    ) -> None:
        db_endereco: Endereco = self.__database.session.get(
            Endereco, instancia_acao_agape.fk_endereco_id
        )

        str_endereco = self.__generate_address_string(endereco, abrangencia)
        geolocalidade = self.__gmaps.get_geolocation(str_endereco)

        db_endereco.cep = endereco.cep
        db_endereco.rua = endereco.rua
        db_endereco.bairro = endereco.bairro
        db_endereco.cidade = endereco.cidade
        db_endereco.estado = endereco.estado
        db_endereco.numero = endereco.numero
        db_endereco.complemento = endereco.complemento
        db_endereco.latitude = geolocalidade.latitude
        db_endereco.longitude = geolocalidade.longitude
        db_endereco.latitude_nordeste = geolocalidade.latitude_nordeste
        db_endereco.longitude_nordeste = geolocalidade.longitude_nordeste
        db_endereco.latitude_sudoeste = geolocalidade.latitude_sudoeste
        db_endereco.longitude_sudoeste = geolocalidade.longitude_sudoeste

    def __delete_agape_action_items(
        self, fk_instancia_acao_agape_id: int
    ) -> None:
        itens: List[ItemInstanciaAgape] = ItemInstanciaAgape.query.filter_by(
            fk_instancia_acao_agape_id=fk_instancia_acao_agape_id
        ).all()

        for item in itens:
            estoque = self.__database.session.get(
                EstoqueAgape, item.fk_estoque_agape_id
            )
            estoque.quantidade += item.quantidade
            historico_movimentacao_agape = HistoricoMovimentacaoAgape(
                fk_estoque_agape_id=estoque.id,
                quantidade=item.quantidade,
                tipo_movimentacao=TipoMovimentacaoEnum.entrada,
            )
            self.__database.session.add(historico_movimentacao_agape)
            self.__database.session.delete(item)
        self.__database.session.flush()

    def __update_agape_action_items(
        self,
        doacoes: List[DonationSchema],
        fk_instancia_acao_agape_id: int,
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
                fk_instancia_acao_agape_id=fk_instancia_acao_agape_id,
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
