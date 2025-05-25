from pydantic import BaseModel


class PaginacaoQuery(BaseModel):
    pagina: int = 1
    por_pagina: int = 10
