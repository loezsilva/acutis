from abc import ABC, abstractmethod
from datetime import date
from http import HTTPStatus

from models.schemas.checkout.get.get_donors_ranking import GetDonorsRankingQueryFilter
from models.schemas.checkout.get.get_top_regular_donors import (
    GetTopRegularDonorsQueryFilter,
)
from models.schemas.checkout.get.listar_doacoes_schema import ListarDoacoesQuery


class CheckoutRepositoryInterface(ABC):

    @abstractmethod
    def get_top_regular_donors(
        filtros: GetTopRegularDonorsQueryFilter, mes_inicial: date, mes_final: date
    ):
        pass

    @abstractmethod
    def get_donors_ranking(
        filtros: GetDonorsRankingQueryFilter,
        mes_inicial: date,
        mes_final: date,
    ):
        pass

    @abstractmethod
    def get_listagem_de_doacoes(self, requests_args: ListarDoacoesQuery):
        pass

    @abstractmethod
    def get_informacoes_sobre_usuario(self, fk_usuario_id: int):
        pass

    @abstractmethod
    def get_listar_recorrencias_canceladas(
        self, filtros_request
    ) -> tuple[dict, HTTPStatus]:
        pass
    
    @abstractmethod
    def exportar_doacoes(
        self, filtros_request
    ) -> tuple[dict, HTTPStatus]:
        pass

    @abstractmethod
    def query_doacoes_inadimplentes(self, filtros: dict, objetivo: str = "listagem"):
        pass