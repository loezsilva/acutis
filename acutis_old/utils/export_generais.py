from typing import List, Dict, Any

from flask import request
from flask_sqlalchemy import SQLAlchemy
from models import Generais, Endereco
from datetime import datetime
from utils.export_excel import export_excel

class ExportGenerais:
    def __init__(self, conn: SQLAlchemy) -> None:
        self.__conn = conn

    def execute(self):
        filters = self.__factory_filters()
        data_query = self.__query_generais(filters)
        return self.__format_response(data_query)
    
    def __factory_filters(self):
        mapping_filter = {
            "id": lambda value: Generais.id.like(f"%{value}%"),
            "nome": lambda value: Generais.nome.like(f"%{value}%"),
            "email": lambda value: Generais.email.like(f"%{value}%"),
            "telefone": lambda value: Generais.telefone.like(f"%{value}%"),
            "data_inicio": lambda value: Generais.created_at >= value,
            "data_fim": lambda value: Generais.created_at <= value,
            "cargo": lambda value: Generais.cargo == value,
            "superior": lambda value: Generais.fk_usuario_superior_id == value
        }
        
        filters = []
        
        for key, func in mapping_filter.items():
            value = request.args.get(key)
            if value:
                if key in ["data_inicio", "data_fim"]:
                    value = datetime.strptime(value, "%Y-%m-%d")   
                filters.append(func(value))
        
        return filters
    
        
    def __query_generais(self, filters: list) -> None:

        generais_query = (
            self.__conn.session.query(Generais, Endereco)
            .join(Endereco, Endereco.fk_general_id == Generais.id)
            .filter(*filters, Generais.deleted_at == None)
            .order_by(self.__conn.desc(Generais.created_at))
        )
        
        return generais_query  
    
    def __format_response(self, data: tuple) -> tuple:
        CARGOS_MAP = {1: "Marechal", 2: "General"}
      
        list_generais = []
        
        for general, endereco in data:
            superior = None
            if general.fk_usuario_superior_id is not None:
                superior = (
                    self.__conn.session.query(Generais.nome)
                    .filter(Generais.id == general.fk_usuario_superior_id)
                    .first()
                )
            general = {
                "id": general.id,
                "nome": general.nome,
                "telefone": general.telefone,
                "email": general.email,
                "created_at": general.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                "rua": endereco.rua,
                "cep": endereco.cep,
                "estado": endereco.estado,
                "complemento": endereco.complemento,
                "bairro": endereco.bairro,
                "numero": endereco.numero,
                "cidade": endereco.cidade,
                "quant_membros_grupo": general.quant_membros_grupo,
                "updated_at": general.updated_at,
                "tempo_de_administrador": general.tempo_de_administrador,
                "link_grupo": general.link_grupo,
                "nome_grupo": general.nome_grupo,
                "usuario_superior": superior.nome if superior else None,
                "cargo": CARGOS_MAP[general.cargo],
            }
            
            list_generais.append(general)
            
        return export_excel(list_generais, 'lista-generais')