from pydantic import BaseModel, RootModel


class ResponsePadraoSchema(BaseModel):
    msg: str


class ErroPadraoResponse(RootModel):
    root: list[ResponsePadraoSchema]


class PaginacaoResponse(BaseModel):
    pagina: int
    paginas: int
    total: int
