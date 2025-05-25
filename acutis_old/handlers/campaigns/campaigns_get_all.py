from models import (
    Campanha,
    ProcessamentoPedido,
    Pedido,
    LandPage,
    LandpageUsers,
    Usuario,
)
from flask import request as FlaskRequest
from builder import db

from services.factories import file_service_factory


class GetAllCampaigns:
    def __init__(self, request: FlaskRequest):
        self.__http_request_args = request.args
        self.__page = self.__http_request_args.get("page", 1, type=int)
        self.__per_page = self.__http_request_args.get(
            "per_page", 10, type=int
        )

        self.__nome_campanha = self.__http_request_args.get("nome_campanha")
        self.__objetivo = self.__http_request_args.get("objetivo")
        self.__status = self.__http_request_args.get("status")
        self.__publica = self.__http_request_args.get("publica")

    def execute(self):

        campaigns = self.__query_campaigns()
        return self.__format_response(campaigns)

    def __get_campaign_image(self, filename: str) -> str:
        s3_client = file_service_factory()
        url = s3_client.get_public_url(filename)
        return url

    def __query_campaigns(self):
        campaign_query = (
            db.session.query(Campanha)
            .filter(
                Campanha.deleted_at == None,
                (
                    Campanha.titulo.ilike(f"%{self.__nome_campanha}%")
                    if self.__nome_campanha
                    else True
                ),
                (
                    Campanha.objetivo == self.__objetivo
                    if self.__objetivo
                    else True
                ),
                Campanha.status == self.__status if self.__status else True,
                Campanha.publica == self.__publica if self.__publica else True,
            )
            .order_by(Campanha.id.desc())
        )

        return campaign_query.paginate(
            page=self.__page, per_page=self.__per_page, error_out=False
        )

    def __format_response(self, data):
        list_campaigns = []

        for campaign in data.items:
            campaign_data = self.__prepare_campaign_base_data(campaign)

            if campaign.objetivo == "doacao":
                campaign_data["valor_total_atingido"] = (
                    self.__calculate_donation_total(campaign)
                )

            if campaign.objetivo == "cadastro":
                campaign_data.update(self.__get_registration_data(campaign))

            list_campaigns.append(campaign_data)

        pagination = {
            "page": self.__page,
            "per_page": self.__per_page,
            "total_pages": data.pages,
            "total_campaigns": data.total,
        }

        return {"campaigns": list_campaigns, "pagination": pagination}, 200

    def __prepare_campaign_base_data(self, campaign):
        return {
            "id": campaign.id,
            "fk_empresa_id": campaign.fk_empresa_id,
            "titulo": campaign.titulo,
            "descricao": campaign.descricao,
            "data_inicio": (
                campaign.data_inicio.strftime("%Y-%m-%d %H:%M:%S")
                if campaign.data_inicio
                else None
            ),
            "data_fim": (
                campaign.data_fim.strftime("%Y-%m-%d %H:%M:%S")
                if campaign.data_fim
                else None
            ),
            "valor_meta": str(campaign.valor_meta),
            "prorrogado": campaign.prorrogado,
            "data_prorrogacao": (
                campaign.data_prorrogacao.strftime("%Y-%m-%d %H:%M:%S")
                if campaign.data_prorrogacao
                else None
            ),
            "data_fechamento_campanha": (
                campaign.data_fechamento_campanha.strftime("%Y-%m-%d %H:%M:%S")
                if campaign.data_fechamento_campanha
                else None
            ),
            "status": campaign.status,
            "filename": (
                self.__get_campaign_image(campaign.filename)
                if campaign.filename != None
                else True
            ),
            "chave_pix": campaign.chave_pix,
            "data_criacao": campaign.data_criacao.strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
            "usuario_criacao": campaign.usuario_criacao,
            "data_alteracao": (
                campaign.data_alteracao.strftime("%Y-%m-%d %H:%M:%S")
                if campaign.data_alteracao
                else None
            ),
            "usuario_alteracao": campaign.usuario_alteracao,
            "publica": campaign.publica,
            "duracao": campaign.duracao,
            "objetivo": campaign.objetivo,
            "cadastros_meta": campaign.cadastros_meta,
            "preenchimento_foto": campaign.preenchimento_foto,
            "label_foto": campaign.label_foto,
        }

    def __calculate_donation_total(self, campaign):
        valor_arrecadado = (
            db.session.query(db.func.sum(ProcessamentoPedido.valor))
            .join(Pedido, Pedido.id == ProcessamentoPedido.fk_pedido_id)
            .filter(
                Pedido.fk_campanha_id == campaign.id,
                ProcessamentoPedido.status_processamento == 1,
                ProcessamentoPedido.contabilizar_doacao == 1,
                Pedido.contabilizar_doacao == 1,
            )
            .scalar()
            or 0
        )
        return str(round(valor_arrecadado, 2))

    def __get_registration_data(self, campaign):
        get_landpage_campaign = (
            db.session.query(LandPage)
            .join(Campanha, LandPage.campanha_id == Campanha.id)
            .first()
        )

        get_quant_cadastros = db.session.query(
            db.func.count(Usuario.id)
        ).outerjoin(
            LandpageUsers, (Usuario.id == LandpageUsers.user_id) & (LandpageUsers.campaign_id == campaign.id)
        ).filter(
            Usuario.deleted_at.is_(None),
            Usuario.campanha_origem == campaign.id
        ).scalar() or 0

        return {
            "cadastros_total_atingido": get_quant_cadastros,
            "banner_landpage": (
                get_landpage_campaign.banner if get_landpage_campaign else None
            ),
        }
