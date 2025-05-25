from typing import Optional
from pydantic import BaseModel, EmailStr, Field


class GetAllUsersPresencesFilters(BaseModel):
    page: Optional[int] = Field(
        default=1,
        gt=0,
        description="Declara a página em que deseja buscar as informações",
    )
    per_page: Optional[int] = Field(
        default=10, gt=0, description="Declara a quantidade de itens por página"
    )
    filtro_usuario_id: Optional[int] = Field(
        description="Campo para filtrar pelo ID do usuário"
    )
    filtro_campanha_id: Optional[int] = Field(
        description="Campo para filtrar pelo ID da campanha"
    )
    filtro_numero_documento: Optional[str] = Field(
        default="", description="Campo para filtrar pelo número de documento"
    )
    filtro_nome_usuario: Optional[str] = Field(
        default="", description="Campo para filtrar pelo nome do usuário"
    )
    filtro_nome_campanha: Optional[str] = Field(
        default="", description="Campo para filtrar pelo nome da campanha"
    )
    filtro_email: Optional[EmailStr] = Field(
        default="", description="Campo para filtrar pelo email do usuário"
    )


class GetAllUsersPresencesSchema(BaseModel):
    id: int = Field(..., description="ID do usuário")
    nome: Optional[str] = Field(description="Nome do usuário")
    email: Optional[EmailStr] = Field(description="Email do usuário")
    numero_documento: Optional[str] = Field(
        description="Número de documento do usuário"
    )
    presencas: Optional[int] = Field(description="Quantidade de presenças do usuário")
    foto: Optional[str] = Field(description="Foto do usuário")
    fk_campanha_id: Optional[int] = Field(description="ID da campanha")
    nome_campanha: Optional[str] = Field(description="Nome da campanha")


class GetAllUsersPresencesResponse(BaseModel):
    page: int
    total: int
    usuarios: list[GetAllUsersPresencesSchema]
