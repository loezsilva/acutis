from http import HTTPStatus
from flask import request
from typing import Dict, List, Tuple

from models.agape.membro_agape import MembroAgape
from models.schemas.agape.get.get_all_members_by_family_id import (
    FamilyMemberSchema,
    GetAllMembersByFamilyIdResponse,
)
from repositories.interfaces.agape_repository_interface import (
    AgapeRepositoryInterface,
)
from utils.functions import calculate_age


class GetAllMembersByFamilyId:
    def __init__(self, agape_repository: AgapeRepositoryInterface) -> None:
        self.__agape_repository = agape_repository
        self.__page = request.args.get("page", 1, type=int)
        self.__per_page = request.args.get("per_page", 10, type=int)

    def execute(self, fk_familia_agape_id: int):
        membros, total = self.__get_members(fk_familia_agape_id)
        response = self.__prepare_response(membros, total)

        return response, HTTPStatus.OK

    def __get_members(
        self, fk_familia_agape_id: int
    ) -> Tuple[List[MembroAgape], int]:
        membros_query = self.__agape_repository.get_all_members(
            fk_familia_agape_id
        )
        membros, total = self.__agape_repository.paginate_query(
            membros_query, self.__page, self.__per_page
        )
        return membros, total

    def __prepare_response(
        self, membros: List[MembroAgape], total: int
    ) -> Dict:
        response = GetAllMembersByFamilyIdResponse(
            page=self.__page,
            total=total,
            membros=[
                FamilyMemberSchema(
                    id=membro.id,
                    nome=membro.nome,
                    telefone=membro.telefone,
                    email=membro.email,
                    cpf=membro.cpf,
                    idade=calculate_age(membro.data_nascimento),
                    ocupacao=membro.ocupacao,
                    renda=membro.renda,
                    responsavel=membro.responsavel,
                ).dict()
                for membro in membros
            ],
        ).dict()

        return response
