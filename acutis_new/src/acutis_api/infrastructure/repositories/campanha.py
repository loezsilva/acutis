import uuid

from flask_jwt_extended import current_user
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func, select

from acutis_api.domain.entities.campanha import Campanha
from acutis_api.domain.entities.campo_adicional import CampoAdicional
from acutis_api.domain.entities.landing_page import LandingPage
from acutis_api.domain.repositories.campanha import (
    CampanhaRepositoryInterface,
    ListarCampanhasQuery,
    RegistrarCampanhaSchema,
)


class CampanhaRepository(CampanhaRepositoryInterface):
    def __init__(self, database: SQLAlchemy):
        self.__database = database

    def atualizar_landing_page(self, landing_page, dados_da_landing_page):
        landing_page.conteudo = dados_da_landing_page.conteudo
        landing_page.shlink = dados_da_landing_page.shlink
        landing_page.atualiado_em = func.now()
        self.__database.session.flush()

    def atualizar_campos_adicionais(
        self, campo_existente, campos_adicionais_atualizado
    ):
        campo_existente.obrigatorio = campos_adicionais_atualizado.obrigatorio
        campo_existente.atualizado_em = func.now()
        self.__database.session.flush()

    def buscar_campos_adicionais(self, fk_campanha_id: int):
        return (
            self.__database.session.query(CampoAdicional)
            .filter(CampoAdicional.fk_campanha_id == fk_campanha_id)
            .all()
        )

    def atualizar_campanha(
        self,
        campanha_para_atualizar: Campanha,
        dados_da_campanha: RegistrarCampanhaSchema,
    ) -> None:
        campanha_para_atualizar.nome = dados_da_campanha.nome
        campanha_para_atualizar.publica = dados_da_campanha.publica
        campanha_para_atualizar.ativa = dados_da_campanha.ativa
        campanha_para_atualizar.chave_pix = dados_da_campanha.chave_pix
        campanha_para_atualizar.fk_cargo_oficial_id = (
            dados_da_campanha.fk_cargo_oficial_id
        )
        campanha_para_atualizar.superior_obrigatorio = (
            dados_da_campanha.superior_obrigatorio
        )
        campanha_para_atualizar.atualizado_em = func.now()

        if dados_da_campanha.foto_capa is not None:
            campanha_para_atualizar.capa = dados_da_campanha.foto_capa

        self.__database.session.flush()

        return campanha_para_atualizar

    def buscar_campanha_por_id(self, fk_campanha_id: uuid.UUID) -> Campanha:
        return (
            self.__database.session.query(Campanha, LandingPage)
            .outerjoin(LandingPage, LandingPage.fk_campanha_id == Campanha.id)
            .order_by(self.__database.desc(Campanha.criado_em))
            .filter(Campanha.id == fk_campanha_id)
            .first()
        )

    def criar_landing_page(
        self, fk_campanha_id: uuid.UUID, dados_da_landing_page
    ):
        nova_landing_page = LandingPage(
            fk_campanha_id=fk_campanha_id,
            conteudo=dados_da_landing_page.conteudo,
            shlink=dados_da_landing_page.shlink,
        )

        self.__database.session.add(nova_landing_page)

    def criar_campos_adicionais(
        self, fk_campanha_id: uuid.UUID, campos_adicionais
    ):
        for campo in campos_adicionais:
            criar_campos_adicionais = CampoAdicional(
                fk_campanha_id=fk_campanha_id,
                nome_campo=campo.nome_campo,
                tipo_campo=campo.tipo_campo,
                obrigatorio=campo.obrigatorio,
            )

            self.__database.session.add(criar_campos_adicionais)

    def registrar_nova_campanha(
        self,
        dados_da_campanha: RegistrarCampanhaSchema,
    ) -> Campanha:
        nova_campanha = Campanha(
            nome=dados_da_campanha.nome,
            objetivo=dados_da_campanha.objetivo,
            publica=dados_da_campanha.publica,
            ativa=dados_da_campanha.ativa,
            meta=dados_da_campanha.meta,
            chave_pix=dados_da_campanha.chave_pix,
            criado_por=current_user.membro.id,
            capa=dados_da_campanha.foto_capa,
            fk_cargo_oficial_id=dados_da_campanha.fk_cargo_oficial_id,
            superior_obrigatorio=dados_da_campanha.superior_obrigatorio,
        )

        self.__database.session.add(nova_campanha)

        return nova_campanha

    def verificar_nome_da_campanha(self, nome_campanha: str) -> tuple:
        return (
            self.__database.session.query(Campanha)
            .filter(Campanha.nome == nome_campanha.strip())
            .first()
        )

    def salvar_alteracoes(self):
        try:
            self.__database.session.commit()
        except Exception as exc:
            self.__database.session.rollback()
            raise exc

    def listar_campanhas(
        self, filtros_da_requisicao: ListarCampanhasQuery
    ) -> dict:
        MAP_ORDER_BY = {
            'desc': self.__database.desc(Campanha.criado_em),
            'asc': self.__database.asc(Campanha.criado_em),
        }

        filtros = [
            (
                Campanha.id == filtros_da_requisicao.id
                if filtros_da_requisicao.id
                else True
            ),
            (
                Campanha.nome.ilike(f'%{filtros_da_requisicao.nome}%')
                if filtros_da_requisicao.nome
                else True
            ),
            (
                Campanha.objetivo == filtros_da_requisicao.objetivo
                if filtros_da_requisicao.objetivo
                else True
            ),
            (
                Campanha.publica == filtros_da_requisicao.publica
                if filtros_da_requisicao.publica is not None
                else True
            ),
            (
                Campanha.ativa == filtros_da_requisicao.ativa
                if filtros_da_requisicao.ativa is not None
                else True
            ),
            (
                self.__database.cast(
                    Campanha.criado_em, self.__database.Date
                ).between(
                    filtros_da_requisicao.data_inicial,
                    filtros_da_requisicao.data_final,
                )
                if filtros_da_requisicao.data_inicial is not None
                and filtros_da_requisicao.data_final is not None
                else True
            ),
        ]

        consulta_campanhas = (
            self.__database.session.query(Campanha)
            .outerjoin(LandingPage, LandingPage.fk_campanha_id == Campanha.id)
            .filter(*filtros)
            .order_by(MAP_ORDER_BY[filtros_da_requisicao.ordenar_por])
        )

        return consulta_campanhas.paginate(
            page=filtros_da_requisicao.pagina,
            per_page=filtros_da_requisicao.por_pagina,
            error_out=False,
        )

    def buscar_campanha_por_nome(self, nome_campanha: str) -> Campanha:
        return self.__database.session.scalar(
            self.__database.select(Campanha).filter(
                Campanha.nome == nome_campanha
            )
        )

    def lista_de_campanhas(self) -> Campanha:
        return self.__database.session.scalars(
            select(Campanha).order_by(Campanha.nome)
        ).all()
