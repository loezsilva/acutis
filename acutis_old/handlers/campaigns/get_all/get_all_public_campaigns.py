from flask_sqlalchemy import SQLAlchemy
from models import Campanha
from services.file_service import FileService


class GetAllPublicCampaigns:
    def __init__(
        self, database: SQLAlchemy, file_service: FileService, page: int, per_page: int
    ) -> None:
        self.__database = database
        self.__file_service = file_service
        self.__page = page
        self.__per_page = per_page

    def execute(self):
        campanhas = self.__get_all_campaigns()
        response = self.__prepare_response(campanhas)
        return response, 200

    def __get_all_campaigns(self):
        campanhas_query = (
            self.__database.session.query(
                Campanha.id,
                Campanha.titulo,
                Campanha.descricao,
                Campanha.objetivo,
                Campanha.filename,
            )
            .filter(
                Campanha.publica == True,
                Campanha.status == True,
                Campanha.deleted_at == None,
            )
            .order_by(Campanha.data_criacao.desc())
        )

        paginate = campanhas_query.paginate(
            page=self.__page, per_page=self.__per_page, error_out=False
        )

        return paginate

    def __get_campaign_image(self, filename: str) -> str:
        url = self.__file_service.get_public_url(filename)
        return url

    def __prepare_response(self, campanhas: list[Campanha]) -> dict:
        response = {
            "page": self.__page,
            "total": campanhas.total,
            "campanhas": [
                {
                    "id": campanha.id,
                    "titulo": campanha.titulo,
                    "descricao": campanha.descricao,
                    "objetivo": campanha.objetivo,
                    "imagem_campanha": self.__get_campaign_image(campanha.filename),
                }
                for campanha in campanhas
            ],
        }

        return response
