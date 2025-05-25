from pydantic import BaseModel, Field


class ListarCargosOficiaisSchema(BaseModel):
    ordenar_por: str = Field(default='desc', description='desc | asc')
    id: str = Field(None, description='ID cargo oficial')
    nome_cargo: str = Field(None, description='Nome do cargo oficial')
    pagina: int = Field(default=1, description='Página atual')
    por_pagina: int = Field(default=10, description='Quantidade por página')
