from enum import Enum
from pydantic import BaseModel, Field


class EnumAcao(str, Enum):
    APROVAR = "aprovar"
    REPROVAR = "reprovar"


class AtualizarAndamentoVocacionalRequest(BaseModel):
    usuario_vocacional_id: int = Field(..., description="Id do usuário vocacioal")
    acao: EnumAcao = Field(..., description="Ação de aprovar ou recusar")
