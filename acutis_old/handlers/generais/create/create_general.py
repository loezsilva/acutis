from http import HTTPStatus
from flask import request as flask_request
from flask_sqlalchemy import SQLAlchemy
from exceptions.error_types.http_conflict import ConflictError
from exceptions.error_types.http_not_found import NotFoundError
from models.generais import Generais
from models.schemas.admin.post.register_general import RegisterGeneralRequest
from models.usuario import Usuario
from utils.functions import get_current_time


class CreateGeneral:
    def __init__(self, database: SQLAlchemy):
        self.__database = database

    def execute(self):
        request = RegisterGeneralRequest.parse_obj(flask_request.json)
        usuario = self.__get_user_data(request.fk_usuario_id)
        general = self.__check_general_already_registered(usuario)
        self.__register_general(request, general)

        return {"msg": "General criado com sucesso!"}, HTTPStatus.CREATED

    def __get_user_data(self, fk_usuario_id: int) -> Usuario:
        usuario: Usuario = self.__database.session.get(Usuario, fk_usuario_id)

        if usuario is None or usuario.deleted_at is not None:
            raise NotFoundError("Usuário não encontrado.")

        return usuario

    def __check_general_already_registered(self, usuario: Usuario) -> None:
        general = (
            Generais.query.join(Usuario, Usuario.id == Generais.fk_usuario_id)
            .filter(Usuario.id == usuario.id, Usuario.deleted_at.is_(None))
            .first()
        )

        return general

    def __register_general(self, request: RegisterGeneralRequest, general: Generais) -> None:
        
        if general is None:
            new_general = Generais(
                fk_cargo_id=2,
                quant_membros_grupo=request.quant_membros_grupo,
                nome_grupo=request.nome_grupo,
                link_grupo=request.link_grupo,
                tempo_de_administrador=request.tempo_de_administrador,
                fk_usuario_id=request.fk_usuario_id,
            )
            self.__database.session.add(new_general)
            self.__database.session.commit()
            
            return
        
        if general != None and general.deleted_at != None: 
            general.quant_membros_grupo = request.quant_membros_grupo
            general.nome_grupo = request.nome_grupo
            general.link_grupo = request.link_grupo
            general.tempo_de_administrador = request.tempo_de_administrador
            general.fk_cargo_id=2
            general.fk_usuario_superior_id = None
            general.status = 0
            general.deleted_at = None
            general.created_at = get_current_time()
            general.updated_at = get_current_time()
            
            self.__database.session.commit()
            return 
        
        if general: 
            raise ConflictError("General já cadastrado.")