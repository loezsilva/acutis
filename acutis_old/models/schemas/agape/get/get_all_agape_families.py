from pydantic import BaseModel, validator

from models.schemas.default import PaginationResponse


class AgapeFamilySchema(BaseModel):
    id: int
    familia: str
    membros: int
    renda: float | None
    cadastrado_em: str = None
    ultimo_recebimento: str = None
    recebimentos: int
    fk_endereco_id: int
    cadastrada_por: str
    observacao: str | None = None
    comprovante_residencia: str | None = None
    fotos_familia: list[str]

    class Config:
        orm_mode = True

    @validator("cadastrada_por", pre=True)
    def format_name(cls, value: str):
        return value.title()


class GetAllAgapeFamiliesResponse(PaginationResponse):
    familias: list[AgapeFamilySchema]
