from typing import Optional
from pydantic import BaseModel


class UpdateProfilePermissionsRequest(BaseModel):
    fk_menu_id: int
    acessar: Optional[bool]
    criar: Optional[bool]
    editar: Optional[bool]
    deletar: Optional[bool]
