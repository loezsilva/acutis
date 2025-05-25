from typing import List

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_, func

from models.clifor import Clifor
from models.endereco import Endereco
from models.usuario import Usuario
from repositories.interfaces.admin_repository_interface import (
    AdminRepositoryInterface,
)


class AdminRepository(AdminRepositoryInterface):
    def __init__(self, database: SQLAlchemy) -> None:
        self.__database = database

    def get_all_regular_users(self) -> List[Usuario]:
        all_users_query = (
            self.__database.session.query(
                Usuario.country.label("pais"),
                Usuario.nome,
                Usuario.id,
                Usuario.nome_social,
                Clifor.cpf_cnpj.label("numero_documento"),
                Usuario.email,
                Clifor.telefone1.label("telefone"),
                func.format(Clifor.data_nascimento, "dd/MM/yyyy").label(
                    "data_nascimento"
                ),
                Clifor.sexo,
                Endereco.cep,
                Endereco.estado,
                Endereco.cidade,
                Endereco.bairro,
                Endereco.rua,
                Endereco.numero,
                Endereco.complemento,
            )
            .join(Clifor, Clifor.fk_usuario_id == Usuario.id)
            .join(Endereco, Clifor.id == Endereco.fk_clifor_id)
            .filter(
                Usuario.deleted_at.is_(None),
                and_(
                    Usuario.obriga_atualizar_cadastro == False,
                    Endereco.obriga_atualizar_endereco == False,
                    Usuario.status == True,
                ),
            )
            .order_by(Endereco.estado, Endereco.cidade)
        )

        all_users = all_users_query.all()

        return all_users

    def get_regular_users_quantity(self) -> int:
        qtd_users = (
            self.__database.session.query(Usuario)
            .join(Clifor, Usuario.id == Clifor.fk_usuario_id)
            .join(Endereco, Clifor.id == Endereco.fk_clifor_id)
            .filter(
                and_(
                    Usuario.status == True,
                    Usuario.deleted_at.is_(None),
                    Endereco.obriga_atualizar_endereco == False,
                    Usuario.obriga_atualizar_cadastro == False,
                )
            )
            .count()
        )

        return qtd_users
