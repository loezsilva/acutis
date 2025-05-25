import datetime
from flask import request
from flask_sqlalchemy import SQLAlchemy
from models import (
    Pedido,
    Clifor,
    Campanha,
    FormaPagamento,
)
from utils.export_excel import export_excel

class ExportDonationsCanceladas:
    def __init__(self, conn: SQLAlchemy) -> None:
        self.__conn = conn
        self.__http_args = request.args
        self.__nome_usuario = self.__http_args.get("nome")
        self.__data_inicial = self.__http_args.get("data_inicial")
        self.__data_final = self.__http_args.get("data_final")
        self.__campanha = self.__http_args.get("campanha_id")

    def execute(self):
        donations = self.__query_donations_canceladas()
        return self.__generate_csv(donations)

    def __query_donations_canceladas(self):
        query = (
            self.__conn.session.query(
                Pedido.id,
                Pedido.cancelada_em,
                Clifor.nome,
                Clifor.cpf_cnpj,
                Campanha.titulo,
                Pedido.data_pedido,
                FormaPagamento.descricao.label("metodo_pagamento"),
                Pedido.valor_total_pedido,
            )
            .join(Clifor, Clifor.id == Pedido.fk_clifor_id)
            .join(Campanha, Campanha.id == Pedido.fk_campanha_id)
            .join(FormaPagamento, FormaPagamento.id == Pedido.fk_forma_pagamento_id)
            .filter(
                Pedido.status_pedido == 2,
                Pedido.periodicidade == 2,
                Pedido.recorrencia_ativa == False,  
                Pedido.contabilizar_doacao == True,
                (Campanha.id == self.__campanha if self.__campanha else True),
                (
                    self.__conn.cast(Pedido.data_pedido, self.__conn.Date) >= self.__conn.cast(self.__data_inicial, self.__conn.Date) if self.__data_inicial else True
                ),
                (
                    self.__conn.cast(Pedido.data_pedido, self.__conn.Date) <= self.__conn.cast(self.__data_final, self.__conn.Date) if self.__data_final else True
                ),
                Clifor.nome.ilike(f"%{self.__nome_usuario}%") if self.__nome_usuario else True,
            )
            .order_by(Pedido.data_pedido.desc())
        )
        
        return query.all()

    def __generate_csv(self, data: list) -> tuple:
        list_donations_canceladas = [
            {
                "id": doacao.id,
                "Nome": doacao.nome,
                "CPF/CNPJ":doacao.cpf_cnpj, 
                "Campanha": doacao.titulo,
                "Data_pedido": doacao.data_pedido.strftime("%d/%m/%Y %H:%M:%S"),
                "Método_pagamento": doacao.metodo_pagamento,
                "Valor": round(doacao.valor_total_pedido, 2),
                "Cancelada_em": doacao.cancelada_em.strftime("%d/%m/%Y %H:%M:%S") if doacao.cancelada_em else None,
            }
            for doacao in data
        ]
        
        return export_excel(list_donations_canceladas, "donations_canceladas")