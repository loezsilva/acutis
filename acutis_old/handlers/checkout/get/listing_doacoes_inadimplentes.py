from http import HTTPStatus
from flask import request
from models.schemas.checkout.schema_recurrence_not_paid import ListagemDeRecorreciaEmLapsosRequest
from repositories.interfaces.checkout_repository_interface import CheckoutRepositoryInterface

class ListingDoacoesInadimplentes:
    def __init__(self, checkout_repository: CheckoutRepositoryInterface) -> None:
        self.__checkout_repository = checkout_repository
        
        self.__http_request = ListagemDeRecorreciaEmLapsosRequest(**request.args)

    def execute(self):
        data = self.__checkout_repository.query_doacoes_inadimplentes(self.__http_request, "listagem")
        return self.__format_response(data)
        
    
    def __format_response(self, data):
        res = {
            "page": data.page,
            "pages": data.pages,
            "total": data.total,
            "doacoes_nao_efetivadas": [
                {
                    "id": doacao.id,
                    "benfeitor": doacao.benfeitor,
                    "benfeitor_id": doacao.benfeitor_id,
                    "data": doacao.data.strftime("%d/%m/%Y %H:%M:%S"),
                    "valor": str(round(doacao.valor, 2)),
                    "campanha": doacao.titulo,
                    "fk_campanha_id": doacao.fk_campanha_id,
                }
                for doacao in data
            ],
        }
        
        return res, HTTPStatus.OK