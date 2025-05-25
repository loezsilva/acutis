from pydantic import BaseModel, Field


class ListarRecorrenciasCanceladasQuery(BaseModel):
    page: int = Field(default=1, description="Pagina atual")
    per_page: int = Field(default=10, description="Quantidade por página")
    campanha_id: int = Field(None, description="ID campanha")
    nome_usuario: str = Field(None, description="Nome do usuário")
    data_inicial: str = Field(None, description="Data inicial")
    data_final: str = Field(None, description="Data final")