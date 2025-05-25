from pydantic import BaseModel, Field


class UpdateUserPermissionRequest(BaseModel):
    fk_perfil_id: int = Field(..., description="ID do perfil")
