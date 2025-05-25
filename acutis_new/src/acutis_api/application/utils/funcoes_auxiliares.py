import io
import re
import uuid
from base64 import b64decode
from calendar import monthrange
from datetime import date, datetime
from enum import Enum
from typing import Union

import pandas as pd
from email_validator import EmailNotValidError, validate_email
from itsdangerous import BadSignature, SignatureExpired, URLSafeTimedSerializer
from validate_docbr import CNPJ, CPF

from acutis_api.domain.services.schemas.gateway_pagamento import (
    TipoDocumentoEnum,
)
from acutis_api.exception.errors.bad_request import HttpBadRequestError
from acutis_api.exception.errors.unauthorized import HttpUnauthorizedError
from acutis_api.exception.errors.unprocessable_entity import (
    HttpUnprocessableEntityError,
)
from acutis_api.exception.errors_handler import errors_handler
from acutis_api.infrastructure.services.factories import file_service_factory
from acutis_api.infrastructure.settings import settings


class TokenSaltEnum(str, Enum):
    ativar_conta = 'active_account_confirmation'
    recuperar_senha = 'reset_password_confirmation'


def gerar_token(objeto: dict, salt: str) -> str:
    if not isinstance(objeto, dict):
        raise TypeError('O argumento passado deve ser do tipo DICT.')

    serializer = URLSafeTimedSerializer(settings.SECRET_KEY)
    token = serializer.dumps(objeto, salt=salt)

    return token


def verificar_token(token: str, salt: str, max_age=24 * 60 * 60):
    try:
        serializer = URLSafeTimedSerializer(settings.SECRET_KEY)

        obj = serializer.loads(token, salt=salt, max_age=max_age)

        return obj
    except SignatureExpired:
        raise HttpUnauthorizedError('Token expirado.')
    except BadSignature:
        raise HttpUnauthorizedError('Token inválido.')


def validar_base64(base64: str):
    if 'data:' not in base64:
        raise HttpUnprocessableEntityError('Ops, o Base64 enviado é inválido.')

    try:
        _, base64 = base64.split(',')
        base64 = b64decode(base64, validate=True)
    except Exception:
        raise HttpUnprocessableEntityError(
            'Ops, não foi possível decodificar o Base64.'
        )


def decodificar_base64_para_arquivo(
    base64: str,
) -> tuple[io.BytesIO, str]:
    extensao, base64 = base64.split(',')
    extensao = extensao.split('/')[1].split(';')[0]
    nome_arquivo = f'{str(uuid.uuid4())}.{extensao}'

    arquivo_binario = b64decode(base64)
    return (io.BytesIO(arquivo_binario), nome_arquivo)


def quantidade_meses_entre_datas(data_inicio, data_fim):
    resultado = (data_fim.year - data_inicio.year) * 12 + (
        data_fim.month - data_inicio.month
    )

    return resultado if resultado > 0 else 1


def quantidade_dias_entre_datas(data_inicio, data_fim):
    diferenca = data_fim - data_inicio
    return abs(diferenca.days)


def valida_cpf_cnpj(
    cpf_cnpj: str, tipo_documento: str, gerar_excesao: bool = True
) -> str:
    cpf_cnpj = ''.join(filter(str.isdigit, cpf_cnpj))

    if tipo_documento == 'cpf':
        cpf = CPF()
        if not cpf.validate(cpf_cnpj):
            if gerar_excesao:
                raise HttpBadRequestError('CPF inválido!')
            return ''

    if tipo_documento == 'cnpj':
        cnpj = CNPJ()
        if not cnpj.validate(cpf_cnpj):
            if gerar_excesao:
                raise HttpBadRequestError('CNPJ inválido!')
            return ''

    return cpf_cnpj


def valida_nome(nome: str) -> tuple[bool, str]:
    if nome is None:
        return False, 'Você deve inserir um nome.'

    name_regex = r'^[a-zA-ZáÁâÂãÃàÀéÉêÊèÈíÍóÓôÔõÕúÚùÙçÇ\s]+$'

    if not bool(re.match(name_regex, nome)):
        return False, f'O nome {nome} inserido possui caracteres inválidos.'

    return True, nome


def valida_email(
    email: str, verificar_entregabilidade: bool, verificar_dominio: bool
) -> tuple[bool, str]:
    if not email:
        return False, 'Você deve inserir um email.'

    try:
        emailinfo = validate_email(
            email, check_deliverability=verificar_entregabilidade
        )

        email = emailinfo.normalized
    except EmailNotValidError:
        return False, 'O email inserido é inválido.'

    if verificar_dominio:
        ALLOWED_DOMAINS = [
            'gmail.com',
            'outlook.com',
            'hotmail.com',
            'icloud.com',
            'me.com',
            'apple.com',
            'headers.com.br',
            'institutohesed.org.br',
            'yahoo.com',
        ]
        email_regex = (
            r'^[a-zA-Z0-9._%+-]+@(' + '|'.join(ALLOWED_DOMAINS) + r')$'
        )
        if not bool(re.match(email_regex, email)):
            return False, 'O domínio do email inserido não é permitido.'

    return True, email


def formatar_string(texto: str | None) -> str | None:
    # Substituir "ç" por "c"
    texto = re.sub('[ç]', 'c', texto)

    # Remover acentos
    texto = re.sub('[áàãâä]', 'a', texto)
    texto = re.sub('[éèêë]', 'e', texto)
    texto = re.sub('[íìîï]', 'i', texto)
    texto = re.sub('[óòõôö]', 'o', texto)
    texto = re.sub('[úùûü]', 'u', texto)

    # Remover pontos e sinais
    texto = re.sub('[.!?,:;ºª]', '', texto)
    texto = re.sub('[_]', ' ', texto)

    return texto


def definir_tipo_documento(numero_documento: str) -> TipoDocumentoEnum | str:
    tamanho_cpf = 11
    tamanho_cnpj = 14

    tipo_documento_map = {
        tamanho_cpf: TipoDocumentoEnum.CPF,
        tamanho_cnpj: TipoDocumentoEnum.CNPJ,
    }

    return tipo_documento_map.get(
        len(numero_documento), 'identidade_estrangeira'
    )


def calcular_data_vencimento(data: date) -> str:
    ano = data.year
    mes = data.month
    dia = data.day

    if mes == 12:
        proximo_mes = 1
        ano += 1
    else:
        proximo_mes = mes + 1

    _, dias_no_proximo_mes = monthrange(ano, proximo_mes)

    if mes == 1 and dia > 28 and proximo_mes == 2:
        dia_vencimento = 28
    else:
        dia_vencimento = min(dia, dias_no_proximo_mes)

    data_vencimento = datetime(ano, proximo_mes, dia_vencimento)

    return data_vencimento.strftime('%Y-%m-%d')


def transforma_string_para_data(value):
    try:
        # Tenta RFC 1123
        return datetime.strptime(value, '%a, %d %b %Y %H:%M:%S GMT')
    except (ValueError, TypeError):
        return None


def remove_caracteres_ascii(texto):
    if isinstance(texto, str):
        texto_sanitizado = re.sub(
            r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]', '', texto
        )
    return texto_sanitizado


def exporta_csv(data, nome_arquivo):
    s3_client = file_service_factory()
    df = pd.DataFrame(data)
    output = io.BytesIO()

    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Dados')

    output.seek(0)

    object_name = f'{nome_arquivo}.xlsx'

    try:
        s3_client.salvar_arquivo(
            output,
            object_name,
            extra_args={
                'ContentType': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'  # noqa
            },
        )

        public_url = s3_client.buscar_url_arquivo(object_name)
        return {'url': public_url}

    except Exception as exc:
        raise errors_handler(exc)

def calcular_idade(data_nascimento: Union[str, date], formato: str = "%Y-%m-%d") -> int:
    """
    Calcula a idade com base na data de nascimento fornecida.

    Args:
        data_nascimento (Union[str, date]): A data de nascimento no formato date ou string.
        formato (str): O formato esperado caso a data seja string. Padrão: "%Y-%m-%d".

    Returns:
        int: Idade em anos completos.

    Raises:
        ValueError: Se a data estiver no futuro ou for inválida.
    """
    if isinstance(data_nascimento, str):
        try:
            data_nascimento = datetime.strptime(data_nascimento, formato).date()
        except ValueError as e:
            raise ValueError(f"Data inválida: {e}")

    hoje = date.today()
    if data_nascimento > hoje:
        raise ValueError("A data de nascimento não pode estar no futuro.")

    idade = hoje.year - data_nascimento.year
    if (hoje.month, hoje.day) < (data_nascimento.month, data_nascimento.day):
        idade -= 1

    return idade