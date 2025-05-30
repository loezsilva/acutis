from datetime import datetime

from pydantic import BaseModel, field_validator


def formatar_data_string(
    valor: str,
    formato_entrada: str = '%Y-%m-%d',
    formato_saida: str = '%d/%m/%Y',
) -> str:
    try:
        data = datetime.strptime(valor, formato_entrada)
        return data.strftime(formato_saida)
    except (ValueError, TypeError):
        return valor


class RegistrarDoacaoPixResponse(BaseModel):
    pix_copia_cola: str
    qrcode: str
    data_vencimento: str

    @field_validator('data_vencimento')
    @classmethod
    def formatar_data_vencimento(cls, value: str):
        return formatar_data_string(value)


class RegistrarDoacaoBoletoResponse(BaseModel):
    numero_linha_digitavel: str
    qrcode: str
    nome_cobranca: str
    nosso_numero: str
    dac_titulo: str
    numero_documento_empresa: str
    data_vencimento: str
    valor_doacao: str
    nome_benfeitor: str
    data_emissao: str
    codigo_carteira: str
    codigo_especie: str
    codigo_barras: str
    msg: str

    @field_validator('data_vencimento', 'data_emissao')
    @classmethod
    def formatar_datas(cls, value: str):
        return formatar_data_string(value)
