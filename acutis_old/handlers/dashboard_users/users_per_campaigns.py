from flask import jsonify
from flask_sqlalchemy import SQLAlchemy

from models.campanha import Campanha
from models.usuario import Usuario
from models.landpage_usuarios import LandpageUsers


class UsersPerCampaigns:
    def __init__(self, conn: SQLAlchemy):
        self.__conn = conn

    def execute(self) -> tuple:
        try:
            resultado = self.__get_users_per_campaign()
            total_usuarios = self.__get_total_users()
            response = self.__format_response(resultado, total_usuarios)
            return response
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    def __get_users_per_campaign(self) -> list:
        return (
            self.__conn.session.query(
                Campanha.titulo.label("campanha"),
                self.__conn.func.count(Usuario.id).label("quantidade_usuarios"),
            )
            .select_from(Usuario)
            .join(Campanha, Usuario.campanha_origem == Campanha.id)
            .outerjoin(
                LandpageUsers,
                (Usuario.id == LandpageUsers.user_id)
                & (LandpageUsers.campaign_id == Campanha.id),
            )
            .filter(Usuario.deleted_at.is_(None), Campanha.deleted_at.is_(None))
            .group_by(Campanha.titulo)
            .all()
        )

    def __get_total_users(self) -> int:
        return (
            self.__conn.session.query(self.__conn.func.count(Usuario.id))
            .filter(Usuario.deleted_at.is_(None))
            .scalar()
        )

    def __format_response(self, resultado: list, total_usuarios: int) -> tuple:
        usuarios_por_campanha = []

        for campanha, quantidade in resultado:
            percentual = (
                (quantidade / total_usuarios) * 100 if total_usuarios > 0 else 0
            )
            usuarios_por_campanha.append(
                {
                    "campanha": campanha,
                    "quantidade_usuarios": quantidade,
                    "percentual": round(percentual, 2),
                }
            )

        return jsonify({"usuarios_por_campanha": usuarios_por_campanha}), 200
