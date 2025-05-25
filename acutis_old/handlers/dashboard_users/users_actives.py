from flask import jsonify
from flask_sqlalchemy import SQLAlchemy
from models.clifor import Clifor
from models.usuario import Usuario


class UserActives:
    def __init__(self, conn: SQLAlchemy):
        self.__conn = conn
    
    def execute(self):
        total_users_register = (
            self.__conn.session.query(Usuario).filter(Usuario.deleted_at == None).count()
        )

        data = self.__get_user_data()
        response = self.__format_response(data, total_users_register)

        return jsonify(response), 200
    
    def __get_user_data(self):
        return (
            self.__conn.session.query(
                self.__conn.func.count(Usuario.id).label("quant_by_gender"),
                Clifor.sexo,
                Usuario.status,
            )
            .join(Clifor, Clifor.fk_usuario_id == Usuario.id)
            .filter(Usuario.deleted_at == None)
            .group_by(Clifor.sexo, Usuario.status)
            .all()
        )

    def __format_response(self, data, total_users_register):
        user_summary = {
            "female": {"active": 0, "inactive": 0},
            "male": {"active": 0, "inactive": 0},
            "no_gender": {"active": 0, "inactive": 0},
        }

        sexo_map = {
            "feminino": "female",
            "masculino": "male",
            None: "no_gender",  
        }

        for row in data:
            sexo = sexo_map.get(row.sexo, "no_gender")  
            status_key = "active" if row.status == 1 else "inactive"
            user_summary[sexo][status_key] += row.quant_by_gender

        total_users_actives = sum(group["active"] for group in user_summary.values())
        total_users_inactives = sum(group["inactive"] for group in user_summary.values())
        total_users_no_gender = sum(user_summary["no_gender"].values())
        total_users_female = sum(user_summary["female"].values())
        total_users_male = sum(user_summary["male"].values())

        percent_active_users = (total_users_actives / total_users_register) * 100
        percent_inactive_users = (total_users_inactives / total_users_register) * 100
        percent_female_users = (total_users_female / total_users_register) * 100
        percent_male_users = (total_users_male / total_users_register) * 100
        percent_null_sex_users = (total_users_no_gender / total_users_register) * 100

        response = {
            "users_active": total_users_actives,
            "user_inactive": total_users_inactives,
            "percent_active_users": round(percent_active_users, 2),
            "percent_inactive_users": round(percent_inactive_users, 2),
            "percent_female_users": round(percent_female_users, 2),
            "percent_male_users": round(percent_male_users, 2),
            "percent_null_sex_users": round(percent_null_sex_users, 2),
        }

        return response


