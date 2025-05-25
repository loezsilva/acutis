from http import HTTPStatus
from typing import Dict
from exceptions.error_types.http_not_found import NotFoundError
from models.agape.familia_agape import FamiliaAgape
from models.agape.foto_familia_agape import FotoFamiliaAgape
from models.endereco import Endereco
from models.schemas.agape.get.get_agape_family_by_cpf import (
    AgapeFamilyAddressSchema,
    AgapeFamilySchema,
    GetAgapeFamilyByCpfResponse,
)
from repositories.interfaces.agape_repository_interface import (
    AgapeRepositoryInterface,
)
from services.file_service import FileService
from utils.validator import cpf_cnpj_validator


class GetAgapeFamilyByCpf:
    def __init__(
        self, repository: AgapeRepositoryInterface, file_service: FileService
    ) -> None:
        self.__repository = repository
        self.__file_service = file_service

    def execute(self, cpf: str, fk_instancia_acao_agape_id: int):
        cpf = cpf_cnpj_validator(cpf, "cpf")
        familia = self.__get_agape_family(cpf, fk_instancia_acao_agape_id)
        endereco = self.__get_agape_family_address(familia.fk_endereco_id)
        fotos_familia = self.__repository.buscar_fotos_por_familia_agape_id(
            familia.id
        )
        response = self.__prepare_response(familia, endereco, fotos_familia)

        return response, HTTPStatus.OK

    def __get_agape_family(
        self, cpf: str, fk_instancia_acao_agape_id: int
    ) -> FamiliaAgape:
        familia = self.__repository.get_agape_family_by_cpf(
            cpf, fk_instancia_acao_agape_id
        )
        if familia is None:
            raise NotFoundError("Família não encontrada pelo CPF informado.")
        return familia

    def __get_agape_family_address(self, endereco_id: int) -> Endereco:
        endereco = self.__repository.get_agape_family_address_by_id(
            endereco_id
        )
        return endereco

    def __prepare_response(
        self, 
        familia: AgapeFamilySchema, 
        endereco: AgapeFamilyAddressSchema,
        fotos_familia: list[FotoFamiliaAgape],
    ) -> Dict:
        response = GetAgapeFamilyByCpfResponse(
            familia=AgapeFamilySchema(
                id=familia.id,
                nome_familia=familia.nome_familia,
                observacao=familia.observacao,
                comprovante_residencia=(
                    self.__file_service.get_public_url(
                        familia.comprovante_residencia
                    )
                    if familia.comprovante_residencia
                    else None
                ),
                cadastrado_em=familia.cadastrado_em,
                status=familia.status,
                ultimo_recebimento=familia.ultimo_recebimento,
            ).dict(),
            endereco=AgapeFamilyAddressSchema.from_orm(endereco).dict(),
            fotos_familia=[
                self.__file_service.get_public_url(db_familia.foto)
                for db_familia in fotos_familia
            ],
        ).dict()
        return response
