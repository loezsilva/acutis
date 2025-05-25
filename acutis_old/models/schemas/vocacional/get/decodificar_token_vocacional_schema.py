from pydantic import BaseModel, Field


class DecodificarTokenVocacionalResponse(BaseModel):
    nome: str = Field(..., description="Nome vocacional")
    email: str = Field(..., description="Email vocacional")
    etapa: str = Field(..., description="Etapa vocacional")
    status: str = Field(..., description="Status etapa vocacional")
    telefone: str = Field(..., description="Telefonde do vocacional")
    pais: str = Field(..., description="País vocacional")
    fk_usuario_vocacional_id: int = Field(..., description="ID vocacional")

    class Config:
        orm_mode = True
