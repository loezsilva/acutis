from flask import request as flask_request
from flask_sqlalchemy import SQLAlchemy

from exceptions.error_types.http_not_found import NotFoundError
from exceptions.error_types.http_unprocessable_entity import (
    HttpUnprocessableEntity,
)
from models.actions_leads import ActionsLeads
from models.foto_leads import FotoLeads
from models.schemas.users.post.register_lead import RegisterLeadFormData
from models.users_imports import UsersImports
from services.file_service import FileService
from utils.functions import get_current_time, is_valid_email, is_valid_name

from utils.regex import format_string


class RegisterLead:
    def __init__(
        self, database: SQLAlchemy, file_service: FileService
    ) -> None:
        self.__database = database
        self.__file_service = file_service

    def execute(self):
        request = RegisterLeadFormData(
            nome=flask_request.form["nome"],
            email=flask_request.form["email"],
            telefone=flask_request.form["telefone"],
            origem=flask_request.form["origem"],
            intencao=flask_request.form.get("intencao"),
            foto=flask_request.files.get("foto"),
        )
        self.__validate_request_data(request)

        action = self.__get_action_data(request.origem)
        lead = self.__get_lead_data_if_exists(request.email, request.origem)
        self.__register_or_update_lead_in_action(request, action, lead)

        return {"msg": "Pré cadastro realizado com sucesso!"}, 201

    def __validate_request_data(self, request: RegisterLeadFormData) -> None:
        request.nome = is_valid_name(request.nome)
        request.email = is_valid_email(
            request.email.strip(),
            check_deliverability=True,
            check_valid_domain=False,
        )
        request.telefone = format_string(
            request.telefone.strip(), only_digits=True
        )

    def __get_action_data(self, origem: int) -> ActionsLeads:
        action: ActionsLeads = self.__database.session.get(
            ActionsLeads, origem
        )
        if not action:
            raise NotFoundError("Ação não encontrada.")

        if not action.status:
            raise HttpUnprocessableEntity(
                "Esta ação não está ativa para receber novos cadastros."
            )

        return action

    def __get_lead_data_if_exists(
        self, email: str, origem: int
    ) -> UsersImports | None:
        lead = UsersImports.query.filter_by(
            email=email, origem_cadastro=origem
        ).first()
        return lead

    def __register_or_update_lead_in_action(
        self,
        request: RegisterLeadFormData,
        action: ActionsLeads,
        lead: UsersImports,
    ) -> None:
        if lead:
            lead.nome = request.nome
            lead.phone = request.telefone
            lead.intencao = request.intencao
            lead.updated_at = get_current_time()

            if action.preenchimento_foto:
                lead_photo: FotoLeads = FotoLeads.query.filter_by(
                    fk_user_import_id=lead.id, fk_action_lead_id=action.id
                ).first()
                if lead_photo:
                    filename = (
                        self.__file_service.upload_image(request.foto)
                        if request.foto
                        else None
                    )
                    lead_photo.foto = filename
                    lead_photo.data_download = None
                    lead_photo.user_download = None
                else:
                    filename = (
                        self.__file_service.upload_image(request.foto)
                        if request.foto
                        else None
                    )
                    lead_photo = FotoLeads(
                        fk_user_import_id=lead.id,
                        fk_action_lead_id=action.id,
                        foto=filename,
                    )
                    self.__database.session.add(lead_photo)
        else:
            lead = UsersImports(
                nome=request.nome,
                email=request.email,
                phone=request.telefone,
                intencao=request.intencao,
                origem_cadastro=action.id,
                data_criacao=get_current_time(),
            )
            self.__database.session.add(lead)
            self.__database.session.flush()

            if action.preenchimento_foto:
                filename = (
                    self.__file_service.upload_image(request.foto)
                    if request.foto
                    else None
                )
                lead_foto = FotoLeads(
                    fk_action_lead_id=action.id,
                    fk_user_import_id=lead.id,
                    foto=filename,
                )
                self.__database.session.add(lead_foto)
        self.__database.session.commit()
