from typing import List, Optional
from pydantic import BaseModel, Field


class GetAllUsersPermissionsQuery(BaseModel):
    page: Optional[int] = Field(
        1,
        gt=0,
        description="Declara a página em que deseja buscar as informações",
    )
    per_page: Optional[int] = Field(
        10,
        gt=0,
        description="Declara a quantidade de itens por página",
    )
    filtro_fk_perfil_id: Optional[int] = Field(
        description="Campo para filtrar pelo ID do perfil"
    )
    filtro_nome_email_cpf: Optional[str] = Field(
        default="", description="Campo para filtrar pelo nome, email ou CPF"
    )


class GetAllUsersPermissionsSchema(BaseModel):
    id: int = Field(..., description="ID da permissão de usuário")
    fk_usuario_id: int = Field(..., description="ID do usuário")
    fk_perfil_id: int = Field(..., description="ID do perfil")
    nome_usuario: str = Field(..., description="Nome do usuário")
    status_usuario: bool = Field(..., description="Status do usuário")
    data_criacao_usuario: str = Field(
        ..., description="Data de criação do usuário"
    )

    class Config:
        orm_mode = True


class GetAllUsersPermissionsResponse(BaseModel):
    page: int
    total: int
    permissoes_usuarios: List[GetAllUsersPermissionsSchema] = Field(
        ..., description="Lista de permissões de usuários"
    )
