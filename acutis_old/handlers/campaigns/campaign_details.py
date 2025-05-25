import re
from flask import request
from exceptions.error_types.http_not_found import NotFoundError
from models.campanha import Campanha
from models.clifor import Clifor
from models.landpage_usuarios import LandpageUsers
from models.pedido import Pedido
from models.processamento_pedido import ProcessamentoPedido
from models.usuario import Usuario


class CampaignsDetails:
    
    def __init__(self, conn) -> None:
        self.__conn = conn
        self.__http_request_args = request.args

        self.__page = self.__http_request_args.get("page", 1, type=int)
        self.__per_page = self.__http_request_args.get("per_page", 10, type=int)

        self.__campaign_filter = self.__http_request_args.get("campanha_id")

    def execute(self):
        campanha: Campanha = self.__verify_campaign(self.__campaign_filter)
        if campanha.objetivo == "cadastro":
            campanha_details_users = self.__info_users_campaing(campanha.id)
        else:
            campanha_details_users = None
            

        if campanha.objetivo == "doacao":
            campanha_details_donations = self.__info_donations_campaign(campanha.id)
        else:
            campanha_details_donations = None
            
        
        response = self.__format_response(campanha.titulo, campanha_details_users, campanha_details_donations)
        
        return response
        
    def __verify_campaign(self, campanha_id: int) -> dict:
        campanha = self.__conn.session.query(Campanha).filter(Campanha.id == campanha_id).first()
        if campanha is None:
            raise NotFoundError("Campanha inválida")

        return campanha

    def __info_users_campaing(self, campanha_id: int) -> tuple:
        
        select_columns = [
            LandpageUsers.landpage_id.label("landpage_id"),
            Usuario.id.label("user_id"),
            Usuario.nome,
            Usuario.email,
            Usuario.status,
            Usuario.data_criacao,
        ]
        
        data_user = self.__conn.session.query(*select_columns).join(
            Usuario, LandpageUsers.user_id == Usuario.id
        ).filter(LandpageUsers.campaign_id == campanha_id).order_by(LandpageUsers.registered_at.desc())
        
        data_users_paginate = data_user.paginate(page=self.__page, per_page=self.__per_page)
        
        return self.__response_data_users(data_users_paginate)
        
    def __response_data_users(self, data_users):
        
        MAP_STATUS = { 0: "Inativo", 1: "Ativo"}
        
        users_list = [
            {
                "id": user.user_id,
                "nome": user.nome,
                "email": user.email,
                "data_cadastro": user.data_criacao.strftime("%d/%m/%Y %H:%M:%S"),
                "status": MAP_STATUS[user.status],
            }
            for user in data_users.items
        ]
        return users_list
        
    def __info_donations_campaign(self, campanha_id: int) -> list:
        query_donations = (
            self.__conn.session.query(Pedido, ProcessamentoPedido, Clifor)
            .join(ProcessamentoPedido, Pedido.id == ProcessamentoPedido.fk_pedido_id)
            .join(Clifor, Clifor.id == Pedido.fk_clifor_id)
            .filter(Pedido.fk_campanha_id == campanha_id)
            .order_by(ProcessamentoPedido.data_processamento.desc())
        )
        
        paginate = query_donations.paginate(page=self.__page, per_page=self.__per_page, error_out=False)
        
        if query_donations is None:
            raise NotFoundError("Nenhuma doação encotrada")
        
        return self.__response_donations_campaigns(paginate)
    
    def __response_donations_campaigns(self, data: tuple) -> list:
        
        STATUS_PROCESSAMENTO_MAP = {0: "Em processamento", 1: "Pago", 2: "Não efetuado"}
        FORMA_PAGAMENTO_MAP = {1: "Cartão de Crédito", 2: "Pix", 3: "Boleto"}
        
        donations_data = [
            {
                "id": pedido.id,
                "valor": str(round(pedido.valor_total_pedido, 2)),
                "data_doacao": processamento.data_processamento.strftime("%d/%m/%Y %H:%M:%S"),
                "recorrente": pedido.recorrencia_ativa,
                "transaction_id": processamento.transaction_id,
                "referencia": processamento.id_transacao_gateway,
                "clifor": clifor.nome,
                "forma_pagamento": FORMA_PAGAMENTO_MAP[pedido.fk_forma_pagamento_id],
                "status_pedido": STATUS_PROCESSAMENTO_MAP[pedido.status_pedido],
            }
            for pedido, processamento, clifor in data.items
        ]
        
        return donations_data

    def __format_response(self, campanha_nome: str, details_users: dict = None, details_donations: dict = None) -> tuple:
        response = {
            "campaign": campanha_nome,
            "details_donations": details_donations,
            "details_users": details_users,
            "page": self.__page,
            "per_page": self.__per_page
        }
        
        return response, 200