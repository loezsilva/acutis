from datetime import date
import json
from pydantic import BaseModel, EmailStr, Field, SecretStr, constr, root_validator, validator
from typing import Optional
from spectree import BaseFile
from models.schemas.users.post.register_user_full import DocumentTypesEnum, GendersEnum, RedirectPagesEnum, RegisterUserAddressSchema, RegisterUserFullDataSchema


class RegisterGeneralRequest(BaseModel):
    fk_usuario_id: int
    quant_membros_grupo: int = Field(..., gt=0, le=1024)
    nome_grupo: constr(min_length=5, max_length=25)  # type: ignore
    link_grupo: constr(min_length=48, max_length=48)  # type: ignore
    tempo_de_administrador: Optional[str]


class FormGeneralWordPressRequest(BaseModel):  
    image: Optional[BaseFile] = Field(None, description="Imagem do usuário")
    fk_usuario_superior_id: int = Field(..., description="ID de general superior")
    pagina_redirecionamento: Optional[RedirectPagesEnum] = Field(
        RedirectPagesEnum.PRINCIPAL,
        description="Pagina onde o usuário será redirecionado após ativar a conta pelo link recebido por email.",
    )
    pais: Optional[str] = Field(
        None, min_length=3, max_length=50, description="Nome do país"
    )
    usuario: RegisterUserFullDataSchema
    endereco: RegisterUserAddressSchema

    @root_validator(pre=True)
    def validate_data(cls, values):
        if "usuario" in values and isinstance(values["usuario"], str):
            try:
                values["usuario"] = json.loads(values["usuario"])
            except json.JSONDecodeError:
                raise ValueError("O campo 'usuario' deve ser um JSON válido.")

        if "endereco" in values and isinstance(values["endereco"], str):
            try:
                values["endereco"] = json.loads(values["endereco"])
            except json.JSONDecodeError:
                raise ValueError("O campo 'endereco' deve ser um JSON valido.")
        return values