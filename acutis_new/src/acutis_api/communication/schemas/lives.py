import uuid

from pydantic import BaseModel, Field


class CriarCanalSchema(BaseModel):
    tag: str = Field(
        ..., min_length=3, max_length=50, description='Nome do canal (tag)'
    )
    rede_social: str = Field(
        ..., min_length=2, max_length=20, description='Rede social do canal'
    )
    fk_campanha_id: uuid.UUID | None = Field(
        None, description='ID da campanha'
    )

    class Config:
        from_attributes = True
