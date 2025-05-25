from flask import request
from flask_sqlalchemy import SQLAlchemy
from typing import List
from models.endereco import Endereco
from models.generais import Generais
from models.usuario import Usuario
from models.clifor import Clifor

class GetAllGenerais:
    def __init__(self, conn: SQLAlchemy):
        self.__conn = conn
        self.__page = request.args.get("page", 1, type=int)
        self.__per_page = request.args.get("per_page", 10, type=int)

    def execute(self):
        count_marechais, count_generais, query_generais = self.__get_generais()
        return self.__format_response(count_marechais, count_generais, query_generais)
    
    def __get_all_filters(self) -> List:
        filter_mapping = {
            "status": lambda value: Generais.status == value,
            "general_id": lambda value: Generais.id == value,
            "nome": lambda value: Clifor.nome.ilike(f"%{value}%"),
            "email": lambda value: Clifor.email.ilike(f"%{value}%"),
            "telefone": lambda value: Clifor.telefone1.ilike(f"%{value}%"),
            "cargo": lambda value: Generais.fk_cargo_id == value,
            "data_cadastro_inicial": lambda value: 
                self.__conn.cast(Generais.created_at, self.__conn.Date)
                >= 
                self.__conn.cast(value, self.__conn.Date),
            "data_cadastro_final": lambda value: 
                self.__conn.cast(Generais.created_at, self.__conn.Date)
                <= 
                self.__conn.cast(value, self.__conn.Date),
            "fk_superior_id": lambda value: Generais.fk_usuario_superior_id == value
        }

        filters = []
        for key, filter_func in filter_mapping.items():
            value = request.args.get(key)
            if value:
                filters.append(filter_func(value))

        return filters
        
    def __get_generais(self):
        generais_query = (
            self.__conn.session.query(Generais, Usuario, Clifor, Endereco)
            .join(Usuario, Generais.fk_usuario_id == Usuario.id)
            .join(Clifor, Clifor.fk_usuario_id == Usuario.id)
            .join(Endereco, Clifor.id == Endereco.fk_clifor_id)
            .filter(*self.__get_all_filters(), Generais.deleted_at == None)
            .order_by(
                self.__conn.func.greatest(Generais.created_at, Generais.updated_at).desc()
            )
        )
        
        count_generais = generais_query.filter(Generais.fk_cargo_id == 2).count()
        count_marechais = generais_query.filter(Generais.fk_cargo_id == 1).count()
        
        paginate = generais_query.paginate(
            page=self.__page, per_page=self.__per_page, error_out=False
        )
        
        return (count_marechais, count_generais, paginate)
    
    def __format_response(self, count_marechais: int, count_generais: int, query_generais):
        CARGOS_MAP = {1: "Marechal", 2: "General"}
        list_generais = []

        for general, usuario, clifor, endereco in query_generais.items:
            superior = None
            if general.fk_usuario_superior_id is not None:
                superior = (
                    self.__conn.session.query(Usuario.nome)
                    .join(Generais, Generais.fk_usuario_id == Usuario.id)
                    .filter(Generais.id == general.fk_usuario_superior_id)
                    .first()
                )

            res = {
                "id": general.id,
                "nome": clifor.nome,
                "telefone": clifor.telefone1,
                "email": clifor.email,
                "created_at": general.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                "rua": endereco.rua,
                "cep": endereco.cep,
                "estado": endereco.estado,
                "complemento": endereco.complemento,
                "bairro": endereco.bairro,
                "numero": endereco.numero,
                "cidade": endereco.cidade,
                "pais": endereco.pais_origem,
                "detalhe_estrangeiro": endereco.detalhe_estrangeiro,
                "quant_membros_grupo": general.quant_membros_grupo,
                "updated_at": general.updated_at.strftime("%Y-%m-%d %H:%M:%S") if general.updated_at != None else None,
                "tempo_de_administrador": general.tempo_de_administrador,
                "link_grupo": general.link_grupo,
                "nome_grupo": general.nome_grupo,
                "status": general.status,
                "usuario_superior": superior.nome if superior else None,
                "cargo": CARGOS_MAP.get(general.fk_cargo_id),
                "usuario_alteracao": general.usuario_alteracao,
            }

            list_generais.append(res)

        paginate = {
            "page": query_generais.page,
            "per_page": self.__per_page,
            "total": query_generais.total,
        }

        response_data = {
            "list": list_generais,
            "paginate": paginate,
            "count_generais": count_generais,
            "count_marechais": count_marechais,
        }
        
        return response_data, 200