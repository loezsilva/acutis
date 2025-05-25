from datetime import datetime

from pydantic import BaseModel, field_validator


class RegistrarDoacaoPixResponse(BaseModel):
    pix_copia_cola: str
    qrcode: str
    data_vencimento: str

    @field_validator('data_vencimento')
    @classmethod
    def formatar_data_vencimento(cls, value: str):
        try:
            data_formatada = datetime.strptime(value, '%Y-%m-%d')
            value = data_formatada.strftime('%d/%m/%Y')
        except:  # NOSONAR #noqa
            pass

        return value
