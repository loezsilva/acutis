from pydantic import BaseModel


class GetAllActionsNamesSchema(BaseModel):
    id: int
    nome: str

    class Config:
        orm_mode = True


class GetAllActionsNamesResponse(BaseModel):
    acoes: list[GetAllActionsNamesSchema]
