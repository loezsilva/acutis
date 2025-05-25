from flask import request
from flask_sqlalchemy import SQLAlchemy

from models.actions_leads import ActionsLeads
from models.users_imports import UsersImports


class LeadsCount:
    def __init__(self, conn: SQLAlchemy):
        self.__conn = conn
        self.__http_args = request.args
        self.__data_inicio = self.__http_args.get("data_inicio")
        self.__data_fim = self.__http_args.get("data_fim")
        self.__acao = self.__http_args.get("acao")
        
    def execute(self):
        data = self.__query_leads()
        return self.__format_response(data)
    
    def __query_leads(self):
        query_count_leads = (
            self.__conn.session.query(
                self.__conn.func.count(UsersImports.id).label("count"),
                self.__conn.cast(UsersImports.data_criacao, self.__conn.Date).label("data_criacao"),
            )
            .join(ActionsLeads, ActionsLeads.id == UsersImports.origem_cadastro)
            .filter(
                (
                    ActionsLeads.nome.in_(
                        [nome.strip() for nome in self.__acao.split(",")]
                    )
                    if self.__acao
                    else True
                ),
                (
                    UsersImports.data_criacao >= self.__data_inicio
                    if self.__data_inicio
                    else True
                ),
                (
                    UsersImports.data_criacao <= self.__data_fim
                    if self.__data_fim
                    else True
                ),
            )
            .group_by(self.__conn.cast(UsersImports.data_criacao, self.__conn.Date))
            .order_by(self.__conn.cast(UsersImports.data_criacao, self.__conn.Date).asc())
        ).all()
        
        return query_count_leads
    
    def __format_response(self, data: tuple):
        return [
            {
                "count": result.count,
                "data_criacao": result.data_criacao.strftime("%Y-%m-%d"),
            }
            for result in data
        ], 200