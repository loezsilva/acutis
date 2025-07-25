import uuid

from flask_jwt_extended import current_user
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import aliased

from acutis_api.communication.enums import TipoOrdenacaoEnum
from acutis_api.communication.enums.admin_membros_oficiais import (
    ListarMembrosOficiaisOrdenarPorEnum,
)
from acutis_api.communication.requests.membros_oficiais import (
    RegistrarMembroOficialRequest,
)
from acutis_api.domain.entities.cargo_oficial import CargosOficiais
from acutis_api.domain.entities.endereco import Endereco
from acutis_api.domain.entities.lead import Lead
from acutis_api.domain.entities.membro import Membro
from acutis_api.domain.entities.oficial import Oficial
from acutis_api.domain.repositories.enums.membros_oficiais import (
    StatusMembroOficialEnum,
)
from acutis_api.domain.repositories.membros_oficiais import (
    MembrosOficiaisRepositoryInterface,
)
from acutis_api.domain.repositories.schemas.admin_membros_oficiais import (
    AlterarCargoOficialSchema,
    ListarMembrosOficiaisSchema,
)


class MembrosOficiaisRepository(MembrosOficiaisRepositoryInterface):
    def __init__(self, database: SQLAlchemy):
        self.__database = database

    def salvar_dados(self):
        self.__database.session.commit()

    def registrar_novo_membro_oficial(
        self, dados_da_requisicao: RegistrarMembroOficialRequest
    ):
        novo_membro_oficial = Oficial(
            fk_membro_id=dados_da_requisicao.fk_membro_id,
            fk_cargo_oficial_id=dados_da_requisicao.fk_cargo_oficial_id,
            fk_superior_id=dados_da_requisicao.fk_superior_id,
            status=StatusMembroOficialEnum.pendente,
            atualizado_por=None,
        )

        self.__database.session.add(novo_membro_oficial)
        return novo_membro_oficial

    def buscar_oficial_por_fk_membro_id(
        self, fk_membro_id: uuid.UUID
    ) -> Oficial:
        return (
            self.__database.session.query(Oficial)
            .filter(Oficial.fk_membro_id == fk_membro_id)
            .first()
        )

    def admin_listar_membros_oficiais(
        self, filtros_da_requisicao: ListarMembrosOficiaisSchema
    ) -> tuple:
        membro_oficial_alias = aliased(Membro)
        superior_alias = aliased(Membro)
        lead_superior_alias = aliased(Lead)

        ordenar_por_map = {
            ListarMembrosOficiaisOrdenarPorEnum.lead_nome: Lead.nome,
            ListarMembrosOficiaisOrdenarPorEnum.lead_email: Lead.email,
            ListarMembrosOficiaisOrdenarPorEnum.membro_documento: (
                membro_oficial_alias.numero_documento
            ),
            ListarMembrosOficiaisOrdenarPorEnum.membro_sexo: (
                membro_oficial_alias.sexo
            ),
            ListarMembrosOficiaisOrdenarPorEnum.oficial_status: Oficial.status,
            ListarMembrosOficiaisOrdenarPorEnum.cargo_oficial: (
                CargosOficiais.nome_cargo
            ),
            ListarMembrosOficiaisOrdenarPorEnum.superior_nome: (
                lead_superior_alias.nome
            ),
            ListarMembrosOficiaisOrdenarPorEnum.criado_em: Oficial.criado_em,
        }

        campo_sqlalchemy = ordenar_por_map[filtros_da_requisicao.ordenar_por]

        campo_ordenacao = (
            self.__database.asc(campo_sqlalchemy)
            if filtros_da_requisicao.tipo_ordenacao
            == (TipoOrdenacaoEnum.crescente)
            else self.__database.desc(campo_sqlalchemy)
        )

        filtros = {
            (
                Lead.nome.ilike(f'%{filtros_da_requisicao.nome}%')
                if filtros_da_requisicao.nome is not None
                else True
            ),
            (
                Lead.email.ilike(f'%{filtros_da_requisicao.email}%')
                if filtros_da_requisicao.email is not None
                else True
            ),
            (
                self.__database.cast(Oficial.criado_em, self.__database.Date)
                >= filtros_da_requisicao.data_inicial
                if filtros_da_requisicao.data_inicial
                else True
            ),
            (
                self.__database.cast(Oficial.criado_em, self.__database.Date)
                <= filtros_da_requisicao.data_final
                if filtros_da_requisicao.data_final
                else True
            ),
            (
                Oficial.fk_cargo_oficial_id
                == (filtros_da_requisicao.fk_cargo_oficial_id)
                if filtros_da_requisicao.fk_cargo_oficial_id is not None
                else True
            ),
            (
                Oficial.fk_superior_id == filtros_da_requisicao.fk_superior_id
                if filtros_da_requisicao.fk_superior_id is not None
                else True
            ),
            (
                Oficial.status == filtros_da_requisicao.numero_documento
                if filtros_da_requisicao.status is not None
                else True
            ),
            (
                membro_oficial_alias.numero_documento.ilike(
                    f'%{filtros_da_requisicao.numero_documento}%'
                )
                if filtros_da_requisicao.numero_documento is not None
                else True
            ),
        }

        if filtros_da_requisicao.filtro_dinamico:
            pesquisa = f'%{filtros_da_requisicao.filtro_dinamico}%'
            filtros.add(
                self.__database.or_(
                    Lead.nome.ilike(pesquisa),
                    Lead.email.ilike(pesquisa),
                    membro_oficial_alias.numero_documento.ilike(pesquisa),
                    membro_oficial_alias.sexo.ilike(pesquisa),
                    Oficial.status.ilike(pesquisa),
                    CargosOficiais.nome_cargo.ilike(pesquisa),
                    lead_superior_alias.nome.ilike(pesquisa),
                )
            )

        consulta = (
            self.__database.session.query(
                Lead,
                membro_oficial_alias,
                Endereco,
                Oficial,
                CargosOficiais.nome_cargo,
                lead_superior_alias.nome.label('nome_superior'),
            )
            .join(
                membro_oficial_alias,
                membro_oficial_alias.fk_lead_id == Lead.id,
            )
            .join(Endereco, Endereco.id == membro_oficial_alias.fk_endereco_id)
            .join(Oficial, Oficial.fk_membro_id == membro_oficial_alias.id)
            .outerjoin(
                CargosOficiais,
                CargosOficiais.id == Oficial.fk_cargo_oficial_id,
            )
            .outerjoin(
                superior_alias, superior_alias.id == Oficial.fk_superior_id
            )
            .outerjoin(
                lead_superior_alias,
                lead_superior_alias.id == superior_alias.fk_lead_id,
            )
            .filter(*filtros)
        )
        consulta = consulta.order_by(campo_ordenacao)

        return consulta.paginate(
            page=filtros_da_requisicao.pagina,
            per_page=filtros_da_requisicao.por_pagina,
            error_out=False,
        )

    def busca_nome_de_usuario_superior(
        self, fk_usuario_superior_id: uuid.UUID
    ) -> str:
        superior = (
            self.__database.session.query(Lead)
            .join(Membro, Membro.fk_lead_id == Lead.id)
            .where(Membro.id == fk_usuario_superior_id)
            .first()
        )

        return superior.nome

    def buscar_nome_cargo_oficial(self, fk_cargo_oficial_id) -> str:
        cargo_oficial = (
            self.__database.session.query(CargosOficiais)
            .where(CargosOficiais.id == fk_cargo_oficial_id)
            .first()
        )

        return cargo_oficial.nome_cargo

    def buscar_membro_oficial_por_id(
        self, fk__membro_oficial_id: uuid.UUID
    ) -> Oficial:
        return (
            self.__database.session.query(Oficial)
            .where(Oficial.id == fk__membro_oficial_id)
            .first()
        )

    @staticmethod
    def atualizar_status_membro_oficial(
        membro_oficial_para_atualizar: Oficial, status: StatusMembroOficialEnum
    ) -> Oficial:
        membro_oficial_para_atualizar.status = status
        membro_oficial_para_atualizar.atualizado_por = current_user.membro.id

        return membro_oficial_para_atualizar

    def busca_cargo_oficial_por_id(
        self, fk_cargo_oficial_id: uuid.UUID
    ) -> CargosOficiais:
        return (
            self.__database.session.query(CargosOficiais)
            .where(CargosOficiais.id == fk_cargo_oficial_id)
            .first()
        )

    @staticmethod
    def admin_alterar_cargo_oficial(
        membro_oficial: Oficial, requisicao: AlterarCargoOficialSchema
    ) -> Oficial:
        membro_oficial.fk_cargo_oficial_id = requisicao.fk_cargo_oficial_id
        membro_oficial.atualizado_por = current_user.membro.id

        return membro_oficial

    @staticmethod
    def admin_alterar_vinculo_oficial(
        membro_oficial: Oficial, membro_oficial_superior: Oficial
    ) -> Oficial:
        membro_oficial.fk_superior_id = membro_oficial_superior.fk_membro_id
        membro_oficial.atualizado_por = current_user.membro.id

        return membro_oficial

    def remover_vinculos_de_superior(
        self, fk_membro_oficial_id: uuid.UUID = None
    ) -> None:
        self.__database.session.query(Oficial).filter(
            Oficial.fk_superior_id == fk_membro_oficial_id
        ).update({Oficial.fk_superior_id: None}, synchronize_session=False)

    def admin_excluir_oficial(self, oficial_para_deletar: Oficial) -> None:
        self.__database.session.delete(oficial_para_deletar)

    def busca_membro_por_id(self, fk_membro_id: uuid.UUID) -> Membro:
        return (
            self.__database.session.query(Lead)
            .join(Membro, Lead.id == Membro.fk_lead_id)
            .filter(Membro.id == fk_membro_id)
            .first()
        )

    def busca_superiores_de_cargo_oficial(
        self, fk_cargo_superior_id: uuid.UUID
    ) -> Oficial:
        membros_superiores = (
            self.__database.session.query(
                Oficial.id,
                Lead.nome,
            )
            .join(Membro, Membro.id == Oficial.fk_membro_id)
            .join(Lead, Lead.id == Membro.fk_lead_id)
            .filter(Oficial.fk_cargo_oficial_id == (fk_cargo_superior_id))
            .all()
        )

        return membros_superiores

    def admin_listar_membro_oficial_por_id(
        self, membro_oficial_id: uuid.UUID
    ) -> tuple:
        membro_oficial_alias = aliased(Membro)
        membro_superior_alias = aliased(Membro)
        lead_superior_alias = aliased(Lead)

        return (
            self.__database.session.query(
                Lead,
                membro_oficial_alias,
                Endereco,
                Oficial,
                CargosOficiais.nome_cargo,
                lead_superior_alias.nome.label('nome_superior'),
            )
            .join(
                membro_oficial_alias,
                membro_oficial_alias.fk_lead_id == Lead.id,
            )
            .join(Oficial, Oficial.fk_membro_id == membro_oficial_alias.id)
            .join(Endereco, Endereco.id == membro_oficial_alias.fk_endereco_id)
            .outerjoin(
                membro_superior_alias,
                membro_superior_alias.id == (Oficial.fk_superior_id),
            )
            .outerjoin(
                lead_superior_alias,
                lead_superior_alias.id == membro_superior_alias.fk_lead_id,
            )
            .outerjoin(
                CargosOficiais,
                CargosOficiais.id == Oficial.fk_cargo_oficial_id,
            )
            .filter(Oficial.id == membro_oficial_id)
            .first()
        )
