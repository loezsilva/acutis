from pydantic import BaseModel, Field

class CreateTypeEmailForm(BaseModel):
    tipo_email: str = Field(..., description="Descricao do tipo email")