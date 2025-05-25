from pydantic import BaseModel


class GetAgapeVolunteersPermissionsStatusResponse(BaseModel):
    status: bool
