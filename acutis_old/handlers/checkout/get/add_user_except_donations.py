from models import Clifor, Pedido, ListExceptionDonations
from builder import db
from exceptions.error_types.http_not_found import NotFoundError
from exceptions.error_types.http_conflict import ConflictError
from flask_jwt_extended import current_user
from utils.functions import get_current_time
from utils.logs_access import log_access
from flask import request


class AddUserExceptDonations:
    def __init__(self) -> None:
        self.__data = request.json
        self.__cpf_cnpj = self.__data.get("cpf_cnpj")
        self.__acao = self.__data.get("acao")

    def execute(self):
        clifor = self.__get_clifor()
        pedidos = self.__get_clifor_pedidos(clifor.id)
        list_except = self.__get_in_listexceptions()
        self.__pedidos_descontabler(
            pedidos=pedidos, clifor=clifor, list_except=list_except
        )

        res = {"msg": "Ação realizada com sucesso."}

        log_access(
            str(res),
            current_user["id"],
            current_user["nome"],
            current_user["fk_perfil_id"],
            200,
        )
        return res, 200

    def __get_in_listexceptions(self):
        doc_list = (
            db.session.query(ListExceptionDonations)
            .filter(ListExceptionDonations.cpf_cnpj == self.__cpf_cnpj)
            .first()
        )

        if doc_list is not None and self.__acao == 1:
            raise ConflictError("CNPJ ou CPF já adicionado a lista")

        if doc_list is None and self.__acao == 2:
            raise ConflictError("Documento não está na lista de exceções")

        return doc_list

    def __get_clifor(self) -> tuple:
        clifor = (
            db.session.query(Clifor)
            .filter(
                Clifor.cpf_cnpj == self.__cpf_cnpj,
            )
            .first()
        )

        if clifor is None:
            raise NotFoundError("Clifor não encontrado")

        return clifor

    def __get_clifor_pedidos(self, fk_clifor_id) -> tuple:
        pedidos = (
            db.session.query(Pedido)
            .filter(Pedido.fk_clifor_id == fk_clifor_id)
            .all()
        )

        if pedidos is None:
            raise NotFoundError("Nenhum pedido encontrado")

        return pedidos

    def __pedidos_descontabler(
        self, pedidos: tuple, clifor: tuple, list_except: tuple | None
    ) -> None:

        if self.__acao == 1:

            for pedido in pedidos:
                pedido.contabilizar_doacao = False

            add_list_exception_donations = ListExceptionDonations(
                fk_clifor_id=clifor.id,
                fk_usuario_id=clifor.fk_usuario_id,
                nome=clifor.nome,
                cpf_cnpj=clifor.cpf_cnpj,
                data_inclusao=get_current_time(),
                incluido_por=current_user["id"],
            )

            db.session.add(add_list_exception_donations)

            db.session.commit()

        if self.__acao == 2:
            for pedido in pedidos:
                pedido.contabilizar_doacao = True

            db.session.delete(list_except)

            db.session.commit()
