from xml.dom import NotFoundErr
from models import Campanha
from builder import db


class DeleteCampaign:
    def __init__(self, campaign_id: int) -> dict:
        self.__campaign_id = campaign_id

    def execute(self):
        campaign = self.__campaign_exists()

        return self.__delete_campaing(campaign)

    def __campaign_exists(self) -> Campanha:
        campaign = (
            db.session.query(Campanha)
            .filter(
                Campanha.id == self.__campaign_id, Campanha.deleted_at == None
            )
            .first()
        )
        if campaign is None:
            raise NotFoundErr("Campanha não encontrada")
        return campaign

    def __delete_campaing(self, campaing: Campanha) -> tuple:
        try:
            campaing.soft_delete()

            response = {"msg": "Campanha deletada com sucesso!"}

            return response, 200

        except Exception:
            db.session.rollback()
            response = {"error": "Ocorreu um error ao deletar campanha!"}

            return response, 500
