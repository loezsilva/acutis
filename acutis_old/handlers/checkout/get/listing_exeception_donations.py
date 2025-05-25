from builder import db
from models import ListExceptionDonations
from flask import request
from exceptions.error_types.http_not_found import NotFoundError


class ListingExceptionDonations:
    def __init__(self) -> None:
        self.__http_request = request.args

        self.__per_page = self.__http_request.get("per_page", 10, type=int)
        self.__page = self.__http_request.get("page", 1, type=int)
        self.__cpf_cnpj = self.__http_request.get("cpf_cnpj")
        self.__nome = self.__http_request.get("nome")
        self.__data_inicio = self.__http_request.get("data_inicio")
        self.__data_fim = self.__http_request.get("data_fim")

    def execute(self):
        donations = self.__execute_query()
        return self.__format_response(donations)

    def __execute_query(self):
        try:
            donations_exceptions = (
                db.session.query(ListExceptionDonations)
                .filter(
                    db.and_(
                        (
                            ListExceptionDonations.cpf_cnpj.ilike(
                                f"%{self.__cpf_cnpj}%"
                            )
                            if self.__cpf_cnpj
                            else True
                        ),
                        (
                            ListExceptionDonations.nome.ilike(
                                f"%{self.__nome}%"
                            )
                            if self.__nome
                            else True
                        ),
                        (
                            db.cast(
                                ListExceptionDonations.data_inclusao, db.Date
                            )
                            >= db.cast(self.__data_inicio, db.Date)
                            if self.__data_inicio
                            else True
                        ),
                        (
                            db.cast(
                                ListExceptionDonations.data_inclusao, db.Date
                            )
                            <= db.cast(self.__data_fim, db.Date)
                            if self.__data_fim
                            else True
                        ),
                    )
                )
                .order_by(db.desc(ListExceptionDonations.id))
            )

            paginate = donations_exceptions.paginate(
                page=self.__page, per_page=self.__per_page, error_out=False
            )

            return paginate

        except Exception as err:
            raise NotFoundError(err)

    def __format_response(self, donations: dict):
        paginate = {
            "page": self.__page,
            "per_page": self.__per_page,
            "total_items": donations.total,
        }

        response = [
            {
                "nome": list.nome,
                "fk_clifor_id": list.fk_clifor_id,
                "fk_usuario_id": list.fk_usuario_id,
                "cpf_cnpj": list.cpf_cnpj,
                "data_inclusao": list.data_inclusao.strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),
                "incluido_por": list.incluido_por,
            }
            for list in donations
        ]

        return {"res": response, "pagination": paginate}, 200
