from datetime import date, datetime, timedelta
import logging
import re
from typing import Optional
import unicodedata
import uuid
import pytz
import io
import os
from base64 import b64decode
from openpyxl import Workbook
from werkzeug.datastructures import FileStorage

from PIL import Image, UnidentifiedImageError

from exceptions.error_types.http_bad_request import BadRequestError
from exceptions.error_types.http_unprocessable_entity import HttpUnprocessableEntity
from exceptions.errors_handler import errors_handler
from exceptions.exception_upload_image import UploadImageException
from email_validator import EmailNotValidError, validate_email
from services.factories import file_service_factory
from templates.email_templates import (
    thanks_for_donation,
)
from utils.send_email import send_email
from datetime import datetime
import pytz
from dateutil.relativedelta import relativedelta


def get_current_time():
    tz = pytz.timezone("America/Fortaleza")
    return datetime.now(tz)


def calculate_days_interval(first_date: datetime) -> int:
    """Calcula o número de dias entre a data atual e a primeira data informada."""

    if first_date.tzinfo is None:
        first_date = pytz.UTC.localize(first_date)

    current = get_current_time()
    difference = current - first_date

    return difference.days


def calculate_months_interval(first_date: datetime) -> int:
    """Calcula o número de meses entre a data atual e a primeira data informada."""

    if first_date.tzinfo is None:
        first_date = pytz.UTC.localize(first_date)

    diff = relativedelta(get_current_time(), first_date)
    return diff.years * 12 + diff.months


def upload_image(image_data: str, filename: str):
    try:
        format_data, image_data = image_data.split(",")
        image_ext = (format_data.split("/")[1]).split(";")[0]
        filename = f"{filename}.{image_ext}"

        image_bytes = b64decode(image_data)
        try:
            image = Image.open(io.BytesIO(image_bytes))
        except UnidentifiedImageError:
            logging.error(
                f"UnidentifiedImageError: {str(type(err))} - {str(err)}"
            )
            raise UnidentifiedImageError(
                "Identificamos um problema ao cadastrar sua foto, por favor tente outro arquivo."
            )

        if image.mode == "RGBA":
            image = image.convert("RGB")

        compressed_image_io = io.BytesIO()
        image.save(compressed_image_io, format=image_ext, quality=15)
        compressed_image_io.seek(0)

        compressed_image_filename = os.path.join("storage/images/", filename)
        os.makedirs(os.path.dirname(compressed_image_filename), exist_ok=True)
        with open(compressed_image_filename, "wb") as f:
            f.write(compressed_image_io.read())

        return filename
    except UploadImageException as err:
        logging.error(
            f"ERRO NO UPLOAD DA IMAGEM: {str(type((err)))} - {str(err)}"
        )
        raise UploadImageException(
            "Ocorreu um erro ao realizar o upload da imagem."
        )


def send_thanks_for_donation(campanha, nome_usuario, email_usuario):
    try:
        s3_client = file_service_factory()

        foto_campanha = s3_client.get_public_url(campanha.filename)

        html = thanks_for_donation(
            nome_usuario, campanha.titulo, foto_campanha
        )

        send_email(
            "Instituto Hesed - Agradecemos Sua Doação", email_usuario, html, 9
        )
    except Exception as e:
        return errors_handler(e)


def is_valid_email(
    email: Optional[str], check_deliverability: bool, check_valid_domain: bool
) -> str | None:
    if not email:
        return None

    try:
        emailinfo = validate_email(
            email, check_deliverability=check_deliverability
        )

        email = emailinfo.normalized
    except EmailNotValidError:
        raise BadRequestError("O email inserido é inválido.")

    if check_valid_domain:
        ALLOWED_DOMAINS = [
            "gmail.com",
            "outlook.com",
            "hotmail.com",
            "icloud.com",
            "me.com",
            "apple.com",
            "headers.com.br",
            "institutohesed.org.br",
            "yahoo.com",
        ]
        email_regex = (
            r"^[a-zA-Z0-9._%+-]+@(" + "|".join(ALLOWED_DOMAINS) + r")$"
        )
        if bool(re.match(email_regex, email)) == False:
            raise BadRequestError(
                "O domínio do email inserido não é permitido."
            )

    return email.lower()


def is_valid_name(nome: str, title: bool = True) -> Optional[str]:
    if nome is None:
        return nome

    name_regex = r"^[a-zA-ZáÁâÂãÃàÀéÉêÊèÈíÍóÓôÔõÕúÚùÙçÇ\s]+$"
    if bool(re.match(name_regex, nome)) == False:
        raise BadRequestError(
            f"O nome {nome} inserido possui caracteres inválidos."
        )

    return nome.title() if title else nome


def is_valid_birthdate(data_nascimento: Optional[date]) -> date:
    if data_nascimento is None:
        return data_nascimento
    if data_nascimento >= get_current_time().date():
        raise BadRequestError("A data de nascimento inserida é inválida.")

    return data_nascimento


def calculate_age(birth_date: str | date) -> int:
    if isinstance(birth_date, str):
        birth_date = datetime.strptime(birth_date, "%d/%m/%Y")

    today = get_current_time().date()
    age = today.year - birth_date.year
    if (today.month, today.day) < (birth_date.month, birth_date.day):
        age -= 1
    return age


def mask_email(email: str) -> str:
    nome, dominio = email.split("@")
    _, extensao = dominio.rsplit(".", 1)

    dominio_oculto = "****"

    return f"{nome}@{dominio_oculto}.{extensao}"


def normalize_text(text: str) -> str:
    normalized = unicodedata.normalize("NFKD", text)

    stripped = normalized.encode("ascii", "ignore").decode("ascii")

    return stripped.lower().strip()


def convert_data_into_xlsx(
    *,
    data: list,
    headers: list = None,
    save_into_bucket: bool = True,
    filename: str | None = None,
) -> io.BytesIO | str:
    if headers is None:
        headers = [column.name for column in data[0].__table__.columns]

    wb = Workbook()
    ws = wb.active
    ws.append(headers)

    for row in data:
        processed_row = []
        for value in row:
            if isinstance(value, datetime):
                processed_row.append(value.strftime("%d/%m/%Y %H:%M"))
            elif isinstance(value, date):
                processed_row.append(value.strftime("%d/%m/%Y"))
            elif value is None:
                processed_row.append("")
            else:
                processed_row.append(value)
        ws.append(processed_row)

    buffer = io.BytesIO()
    wb.save(buffer)
    buffer.seek(0)

    if save_into_bucket:
        if filename is None:
            filename = f"{str(uuid.uuid4())}.xlsx"
        else:
            filename = (
                f"{filename}.xlsx"
                if not filename.endswith(".xlsx")
                else filename
            )

        s3_client = file_service_factory()
        s3_client.upload_fileobj(
            buffer,
            filename,
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )

        return s3_client.get_public_url(filename)

    return buffer


def last_day_of_month(year: int, month: int) -> int:
    if month == 12:
        next_month = 1
        next_year = year + 1
    else:
        next_month = month + 1
        next_year = year

    return (date(next_year, next_month, 1) - timedelta(days=1)).day

def decodificar_base64_para_arquivo(base64_str: str) -> FileStorage:
    prefixo, dados_base64 = _extrair_dados_base64(base64_str)
    _validar_base64(dados_base64)

    extensao = _extrair_extensao(prefixo)
    nome_arquivo = f"{uuid.uuid4()}.{extensao}"
    arquivo_binario = b64decode(dados_base64)

    return FileStorage(io.BytesIO(arquivo_binario), nome_arquivo)

def _extrair_dados_base64(base64_str: str) -> tuple[str, str]:
    if not base64_str.startswith("data:") or ',' not in base64_str:
        raise HttpUnprocessableEntity("Ops, o Base64 enviado é inválido.")

    try:
        prefixo, dados = base64_str.split(",", 1)
        return prefixo, dados
    except ValueError:
        raise HttpUnprocessableEntity("Ops, o Base64 enviado é inválido.")

def _validar_base64(dados_base64: str):
    try:
        b64decode(dados_base64, validate=True)
    except Exception:
        raise HttpUnprocessableEntity("Ops, não foi possível decodificar o Base64.")

def _extrair_extensao(prefixo: str) -> str:
    try:
        return prefixo.split("/")[1].split(";")[0]
    except IndexError:
        raise HttpUnprocessableEntity("Não foi possível extrair a extensão do arquivo.")