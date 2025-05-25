from pydantic import BaseModel, Field, SecretStr, validator


class ChangePasswordRequest(BaseModel):
    old_password: SecretStr = Field(
        ...,
        min_length=8,
        max_length=16,
        description="Senha atual do usuário",
    )
    new_password: SecretStr = Field(
        ...,
        min_length=8,
        max_length=16,
        description="Nova senha do usuário",
    )

    @validator("new_password")
    def validar_password(cls, value: SecretStr):
        senha = value.get_secret_value()
        if not any(char.isdigit() for char in senha):
            raise ValueError("A senha deve conter pelo menos um número.")
        if not any(char.isupper() for char in senha):
            raise ValueError("A senha deve conter pelo menos uma letra maiúscula.")
        if not any(char.islower() for char in senha):
            raise ValueError("A senha deve conter pelo menos uma letra minúscula.")
        if not any(char in "@$!%*#?&" for char in senha):
            raise ValueError("A senha deve conter pelo menos um caractere especial.")
        return value
