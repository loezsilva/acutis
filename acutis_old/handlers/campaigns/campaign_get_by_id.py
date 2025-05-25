from exceptions.error_types.http_not_found import NotFoundError

from models import (
    Campanha,
    Pedido,
    ProcessamentoPedido,
    LandPage,
    LandpageUsers,
    SetupPagamento,
    Usuario
)
from builder import db
from services.factories import file_service_factory
import logging
from utils.functions import get_current_time


class CampaignGetById:
    def __init__(self, campaign_id: int) -> dict:
        self.__campaign_id = campaign_id

    def execute(self):
        
        campaign = self.__get_campaign()
        if campaign is None:
            raise NotFoundError("Campanha não encontrada")

        return campaign

    def __get_campaign_image(self, filename: str) -> str:
        s3_client = file_service_factory()
        url = s3_client.get_public_url(filename)
        return url

    def __get_campaign(self):
        try:

            valor_total_mes_atual = None
            get_landpage_campaign = None
            get_quant_cadastros = None
            get_quant_cadastros_mes_atual = None

            columns_to_select = [
                Campanha.id.label("campanha_id"),
                Campanha.titulo.label("campanha_nome"),
                Campanha.data_inicio,
                Campanha.objetivo,
                Campanha.status,
                Campanha.publica,
                Campanha.valor_meta,
                Campanha.descricao,
                Campanha.cadastros_meta,
                Campanha.data_criacao,
                Campanha.data_alteracao,
                Campanha.duracao,
                Campanha.filename,
                Campanha.data_fim,
                Campanha.label_foto,
                Campanha.preenchimento_foto,
                Campanha.chave_pix,
                SetupPagamento.boleto_recorrente,
                SetupPagamento.boleto_unico,
                SetupPagamento.credito_recorrente,
                SetupPagamento.credito_recorrente,
                SetupPagamento.credito_unico,
                SetupPagamento.id.label("setup_id"),
                SetupPagamento.pix_recorrente,
                SetupPagamento.pix_unico,
            ]

            result: Campanha = (
                (db.session.query(*columns_to_select))
                .outerjoin(
                    SetupPagamento,
                    SetupPagamento.fk_campanha_id == Campanha.id,
                )
                .filter(
                    Campanha.id == self.__campaign_id,
                    Campanha.deleted_at == None,
                )
                .first()
            )

            # Busca valor arrecadado pela campanha
            valor_total_query_campanha = None
            if result.objetivo == "doacao":
                query_valores = (
                    db.session.query(db.func.sum(ProcessamentoPedido.valor))
                    .join(
                        Pedido, ProcessamentoPedido.fk_pedido_id == Pedido.id
                    )
                    .filter(
                        ProcessamentoPedido.contabilizar_doacao == 1,
                        Pedido.contabilizar_doacao == 1,
                        ProcessamentoPedido.status_processamento == 1,
                        Pedido.fk_campanha_id == self.__campaign_id,
                    )
                )

                valor_total_query_campanha = query_valores.scalar()

                valor_total_mes_atual = query_valores.filter(
                    db.func.month(ProcessamentoPedido.data_processamento)
                    == get_current_time().month,
                    db.func.year(ProcessamentoPedido.data_processamento)
                    == get_current_time().year,
                ).scalar()

            # Busca landpage e quantida de cadastros da campanha caso a campanha for de cadastro
            if result.objetivo == "cadastro":
                get_landpage_campaign = (
                    db.session.query(LandPage)
                    .join(Campanha, LandPage.campanha_id == result.campanha_id)
                    .first()
                )

                query_quant_cadastros = (
                    db.session.query(db.func.count(db.distinct(Usuario.id)))
                    .join(LandpageUsers, LandpageUsers.user_id == Usuario.id, isouter=True)
                    .join(Campanha, Campanha.id == LandpageUsers.campaign_id, isouter=True)
                    .filter(
                        db.or_(
                            Campanha.id == self.__campaign_id,
                            Usuario.campanha_origem == self.__campaign_id
                        ),
                        Usuario.deleted_at == None
                    )
                )
                
                get_quant_cadastros_mes_atual = (
                    db.session.query(db.func.count(db.distinct(Usuario.id)))
                    .join(LandpageUsers, LandpageUsers.user_id == Usuario.id, isouter=True)
                    .join(Campanha, Campanha.id == LandpageUsers.campaign_id, isouter=True)
                    .filter(
                        db.or_(
                            Campanha.id == self.__campaign_id,
                            Usuario.campanha_origem == self.__campaign_id
                        ),
                        Usuario.deleted_at == None,
                        db.func.month(Usuario.data_criacao) == get_current_time().month,
                        db.func.year(Usuario.data_criacao) == get_current_time().year
                    )
                ).scalar()

                get_quant_cadastros = query_quant_cadastros.scalar()

            data_campaign = {
                "id": result.campanha_id,
                "campanha_nome": result.campanha_nome,
                "data_inicio": (
                    str(result.data_inicio.strftime("%d-%m-%Y %H:%M:%S"))
                    if result.data_inicio
                    else None
                ),
                "data_fim": (
                    str(result.data_fim.strftime("%d-%m-%Y %H:%M:%S"))
                    if result.data_fim
                    else None
                ),
                "objetivo": result.objetivo,
                "valor_total": (
                    str(round(valor_total_query_campanha, 2))
                    if valor_total_query_campanha
                    else None
                ),
                "valor_meta": (
                    str(round(result.valor_meta, 2))
                    if result.valor_meta != None
                    else None
                ),
                "status": result.status,
                "publica": result.publica,
                "descricao": result.descricao,
                "cadastros_meta": result.cadastros_meta,
                "data_criacao": result.data_criacao.strftime(
                    "%d-%m-%Y %H:%M:%S"
                ),
                "data_alteracao": (
                    str(result.data_alteracao.strftime("%d-%m-%Y %H:%M:%S"))
                    if result.data_alteracao
                    else None
                ),
                "duracao": result.duracao,
                "filename": (
                    self.__get_campaign_image(result.filename)
                    if result.filename
                    else None
                ),
                "label_foto": result.label_foto,
                "cadastros_total_atingido": (
                    get_quant_cadastros if get_quant_cadastros else None
                ),
                "preenchimento_foto": result.preenchimento_foto,
                "chave_pix": result.chave_pix,
                "valor_total_mes_atual": (
                    str(round(valor_total_mes_atual, 2))
                    if valor_total_mes_atual
                    else None
                ),
                "cadastros_total_mes_atual": get_quant_cadastros_mes_atual,
            }

            if get_landpage_campaign:
                data_landing_page = {
                    "tipo_cadastro": get_landpage_campaign.tipo_cadastro,
                    "id": get_landpage_campaign.id,
                    "url": get_landpage_campaign.url,
                    "titulo": get_landpage_campaign.titulo,
                    "banner": (
                        self.__get_campaign_image(get_landpage_campaign.banner)
                        if get_landpage_campaign
                        else None
                    ),
                    "descricao": get_landpage_campaign.descricao,
                    "texto_email_pos_registro": get_landpage_campaign.texto_email_pos_registro,
                    "texto_pos_registro": get_landpage_campaign.texto_pos_registro,
                }
            else:
                data_landing_page = {}

            if result.objetivo == "doacao":
                dados_setup_pagamento = {
                    "boleto_recorrente": result.boleto_recorrente,
                    "boleto_unico": result.boleto_unico,
                    "credito_recorrente": result.credito_recorrente,
                    "credito_unico": result.credito_unico,
                    "id": result.setup_id,
                    "pix_recorrente": result.pix_recorrente,
                    "pix_unico": result.pix_unico,
                }
            else:
                dados_setup_pagamento = {}

            res = {
                "dados_campanha": data_campaign,
                "dados_landing_page": data_landing_page,
                "dados_setup_pagamento": dados_setup_pagamento,
            }

            return res, 200

        except Exception as err:
            response = {"error": "Erro ao buscar campanha!"}
            logging.error(f"{type(err)} - {err}")
            return response, 500
