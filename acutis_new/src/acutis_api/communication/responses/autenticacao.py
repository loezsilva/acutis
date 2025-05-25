import uuid

from pydantic import BaseModel, ConfigDict, EmailStr


class LoginResponse(BaseModel):
    access_token: str | None = None
    refresh_token: str | None = None


class RefreshTokenResponse(BaseModel):
    access_token: str


class VerificarTokenResponse(BaseModel):
    email: str


class UsuarioLogadoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    nome: str | None
    nome_social: str | None
    email: EmailStr | None
    numero_documento: str | None
    data_nascimento: str | None
    telefone: str | None
    sexo: str | None
    foto: str | None
    pais: str | None
    lead_id: uuid.UUID | None
    membro_id: uuid.UUID | None
    criado_em: str | None
    atualizado_em: str | None
    cadastro_atualizado_em: str | None
    ultimo_acesso: str | None
    origem_cadastro: str | None
