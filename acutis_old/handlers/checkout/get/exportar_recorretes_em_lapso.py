from http import HTTPStatus
from flask import request
from models.schemas.checkout.schema_recurrence_not_paid import ListagemDeRecorreciaEmLapsosRequest
from repositories.interfaces.checkout_repository_interface import CheckoutRepositoryInterface
from utils.export_excel import export_excel

class ExportarDoacoesEmLapsos:
    def __init__(self, checkout_repository: CheckoutRepositoryInterface) -> None:
        self.__checkout_repository = checkout_repository
        self.__http_request = ListagemDeRecorreciaEmLapsosRequest(**request.args)

    def execute(self):
        data = self.__checkout_repository.query_doacoes_inadimplentes(self.__http_request, "exportar")
        
        return self.__formatar_resposta(data)
        
    def __formatar_resposta(self, data):
        
        lista_para_exportar = []
        
        for doacao in data: 
            
            lista_para_exportar.append(
                {
                    "id": doacao.id,
                    "Nome": doacao.benfeitor,
                    "CPF/CNPJ": doacao.cpf_cnpj,                   
                    "data": doacao.data.strftime("%d/%m/%Y %H:%M:%S"),
                    "valor": str(round(doacao.valor, 2)),
                    "campanha": doacao.titulo,
                    "fk_campanha_id": doacao.fk_campanha_id
                }
            )
        
        return export_excel(lista_para_exportar, "doacoes_em_lapsos"), HTTPStatus.OK
        