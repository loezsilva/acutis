from http import HTTPStatus
from models.schemas.default import DefaultURLResponse
from repositories.agape_repository import AgapeRepository
from utils.functions import convert_data_into_xlsx


class ExportAgapeDonations:
    def __init__(self, repository: AgapeRepository) -> None:
        self.__repository = repository

    def execute(self, fk_instancia_acao_agape_id: int):
        doacoes = self.__repository.export_agape_donations(
            fk_instancia_acao_agape_id
        )
        headers = [
            "Nome da Ação",
            "Família Beneficiada",
            "Item Doado",
            "Quantidade Doada",
            "Data da Doação",
        ]
        url = convert_data_into_xlsx(
            data=doacoes,
            headers=headers,
            filename="doacoes_agape",
        )

        response = self.__prepare_response(url)
        return response, HTTPStatus.OK

    def __prepare_response(self, url: str) -> dict:
        response = DefaultURLResponse(url=url).dict()

        return response
