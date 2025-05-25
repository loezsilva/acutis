from flask import request, jsonify
from flask_sqlalchemy import SQLAlchemy
from models.usuario import Usuario
from models.endereco import Endereco
from models.campanha import Campanha
from models.clifor import Clifor
from models.landpage_usuarios import LandpageUsers

class UsersAndCampaignsByRegion:
    def __init__(self, conn: SQLAlchemy):
        self.__conn = conn

    def execute(self) -> tuple:
        page, per_page = self.__get_pagination_params()

        query = self.__get_query()
        paginated_result = query.paginate(page=page, per_page=per_page, error_out=False)
        users_by_region_list = self.__format_response(paginated_result.items)

        response = {
            "users_and_campaigns_by_region": users_by_region_list,
            "page": page,
            "per_page": per_page,
            "total_campaigns": paginated_result.total,
            "total_pages": (paginated_result.total + per_page - 1) // per_page,
        }

        return jsonify(response), 200


    def __get_pagination_params(self):
        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 10, type=int)
        return page, per_page

    def __get_query(self):
        return (
            self.__conn.session.query(
                Endereco.cidade,
                Campanha.titulo.label("campanha_destaque"),
                self.__conn.func.count(self.__conn.distinct(Usuario.id)).label("quantidade_usuarios"),
                (
                    self.__conn.func.count(self.__conn.distinct(Usuario.id))
                    * 100.0
                    / self.__conn.session.query(self.__conn.func.count())
                    .filter(Usuario.deleted_at.is_(None))
                    .scalar()
                ).label("percentage"),
                self.__conn.func.count(
                    self.__conn.case((Usuario.campanha_origem == Campanha.id, Usuario.id))
                ).label("quantidade_campanha_destaque"),
            )
            .join(LandpageUsers, LandpageUsers.user_id == Usuario.id)
            .join(Clifor, Clifor.fk_usuario_id == Usuario.id)
            .join(Endereco, Endereco.fk_clifor_id == Clifor.id)
            .join(Campanha, Campanha.id == LandpageUsers.campaign_id)
            .filter(Usuario.deleted_at.is_(None))
            .group_by(Endereco.cidade, Campanha.titulo)
            .order_by(self.__conn.desc("quantidade_usuarios"))
        )

    def __format_response(self, paginated_items):
        return [
            {
                "cidade": item.cidade,
                "campanha_destaque": item.campanha_destaque,
                "quantidade_usuarios": item.quantidade_usuarios,
                "percentage": round(item.percentage, 2),
                "quantidade_campanha_destaque": item.quantidade_campanha_destaque,
            }
            for item in paginated_items
        ]