from datetime import datetime
from flask import request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from models.campanha import Campanha
from models.clifor import Clifor
from models.forma_pagamento import FormaPagamento
from models.pedido import Pedido
from models.processamento_pedido import ProcessamentoPedido
from models.usuario import Usuario
from utils.export_excel import export_excel
from utils.functions import get_current_time, last_day_of_month

class ExportRecurrencesNotPaid:
    def __init__(self, conn: SQLAlchemy):
        self.__conn = conn
        self.__current_date = get_current_time()
        self.__http_request = request.args

        self.__filter_nome = self.__http_request.get("nome")
        self.__data_inicio = self.__http_request.get("data_inicio")
        self.__data_fim = self.__http_request.get("data_fim")
        self.__filter_metodo = self.__http_request.get("forma_pagamento")   
        self.__filter_campanha = self.__http_request.get("campanha_id")   

    def execute(self):
        data = self.__query()
        return self.__generate_csv(data)

    def __query(self):
        ultimo_dia_mes_atual = last_day_of_month(
            self.__current_date.year, self.__current_date.month
        )
        
        processed_orders_subquery = (
            self.__conn.session.query(ProcessamentoPedido.fk_pedido_id)
            .join(Pedido, ProcessamentoPedido.fk_pedido_id == Pedido.id)
            .filter(
                self.__conn.func.month(ProcessamentoPedido.data_processamento) == self.__current_date.month,
                self.__conn.func.year(ProcessamentoPedido.data_processamento) == self.__current_date.year,
                ProcessamentoPedido.status_processamento == 1,
                Pedido.contabilizar_doacao == 1,
                Pedido.periodicidade == 2,
            )
            .subquery()
        )

        subquery_max_processamento = (
            self.__conn.session.query(
                ProcessamentoPedido.fk_pedido_id,
                self.__conn.func.max(ProcessamentoPedido.id).label("max_processamento_id"),
            )
            .group_by(ProcessamentoPedido.fk_pedido_id)
            .subquery()
        )
        
        data_pedido_ajusted = ( self.__conn.func.concat(
                    self.__current_date.year,
                    "-",
                    self.__conn.func.right(
                        self.__conn.func.concat("0", self.__conn.cast(self.__current_date.month, self.__conn.String)),
                        2,
                    ),
                    "-",
                    self.__conn.func.right(
                        self.__conn.func.concat(
                            "0",
                            self.__conn.cast(
                                self.__conn.case(
                                    (
                                        self.__conn.func.day(Pedido.data_pedido) > ultimo_dia_mes_atual,
                                        ultimo_dia_mes_atual,
                                    ),
                                    else_=self.__conn.func.day(Pedido.data_pedido),
                                ),
                                self.__conn.String,
                            ),
                        ),
                        2,
                    ),
                ).label("data_pedido_ajusted")
        )

        query_donations = (
            self.__conn.session.query(
                Pedido.id.label("pedido_id"),
                Clifor.id.label("clifor_id"),
                Clifor.nome,
                Clifor.cpf_cnpj,
                func.format(Pedido.data_pedido, "dd/MM/yyyy HH:mm:ss").label("data_pedido"),
                Pedido.valor_total_pedido,
                data_pedido_ajusted,
                Campanha.titulo.label("nome_campanha"),
                Campanha.descricao,
                FormaPagamento.descricao.label("metodo_pagamento"),
                ProcessamentoPedido.id.label("fk_processamento_pedido_id"),
                func.format(
                    ProcessamentoPedido.data_lembrete_doacao,
                    "dd/MM/yyyy HH:mm:ss",
                ).label("data_lembrete_doacao"),
                Usuario.nome.label("lembrete_enviado_por"),
            )
            .join(
                subquery_max_processamento,
                Pedido.id == subquery_max_processamento.c.fk_pedido_id,
            )
            .join(
                ProcessamentoPedido,
                ProcessamentoPedido.id == subquery_max_processamento.c.max_processamento_id,
            )
            .join(Clifor, Clifor.id == Pedido.fk_clifor_id)
            .join(
                FormaPagamento,
                FormaPagamento.id == Pedido.fk_forma_pagamento_id,
            )
            .join(Campanha, Campanha.id == Pedido.fk_campanha_id)
            .outerjoin(
                Usuario, Usuario.id == ProcessamentoPedido.lembrete_enviado_por
            )
            .filter(
                (
                    self.__conn.func.cast(data_pedido_ajusted, self.__conn.Date).between(
                        self.__conn.func.cast(self.__data_inicio, self.__conn.Date),
                        self.__conn.func.cast(self.__data_fim, self.__conn.Date)
                    ) if self.__data_inicio and self.__data_fim
                    else True
                ),
                Pedido.contabilizar_doacao == 1,
                Pedido.periodicidade == 2,
                Pedido.recorrencia_ativa == 1,
                self.__conn.func.day(Pedido.data_pedido) < self.__conn.func.day(self.__current_date),
                Pedido.id.notin_(processed_orders_subquery),
                (
                    Clifor.nome.ilike(f"%{self.__filter_nome}%")
                    if self.__filter_nome
                    else True
                ),
                (
                    Campanha.id == self.__filter_campanha
                    if self.__filter_campanha
                    else True
                ),
                (
                    FormaPagamento.id == self.__filter_metodo
                    if self.__filter_metodo
                    else True
                ),
            )
            .order_by(self.__conn.desc(data_pedido_ajusted))
        )

        return query_donations

    def __generate_csv(self, data):
        res = [
            {
                "Pedido_id": donation.pedido_id,
                "Clifor_id": donation.clifor_id,
                "Nome": donation.nome,
                "CPF/CNPJ": donation.cpf_cnpj,
                "Data_prevista": datetime.strptime(donation.data_pedido_ajusted, "%Y-%m-%d").strftime("%d/%m/%Y"),
                "Valor": str(round(donation.valor_total_pedido, 2)),
                "Método_pagamento": donation.metodo_pagamento,
                "Campanha": donation.nome_campanha or "",
            } for donation in data
        ]
        
        return export_excel(res, 'doacoes-recorrentes-nao-efetuadas')