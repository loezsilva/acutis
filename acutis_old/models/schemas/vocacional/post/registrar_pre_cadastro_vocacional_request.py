from pydantic import BaseModel, Field

from models.vocacional.usuario_vocacional import VocationalGendersEnum


class RegistrarPreCadastroRequest(BaseModel):
    nome: str = Field(
        ...,
        min_length=3,
        max_length=255,
        description="Nome do vocacionado",
        strip_whitespace=True,
    )
    email: str = Field(..., description="E-mail do vocacionado", strip_whitespace=True)
    telefone: str = Field(
        ..., description="Telefone do vocacionado", strip_whitespace=True
    )
    genero: VocationalGendersEnum = Field(
        ..., description="Gênero do vocacionado", strip_whitespace=True
    )
    pais: str = Field(..., description="País do vocacionado", strip_whitespace=True)
