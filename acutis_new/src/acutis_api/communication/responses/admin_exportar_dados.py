from pydantic import BaseModel


class ExportarDadosResponse(BaseModel):
    msg: str
    url: str | None
