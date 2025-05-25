from datetime import timedelta
from typing import Optional
from flask_jwt_extended import current_user
from flask_sqlalchemy import SQLAlchemy
from flask import request as flask_request
import pytz

from exceptions.error_types.http_conflict import ConflictError
from exceptions.error_types.http_not_found import NotFoundError
from models.campanha import Campanha
from models.evento_usuario import EventoUsuario
from models.schemas.users.post.register_presence import RegisterPresenceRequest
from services.send_data_to_app_acutis import SendDataToAppAcutis
from utils.functions import get_current_time


class RegisterPresence:
    def __init__(self, database: SQLAlchemy):
        self.__database = database

    def execute(self):
        request = RegisterPresenceRequest.parse_obj(flask_request.json)
        landing_page = request.fk_landpage_id
        campaign = self.__get_campaign_data(request.fk_campanha_id)

        presence = self.__checks_user_already_present(campaign.id)
        self.__register_user_presence(presence, campaign, landing_page)
        self.__commit_changes()
        
        if request.fk_campanha_id == 43:
            # envia dados do usuário para o app acutis quando presença registrada na campanha 43
            payload = {
                "email": current_user["email"],
                "cpf": current_user["numero_documento"],
                "patent": "membro",
                "name": current_user["nome"]
            }
                        
            register_general_in_app_acutis = SendDataToAppAcutis(payload)
            register_general_in_app_acutis.execute()

        return {"msg": "Presença registrada com sucesso!"}, 201

    def __get_campaign_data(self, fk_campanha_id: int) -> Campanha:
        campaign = self.__database.session.get(Campanha, fk_campanha_id)
        if campaign is None:
            raise NotFoundError("Campanha não encontrada.")

        return campaign

    def __checks_user_already_present(
        self, fk_campanha_id: int
    ) -> Optional[EventoUsuario]:
        presence: EventoUsuario = EventoUsuario.query.filter_by(
            fk_usuario_id=current_user["id"], fk_campanha_id=fk_campanha_id
        ).first()
        if presence:
            tz = pytz.timezone("America/Fortaleza")
            data_register_aware = (
                tz.localize(presence.data_register)
                if presence.data_register.tzinfo is None
                else presence.data_register
            )
            if (get_current_time() - timedelta(hours=3)) < data_register_aware:
                raise ConflictError("Registro de presença já realizado anteriormente")

        return presence

    def __register_user_presence(
        self,
        presence: Optional[EventoUsuario],
        campaign: Campanha,
        landing_page: Optional[int],
    ) -> None:
        if presence:
            presence.presencas += 1
            presence.data_register = get_current_time()
            if landing_page:
                presence.fk_landpage_id = landing_page
        else:
            presence = EventoUsuario(
                fk_usuario_id=current_user["id"],
                fk_campanha_id=campaign.id,
                fk_landpage_id=landing_page,
                presencas=1,
            )
            self.__database.session.add(presence)

    def __commit_changes(self) -> None:
        try:
            self.__database.session.commit()
        except Exception as exception:
            self.__database.session.rollback()
            raise exception
