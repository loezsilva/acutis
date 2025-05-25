from pydantic import BaseModel


class GetUserPresenceByIdResponse(BaseModel):
    qtd_campanhas_registradas: int
    qtd_presencas_registradas: int
