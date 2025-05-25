from pydantic import BaseModel, Field


class RenviarEmailVocacionalRequest(BaseModel):
    usuario_vocacional_id: int = Field(..., description="ID vocacional")
