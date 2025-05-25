from flask_sqlalchemy import SQLAlchemy
from models.clifor import Clifor


class BuscaIdUsuarioPorValor:
    """
        Classe busca id de usuário por cpf, telefone ou email; 
        Algumas validações não foram aplicadas mediante a necessidades específicas.
    """
    def __init__(self, database: SQLAlchemy):
        self.__database = database

    def execute(self, valor_busca):

        busca_por_telefone: Clifor = self.__busca_por_telefone(valor_busca)

        if (
            busca_por_telefone is not None
            and busca_por_telefone.fk_usuario_id is not None
        ):
            return {"usuario_id": busca_por_telefone.fk_usuario_id}

        busca_por_email: Clifor = self.__busca_por_email(valor_busca)

        if busca_por_email is not None and busca_por_email.fk_usuario_id is not None:
            return {"usuario_id": busca_por_email.fk_usuario_id}

        busca_por_documento: Clifor = self.__busca_por_documento(valor_busca)

        if (
            busca_por_documento is not None
            and busca_por_documento.fk_usuario_id is not None
        ):
            return {"usuario_id": busca_por_documento.fk_usuario_id}

        return {}, 204

    def __busca_por_telefone(self, telefone):

        return (
            self.__database.session.query(Clifor)
            .filter(Clifor.telefone1 == telefone.strip())
            .first()
        )

    def __busca_por_email(self, email):
        
        # is_valid_email(email)
        
        return (
            self.__database.session.query(Clifor)
            .filter(Clifor.email == email.strip()).first()
        )

    def __busca_por_documento(self, cpf_cnpj):

        # cpf_cnpj = format_string(valor_documento, only_digits=True)
        # match len(valor_documento):
        #     case 11:
        #         tipo_documento = "cpf"
        #     case 14:
        #         tipo_documento = "cnpj"
        #     case _:
        #         raise BadRequestError("Documento inválido.")

        # cpf_cnpj = cpf_cnpj_validator(cpf_cnpj, tipo_documento)

        return (
            self.__database.session.query(Clifor)
            .filter(Clifor.cpf_cnpj == cpf_cnpj.strip())
            .first()
        )
