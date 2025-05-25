from pydantic import BaseModel


class GetAllProfilesSchema(BaseModel):
    id: int
    nome: str
    status: bool
    super_perfil: bool
    data_criacao: str
    quantidade_usuarios: int

    class Config:
        orm_mode = True


class GetAllProfilesResponse(BaseModel):
    page: int
    total: int
    perfis: list[GetAllProfilesSchema]
