from typing import List
from pydantic import BaseModel


class GetProfileByIdSchema(BaseModel):
    id: int
    nome: str
    status: bool
    super_perfil: bool
    data_criacao: str

    class Config:
        orm_mode = True


class GetPermissionsMenuProfileSchema(BaseModel):
    fk_menu_id: int
    nome_menu: str
    acessar: bool
    criar: bool
    editar: bool
    deletar: bool

    class Config:
        orm_mode = True


class GetProfileByIdResponse(BaseModel):
    perfil: GetProfileByIdSchema
    menus: List[GetPermissionsMenuProfileSchema]
