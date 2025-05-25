from flask_sqlalchemy import SQLAlchemy
from exceptions.error_types.http_not_found import NotFoundError
from exceptions.errors_handler import errors_handler
from handlers.generais.desvincular_generais import DesvincularGenerais
from models.clifor import Clifor
from models.generais import Generais
from models.usuario import Usuario
from services.send_data_to_app_acutis import SendDataToAppAcutis
from services.send_data_to_memberkit import send_data_to_memberkit
from typing import Tuple, Dict

class UpdateStatusGeneral:
    def __init__(self, general_id: int, db: SQLAlchemy) -> None:
        self.__conn = db
        self.__general_id = general_id
        self.__map_cargo = {1: "marechal", 2: "general"}
        
    def execute(self) -> Tuple[Dict[str, str], int]:
        
        general_to_update = self.__get_general()
        return self.__update_status(general_to_update)       
        
    def __get_general(self) -> Generais:
        general = (
            self.__conn.session.query(Generais)
            .filter(
                Generais.id == self.__general_id,
                Generais.deleted_at.is_(None)
            )
            .first()
        )
        if general is None:
            raise NotFoundError("General não encontrado")

        return general

    def __update_status(self, general_to_update: Generais):
        try:
            general_to_update.status = not general_to_update.status
            
            if general_to_update.status == True: 
                self.__send_general_to_app_acutis_case_aproved(general_to_update)
                self.__send_member_kit_case_aproved(general_to_update)
            
            if general_to_update.status == False:
                self.__case_marechal_reproved(general_to_update)
            
            self.__conn.session.commit()
            return self.__format_response(general_to_update)
                
        except Exception as e:
            self.__conn.session.rollback()
            raise e 


    def __case_marechal_reproved(self, general_to_update: Generais):
        if general_to_update.status == 0 and  general_to_update.fk_cargo_id == 1:
            desvincular_generais = DesvincularGenerais(general_to_update.id, self.__conn)
            desvincular_generais.execute()
    
    
    def __send_member_kit_case_aproved(self, general_to_update: Generais):
        try:
            get_general_data = (
                self.__conn.session.query(Generais.status, Generais.id, Usuario.nome, Usuario.email, Clifor.telefone1.label('telefone'))
                .join(Usuario, Usuario.id == Generais.fk_usuario_id)
                .join(Clifor, Clifor.fk_usuario_id == Usuario.id)
                .filter(
                    Generais.id == self.__general_id, 
                    Generais.deleted_at.is_(None))
                .first()
            )
            
            if general_to_update.status == True:
                send_data_to_memberkit(
                    phone=get_general_data.telefone,
                    full_name=get_general_data.nome,
                    email=get_general_data.email
                )
        except Exception as e:
            raise e
        
        
    def __send_general_to_app_acutis_case_aproved(self, general_aproved: Generais) -> None: 
        try: 
            get_general_aproved = (
                self.__conn.session.query(Generais.fk_cargo_id.label("cargo"), Generais.status, Generais.id, Usuario.nome, Usuario.email, Clifor.cpf_cnpj.label("cpf"))
                .join(Usuario, Usuario.id == Generais.fk_usuario_id)
                .join(Clifor, Clifor.fk_usuario_id == Usuario.id)
                .filter(
                    Generais.deleted_at.is_(None),
                    Generais.id == self.__general_id
                ) 
                .first()
            )      
            
            if general_aproved.status == True:
                payload = {
                    "email": get_general_aproved.email,
                    "cpf": get_general_aproved.cpf,
                    "patent": self.__map_cargo[get_general_aproved.cargo],
                    "name": get_general_aproved.nome
                }
                
                register_general_in_app_acutis = SendDataToAppAcutis(payload)
                register_general_in_app_acutis.execute()
                
        except Exception as e:
            raise e 
                            
    
    def __format_response(self, general_to_update: Generais) -> Tuple[Dict[str, str], int]:

        map_status = {True: "aprovado", False: "recusado"}

        msg = {
            "msg": f"{self.__map_cargo[general_to_update.fk_cargo_id]} {map_status[general_to_update.status]} com sucesso!",
        }

        return msg, 200
