from flask import request
from flask_sqlalchemy import SQLAlchemy

from exceptions.error_types.http_not_found import NotFoundError
from models.campanha import Campanha
from models.landpage_usuarios import LandpageUsers
from models.usuario import Usuario


class GetRegisterOfCampaign:
    def __init__(self, conn: SQLAlchemy, campaign_id: int):
        self.__conn = conn
        self.__http_args = request.args
        self.__page = self.__http_args.get("page")
        self.__per_page = self.__http_args.get("per_page")
        self.__campaign_id = campaign_id
    
    def execute(self):
        self.__verify_campaign()
        data = self.__get_register()
        return self.__format_response(data)
    
    def __get_register(self):
        query = (
            self.__conn.session.query(LandpageUsers, Usuario)
            .join(Usuario, Usuario.id == LandpageUsers.user_id)
            .filter(LandpageUsers.campaign_id == self.__campaign_id)
            .order_by(self.__conn.desc(Usuario.data_criacao))
        )
        
        paginate = query.paginate(
            page=self.__page, per_page=self.__per_page, error_out=False
        )
        
        return paginate
    
    def __format_response(self, data: tuple) -> tuple:
        
        MAP_STATUS = {True: "Ativo", False: "Inativo"}
        
        res = [
            {
                "user_id": user.nome,
                "email": user.email,
                "ultimo_acesso": (
                    user.data_ultimo_acesso.strftime("%Y-%m-%d %H:%S:%M")
                    if user.data_ultimo_acesso != None
                    else None
                ),
                "data_criacao": user.data_criacao.strftime("%Y-%m-%d %H:%S:%M"),
                "status": MAP_STATUS[user.status],
            }
            for landpage, user in data
        ]

        return {
            "res": res,
            "paginate": data.total,
            "page": data.page,
            "per_page": self.__per_page,
        }, 200
        
    def __verify_campaign(self):
        campaign = self.__conn.session.query(Campanha).filter(Campanha.id == self.__campaign_id).first()
        
        if campaign is None:
            raise NotFoundError("Campanha inválida")
        
        