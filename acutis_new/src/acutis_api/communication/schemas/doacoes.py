import uuid

from pydantic import BaseModel


class PixRecorrenteTokenSchema(BaseModel):
    processamento_doacao_id: uuid.UUID
    numero_documento: str
    nome: str
    chave_pix: str
