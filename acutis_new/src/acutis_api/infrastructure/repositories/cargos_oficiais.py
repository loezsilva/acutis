import uuid

from flask_jwt_extended import current_user
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import select

from acutis_api.domain.entities.cargo_oficial import CargosOficiais
from acutis_api.domain.entities.lead import Lead
from acutis_api.domain.entities.membro import Membro
from acutis_api.domain.entities.oficial import Oficial
from acutis_api.domain.repositories.cargos_oficiais import (
    CargosOficiaisRepositoryInterface,
)
from acutis_api.domain.repositories.schemas.cargos_oficiais import (
    ListarCargosOficiaisSchema,
)


class CargosOficiaisRepository(CargosOficiaisRepositoryInterface):
    def __init__(self, database: SQLAlchemy):
        self.__database = database

    def salvar_dados(self):
        self.__database.session.commit()

    def registrar_novo_cargo_vocacional(
        self, nome_cargo: str, fk_cargo_superior_id: uuid.UUID
    ) -> CargosOficiais:
        novo_cargo_oficial = CargosOficiais(
            nome_cargo=nome_cargo,
            criado_por=current_user.membro.id,
            atualizado_por=None,
            fk_cargo_superior_id=fk_cargo_superior_id,
        )

        self.__database.session.add(novo_cargo_oficial)

        return novo_cargo_oficial

    def busca_cargo_por_nome(self, nome_cargo: str) -> CargosOficiais:
        return self.__database.session.scalar(
            select(CargosOficiais).where(
                CargosOficiais.nome_cargo == nome_cargo
            )
        )

    def listar_todos_cargos_oficiais(
        self, filtros_da_requisicao: ListarCargosOficiaisSchema
    ) -> CargosOficiais:
        MAP_ORDER_BY = {
            'desc': self.__database.desc(CargosOficiais.criado_em),
            'asc': self.__database.asc(CargosOficiais.criado_em),
        }

        filtros = [
            (
                CargosOficiais.nome_cargo.ilike(
                    f'%{filtros_da_requisicao.nome_cargo}%'
                )
                if filtros_da_requisicao.nome_cargo is not None
                else True
            ),
            (
                CargosOficiais.id == filtros_da_requisicao.id
                if filtros_da_requisicao.id is not None
                else True
            ),
        ]

        consulta = (
            self.__database.session.query(
                Lead.nome,
                CargosOficiais.id,
                CargosOficiais.nome_cargo,
                CargosOficiais.criado_em,
                CargosOficiais.criado_por,
                CargosOficiais.fk_cargo_superior_id,
            )
            .join(Membro, Membro.id == CargosOficiais.criado_por)
            .join(Lead, Lead.id == Membro.fk_lead_id)
            .filter(*filtros)
            .order_by(MAP_ORDER_BY[filtros_da_requisicao.ordenar_por])
        )

        return consulta.paginate(
            page=filtros_da_requisicao.pagina,
            per_page=filtros_da_requisicao.por_pagina,
            error_out=False,
        )

    def busca_cargo_oficial_por_id(
        self, fk_cargo_oficial_id: uuid.UUID
    ) -> CargosOficiais:
        return self.__database.session.scalar(
            select(CargosOficiais).where(
                CargosOficiais.id == fk_cargo_oficial_id
            )
        )

    @staticmethod
    def atualizar_cargo_oficial(
        cargo_para_atualizar: CargosOficiais, dados_para_atualizar: dict
    ) -> CargosOficiais:
        cargo_para_atualizar.nome_cargo = dados_para_atualizar.nome_cargo
        cargo_para_atualizar.fk_cargo_superior_id = (
            dados_para_atualizar.fk_cargo_superior_id
        )
        cargo_para_atualizar.atualizado_por = current_user.membro.id

        return cargo_para_atualizar

    def buscar_oficiais_com_cargo_a_ser_deletado(
        self, fk_cargo_id: uuid.UUID
    ) -> None:
        (
            self.__database.session.query(Oficial)
            .filter(Oficial.fk_cargo_oficial_id == fk_cargo_id)
            .update(
                {Oficial.fk_cargo_oficial_id: None}, synchronize_session=False
            )
        )

    def admin_deleta_cargo_oficial(self, fk_cargo_id: uuid.UUID) -> None:
        cargo_para_deletar = (
            self.__database.session.query(CargosOficiais)
            .filter(CargosOficiais.id == fk_cargo_id)
            .first()
        )

        self.__database.session.delete(cargo_para_deletar)

    def lista_de_cargos_oficiais(self) -> CargosOficiais:
        return self.__database.session.scalars(
            select(CargosOficiais).order_by(CargosOficiais.nome_cargo)
        ).all()
