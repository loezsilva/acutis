from flask_sqlalchemy import SQLAlchemy
from exceptions.error_types.http_not_found import NotFoundError
from models.clifor import Clifor
from models.endereco import AtualizarEnderecoPorUserIdResponse, Endereco
from models.schemas.endereco.atualizar_endereco_por_telefone import (
    AtualizarEnderecoPorTelefoneRequest,
)
from utils.regex import format_string


class AtualizarEnderecoViaTelefoneUseCase:
    def __init__(self, database: SQLAlchemy):
        self.__database = database

    def execute(
        self, requisicao: AtualizarEnderecoPorTelefoneRequest
    ) -> dict[AtualizarEnderecoPorUserIdResponse]:
        
        telefone_formatado = format_string(
            requisicao.telefone.strip(), only_digits=True
        )
        
        clifor = self.__busca_usuario(telefone_formatado)
        endereco_do_usuario = self.__busca_endereco_do_membro(clifor.id)
        return self.__atualizar_endereco(endereco_do_usuario, requisicao)

    def __busca_endereco_do_membro(self, fk_clifor_id):
        endereco = (
            self.__database.session.query(Endereco)
            .filter(Endereco.fk_clifor_id == fk_clifor_id)
            .first()
        )

        if endereco is None:
            raise NotFoundError("Endereço não encontrado")

        return endereco

    def __busca_usuario(self, telefone):
        clifor = (
            self.__database.session.query(Clifor)
            .filter(Clifor.telefone1 == telefone)
            .first()
        )

        if clifor is None:
            raise NotFoundError("Usuário não encontrado")

        return clifor

    def __atualizar_endereco(
        self, endereco: Endereco, requisicao: AtualizarEnderecoPorTelefoneRequest
    ):
        campos = [
            ("rua", requisicao.rua),
            ("numero", requisicao.numero),
            ("complemento", requisicao.complemento),
            ("bairro", requisicao.bairro),
            ("cidade", requisicao.cidade),
            ("cep", requisicao.cep),
            ("estado", requisicao.estado),
            ("detalhe_estrangeiro", requisicao.detalhe_estrangeiro)
        ]

        for campo, valor in campos:
            if valor is not None:
                setattr(endereco, campo, valor)

        self.__database.session.commit()

        return {"msg": "Endereço atualizado com sucesso"}
