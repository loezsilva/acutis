from pydantic import BaseModel, EmailStr, Field


class ForgotPasswordRequest(BaseModel):
    email: EmailStr = Field(..., description="Email do usuário")
    url_redirect: str = Field(default = "/login/reset-password", description="Url de redirecionamento")
