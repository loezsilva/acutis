from datetime import date, datetime
from pydantic import BaseModel, validator


class AgapeVoluntarySchema(BaseModel):
    id: int
    nome: str
    data_inicio: str
    data_ultimo_acesso: str | None

    class Config:
        orm_mode = True

    @validator("data_inicio", "data_ultimo_acesso", pre=True)
    def format_data(cls, value):
        if isinstance(value, (datetime, date)):
            return value.strftime("%d/%m/%Y")
        return value


class GetAgapeVolunteersResponse(BaseModel):
    total: int
    page: int
    pages: int
    voluntarios: list[AgapeVoluntarySchema]
