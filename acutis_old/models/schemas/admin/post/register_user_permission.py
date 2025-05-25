from pydantic import BaseModel, Field


class RegisterUserPermissionRequest(BaseModel):
    fk_usuario_id: int = Field(..., gt=0, description="ID do usuário")
    fk_perfil_id: int = Field(..., gt=0, description="ID do perfil")
