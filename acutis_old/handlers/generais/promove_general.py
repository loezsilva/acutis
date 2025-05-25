from flask import request
from flask_jwt_extended import current_user
from flask_sqlalchemy import SQLAlchemy
from exceptions.error_types.http_conflict import ConflictError
from exceptions.error_types.http_not_found import NotFoundError
from handlers.generais.desvincular_generais import DesvincularGenerais
from models import Generais
from typing import Dict
from builder import db
from models.clifor import Clifor
from models.usuario import Usuario
from services.send_data_to_app_acutis import SendDataToAppAcutis
from utils.functions import get_current_time


class AlterCargoGeneral:
    def __init__(self, fk_general_id: int, conn: SQLAlchemy) -> Dict:
        self.__fk_general_id = fk_general_id
        self.__http_request = request.json
        self.__acao = self.__http_request.get("acao")
        self.__fk_marechal_id = self.__http_request.get("marechal_id")
        self.__conn = conn
        self.__map_cargo = {1: "marechal", 2: "general"}

    def execute(self):
        general, usuario, clifor = self.__get_general()
        if self.__acao == "promover":
            return self.__promove_to_marechal(general, usuario, clifor)

        if self.__acao == "rebaixar":
            return self.__rebaixar_to_general(general)

        if self.__acao == "vincular":
            return self.__vincular_to_marechal(general, self.__fk_marechal_id)

    def __get_general(self) -> Dict:
        
        general = (self.__conn.session.query(Generais, Usuario, Clifor)
            .join(Usuario, Usuario.id == Generais.fk_usuario_id)
            .join(Clifor, Clifor.fk_usuario_id == Usuario.id)
            .filter(
                Generais.deleted_at.is_(None),
                Generais.id == self.__fk_general_id
            )
            .first()
        )
        if general is None:
            raise NotFoundError("General não encontrado")

        return general

    def __promove_to_marechal(self, general: Generais, usuario: Usuario, clifor: Clifor) -> tuple:    
          
        try: 
            if general.status != True:
                raise ConflictError("É necessário aprová-lo para promover.")

            if general.fk_cargo_id == 1:
                raise ConflictError("Esse cadastro já possui o cargo de marechal")

            general.updated_at = get_current_time()
            general.usuario_alteracao = current_user["id"]
            general.fk_cargo_id = 1
            general.fk_usuario_superior_id = None
            
            payload = {
                "email": usuario.email,
                "cpf": clifor.cpf_cnpj,
                "patent": self.__map_cargo[general.fk_cargo_id],
                "name": usuario.nome
            }
                    
            register_general_in_app_acutis = SendDataToAppAcutis(payload)
            register_general_in_app_acutis.execute()

            db.session.commit()
            return {"msg": "General promovido a marechal com sucesso!"}, 200
        except Exception as e:
            self.__conn.session.rollback()
            raise e

    def __rebaixar_to_general(self, general: dict) -> tuple:
        try:
            if general.fk_cargo_id == 2:
                raise ConflictError("Esse cadastro já possue o cargo de general")

            general.fk_cargo_id = 2
            general.updated_at = get_current_time()
            general.usuario_alteracao = current_user["id"]

            desvincular_generais = DesvincularGenerais(general.id, self.__conn)
            desvincular_generais.execute()

            db.session.commit()
            return {"msg": "Rabaixado a general com sucesso!"}, 200

        except Exception as e:
            raise e

    def __vincular_to_marechal(
        self, general: dict, fk_marechal_id: int
    ) -> tuple:
        try:
            marechal_exist = Generais.query.filter_by(
                id=fk_marechal_id, fk_cargo_id=1, deleted_at=None
            ).first()

            if general.status != True:
                raise ConflictError("É necessário aprová-lo para vincular.")

            if marechal_exist is None:
                raise NotFoundError("Marechal não encontrado!")

            if general.fk_cargo_id == 1:
                raise ConflictError(
                    "Não é possível vincular um marechal a outro marechal!"
                )

            if general.id == fk_marechal_id:
                raise ConflictError(
                    "Não é possível atribuir superior ao mesmo cadastro!"
                )

            if general.fk_usuario_superior_id == self.__fk_marechal_id:
                raise ConflictError("General já está vinculado a esse Marechal")

            general.updated_at = get_current_time()
            general.usuario_alteracao = current_user["id"]
            general.fk_usuario_superior_id = self.__fk_marechal_id

            db.session.commit()

            return {"msg": "General vinculado a Marechal com sucesso"}, 200
        except Exception as e:
            db.session.rollback()
            raise e