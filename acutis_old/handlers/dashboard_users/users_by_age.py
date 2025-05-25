from flask import jsonify
from flask_sqlalchemy import SQLAlchemy
from models.usuario import Usuario
from models.clifor import Clifor

class UserByAge:
    def __init__(self, conn: SQLAlchemy):
        self.__conn = conn

    def execute(self) -> tuple:
        try:
            user_by_age_data = self.__get_user_by_age_data()
            response = self.__format_response(user_by_age_data)
            return response

        except Exception as e:
            return jsonify({"error": str(e)}), 500

    def __get_user_by_age_data(self) -> list:
        year_diff = self.__conn.func.datediff(
            self.__conn.text("YEAR"), Clifor.data_nascimento, self.__conn.func.getdate()
        )

        faixa_etaria_case = self.__conn.case(
            (year_diff.between(15, 24), "15 a 24"),
            (year_diff.between(25, 34), "25 a 34"),
            (year_diff.between(35, 44), "35 a 44"),
            (year_diff.between(45, 59), "45 a 59"),
            (year_diff.between(60, 74), "60 a 74"),
            else_="75 ou mais",
        ).label("faixa_etaria")

        subquery = (
            self.__conn.session.query(
                Usuario.id.label("usuario_id"),
                faixa_etaria_case,
                Clifor.sexo
            )
            .join(Clifor, Clifor.fk_usuario_id == Usuario.id)
            .filter(Usuario.deleted_at.is_(None))
            .subquery()
        )

        query = (
            self.__conn.session.query(
                subquery.c.faixa_etaria,
                self.__conn.func.count(self.__conn.case((subquery.c.sexo == "feminino", 1))).label("female_count"),
                self.__conn.func.count(self.__conn.case((subquery.c.sexo == "masculino", 1))).label("male_count"),
                self.__conn.func.count(
                    self.__conn.case((subquery.c.sexo.is_(None) | (subquery.c.sexo == ""), 1))
                ).label("no_gender")
            )
            .group_by(subquery.c.faixa_etaria)
            .order_by(subquery.c.faixa_etaria)
        )

        return query.all()

    def __format_response(self, user_by_age_data: list) -> tuple:
        result_user_by_age = []
        for row in user_by_age_data:
            faixa_etaria, female_count, male_count, no_gender = row
            total_count = female_count + male_count + no_gender
            result_user_by_age.append(
                {
                    "age_range": faixa_etaria,
                    "female_count": female_count,
                    "male_count": male_count,
                    "desconhecido": no_gender,
                    "total_count": total_count,
                }
            )

        return jsonify({"user_by_age": result_user_by_age}), 200
