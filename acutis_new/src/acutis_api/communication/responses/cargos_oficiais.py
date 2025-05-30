import uuid

from pydantic import BaseModel, ConfigDict, RootModel


class RegistrarNovoCargoficialResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    nome_cargo: str


class ListaDeCargosOficiaisSchema(BaseModel):
    id: uuid.UUID
    nome_cargo: str


class ListaDeCargosOficiaisResponse(RootModel):
    root: list[ListaDeCargosOficiaisSchema]


class ObterTotalCadastrosCargoOficialSchema(BaseModel):
    nome_cargo: str
    total_cadastros_cargo: int


class ObterTotalCadastrosCargoOficialResponse(RootModel):
    root: list[ObterTotalCadastrosCargoOficialSchema]
