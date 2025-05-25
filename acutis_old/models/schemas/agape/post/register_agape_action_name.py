from pydantic import BaseModel, constr


class RegisterAgapeActionNameRequest(BaseModel):
    nome: constr(strip_whitespace=True, min_length=3)  # type: ignore
