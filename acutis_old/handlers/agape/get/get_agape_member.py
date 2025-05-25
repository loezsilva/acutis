from http import HTTPStatus
from typing import Dict

from exceptions.error_types.http_not_found import NotFoundError
from models.agape.membro_agape import MembroAgape
from models.schemas.agape.get.get_agape_member import GetAgapeMemberResponse
from repositories.interfaces.agape_repository_interface import (
    AgapeRepositoryInterface,
)
from services.file_service import FileService


class GetAgapeMember:
    def __init__(
        self, repository: AgapeRepositoryInterface, file_service: FileService,
    ) -> None:
        self.__repository = repository
        self.__file_service = file_service

    def execute(self, fk_membro_agape_id: int):
        membro = self.__get_member(fk_membro_agape_id)
        response = self.__prepare_response(membro)
        return response, HTTPStatus.OK

    def __get_member(self, fk_membro_agape_id: int) -> MembroAgape:
        membro = self.__repository.get_member_by_id(fk_membro_agape_id)
        if membro is None:
            raise NotFoundError("Membro não encontrado.")
        return membro

    def __prepare_response(self, membro: MembroAgape) -> Dict:
        response = GetAgapeMemberResponse(
            id=membro.id,
            nome=membro.nome,
            email=membro.email,
            telefone=membro.telefone,
            cpf=membro.cpf,
            data_nascimento=membro.data_nascimento,
            responsavel=membro.responsavel,
            funcao_familiar=membro.funcao_familiar,
            escolaridade=membro.escolaridade,
            ocupacao=membro.ocupacao,
            renda=membro.renda,
            foto_documento=self.__file_service.get_public_url(
                membro.foto_documento
            ) if membro.foto_documento else None,
            beneficiario_assistencial=membro.beneficiario_assistencial,
        ).dict()

        return response
