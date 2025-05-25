from typing import List, Optional
from pydantic import BaseModel


class GetActionDetailsByIdResponse(BaseModel):
    id: int
    nome: Optional[str]
    titulo: Optional[str]
    descricao: Optional[str]
    background: Optional[str]
    banner: Optional[str]
    status: Optional[bool]
    preenchimento_foto: Optional[bool]
    label_foto: Optional[str]
    sorteio: Optional[bool]
    total_leads: Optional[int]
    criado_em: Optional[str]
    cadastrado_por: Optional[str]
    sorteados: Optional[List[str]]
    sorteador: Optional[str]
    data_sorteio: Optional[str]
