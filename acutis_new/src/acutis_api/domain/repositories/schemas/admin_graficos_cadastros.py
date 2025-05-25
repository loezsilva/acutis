from datetime import datetime

from pydantic import BaseModel, Field, field_validator


class ResumoQuantidadeRegistrosSchema(BaseModel):
    data_inicio: str = Field(
        None, description='Data de início no formato YYYY-MM-DD'
    )
    data_fim: str = Field(
        None, description='Data de fim no formato YYYY-MM-DD'
    )

    @field_validator('data_inicio', 'data_fim')
    def validate_data(cls, value):
        if value:
            try:
                value = datetime.strptime(value, '%Y-%m-%d').date()
            except ValueError:
                raise ValueError('Data deve estar no formato YYYY-MM-DD')
        return value
