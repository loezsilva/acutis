from typing import Optional

from pydantic import BaseModel


class BuscaLandingPageDaCampanhaResponse(BaseModel):
    conteudo: str
    estrutura_json: Optional[str]
