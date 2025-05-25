from models.mensageria import Mensageria
from typing import List
from flask import request
from flask_sqlalchemy import SQLAlchemy
from models.mensageria.tipo_email import TipoEmail


class GetEmailsSent:
    def __init__(self, database: SQLAlchemy) -> None:
        self.__conn = database
        self.__page = request.args.get("page", 1, type=int)
        self.__per_page = request.args.get("per_page", 10, type=int)

    def execute(self):
        filters = self.__get_all_filters()
        data_emails = self.__get_emails_sent(filters)
        return self.__format_response(data_emails)

    def __get_emails_sent(self, filters: List):
        emails_sent = (
            self.__conn.session.query(Mensageria)
            .filter(*filters)
            .order_by(Mensageria.id.desc())
        )

        paginate_res = emails_sent.paginate(
            page=self.__page,
            per_page=self.__per_page,
        )

        return paginate_res

    def __get_all_filters(self) -> List:
        filter_mapping = {
            "sg_message_id": lambda value: Mensageria.sg_message_id == value,
            "status": lambda value: Mensageria.status == value,
            "email": lambda value: Mensageria.email.ilike(f"%{value}%"),
            "tipo_email": lambda value: Mensageria.tipo_email == value,
            "data_inicial": lambda value: self.__conn.cast(
                Mensageria.created_at, self.__conn.Date
            )
            >= self.__conn.cast(value, self.__conn.Date),
            "data_final": lambda value: self.__conn.cast(
                Mensageria.created_at, self.__conn.Date
            )
            <= self.__conn.cast(value, self.__conn.Date),
        }

        filters = []
        for key, filter_func in filter_mapping.items():
            value = request.args.get(key)
            if value:
                filters.append(filter_func(value))

        return filters

    def __format_response(self, emails_sent: list):

        if not emails_sent.items:
            return {
                "data": [],
                "pagination": {
                    "page": self.__page,
                    "per_page": self.__per_page,
                    "total": 0,
                    "total_pages": 0,
                },
            }, 200

        res = [
            {
                "id": email.id,
                "sg_message_id": email.sg_message_id,
                "status": email.status,
                "email": email.email,
                "url": email.url,
                "created_at": email.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                "updated_at": (
                    email.updated_at.strftime("%Y-%m-%d %H:%M:%S")
                    if email.updated_at
                    else None
                ),
                "tipo_email": TipoEmail.query.get(email.fk_tipo_email_id).slug,
                "motivo_retorno": email.motivo_retorno,
            }
            for email in emails_sent.items
        ]

        pagination = {
            "page": emails_sent.page,
            "per_page": emails_sent.per_page,
            "total": emails_sent.total,
            "total_pages": emails_sent.pages,
        }

        return {"data": res, "pagination": pagination}, 200
