from http import HTTPStatus

from models.schemas.default import DefaultURLResponse
from repositories.agape_repository import AgapeRepository
from utils.functions import convert_data_into_xlsx


class ExportAgapeFamilies:
    def __init__(self, repository: AgapeRepository) -> None:
        self.__repository = repository

    def execute(self):
        familias = self.__repository.export_agape_families()

        headers = [
            "Nome Família",
            "Data de Cadastro Família",
            "Nome Membro",
            "Responsável",
            "Telefone",
            "Email",
            "CPF",
            "Data de Nascimento",
            "Ocupação",
            "Renda",
            "Data de Cadastro Membro",
            "Rua",
            "Número",
            "Complemento",
            "Bairro",
            "Ponto de Referência",
            "Cidade",
            "Estado",
            "CEP",
        ]

        url = convert_data_into_xlsx(
            data=familias,
            headers=headers,
            filename="familias_agape",
        )
        response = self.__prepare_response(url)

        return response, HTTPStatus.OK

    def __prepare_response(self, url: str) -> dict:
        response = DefaultURLResponse(url=url).dict()

        return response
