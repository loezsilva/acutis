from datetime import datetime
from io import BytesIO
from http import HTTPStatus
import json
from faker import Faker
from flask.testing import FlaskClient
import pytest
from werkzeug.datastructures import FileStorage

faker = Faker("pt-BR")


@pytest.fixture
def mock_image_file():
    return BytesIO(b"fake image data"), "test_image.jpg"


def test_register_ficha_vocacional_successo(
    test_client: FlaskClient, seed_cadastro_vocacional_aprovado, mock_image_file
):
    pre_cadastro, cadastro_vocacional = seed_cadastro_vocacional_aprovado

    ficha_vocacional_data = {
        "fk_usuario_vocacional_id": pre_cadastro.id,
        "motivacao_instituto": "Sestãoociedade.",
        "motivacao_admissao_vocacional": "De melhor através da minha vocação.",
        "referencia_conhecimento_instituto": "Conheci o instituto através de um amigo que já participou do processo vocacional.",
        "identificacao_instituto": "Me identifico com a forma como o instituto promove a justiça social e o desenvolvimento comunitário.",
        "testemunho_conversao": "Minha conversão começou após uma experiência profunda durante um retiro espiritual, onde senti um chamado pa",
        "escolaridade": "Ensino Superior Completo",
        "profissao": "Professor",
        "cursos": "Licenciatura em História, Pós-graduação em Educação Inclusiva",
        "rotina_diaria": "Acordo às 6h, vou para a escola onde leciono, à tarde estudo e à noite participo de grupos de oração",
        "aceitacao_familiar": "Minha família apoia minha decisão, embora tenham suas preocupações.",
        "estado_civil": "Solteiro(a)",
        "motivo_divorcio": None,
        "seminario_realizado_em": "2023-03-15",
        "deixou_religiao_anterior_em": "2020-05-20",
        "remedio_controlado_inicio": "2019-08-10",
        "remedio_controlado_termino": "2021-02-15",
        "sacramentos": ["eucaristia", "crisma", "teste"],
        "descricao_problema_saude": "Tive um período de depressão, mas atualmente estou bem e sem necessidade de medicação.",
    }

    mock_file, filename = mock_image_file
    file_storage = FileStorage(
        stream=mock_file, filename=filename, content_type="image/jpeg"
    )

    data = {
        "ficha_vocacional": json.dumps(ficha_vocacional_data),
        "foto_vocacional": (file_storage, filename),
    }

    response = test_client.post(
        "/vocacional/registrar-ficha-vocacional",
        data=data,
        content_type="multipart/form-data",
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json["msg"] == "Ficha vocacional preenchida com sucesso."


def test_register_ficha_vocacional_bad_request_error(
    test_client: FlaskClient, seed_cadastro_vocacional_aprovado, mock_image_file
):
    pre_cadastro, cadastro_vocacional = seed_cadastro_vocacional_aprovado

    ficha_vocacional_data = {
        "fk_usuario_vocacional_id": pre_cadastro.id,
        "motivacao_instituto": "Sestãoociedade.",
    }

    mock_file, filename = mock_image_file
    file_storage = FileStorage(
        stream=mock_file, filename=filename, content_type="image/jpeg"
    )

    data = {
        "ficha_vocacional": json.dumps(ficha_vocacional_data),
        "foto_vocacional": (file_storage, filename),
    }

    response = test_client.post(
        "/vocacional/registrar-ficha-vocacional",
        data=data,
        content_type="multipart/form-data",
    )

    assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
    assert (
        response.json["error"]
        == "Erro interno no servidor, tente novamente mais tarde!"
    )


def test_register_ficha_vocacional_pre_cadastro_nao_encontrado(
    test_client: FlaskClient, seed_cadastro_vocacional_aprovado, mock_image_file
):
    pre_cadastro, cadastro_vocacional = seed_cadastro_vocacional_aprovado

    ficha_vocacional_data = {
        "fk_usuario_vocacional_id": 2000,
        "motivacao_instituto": "Sestãoociedade.",
        "motivacao_admissao_vocacional": "De melhor através da minha vocação.",
        "referencia_conhecimento_instituto": "Conheci o instituto através de um amigo que já participou do processo vocacional.",
        "identificacao_instituto": "Me identifico com a forma como o instituto promove a justiça social e o desenvolvimento comunitário.",
        "testemunho_conversao": "Minha conversão começou após uma experiência profunda durante um retiro espiritual, onde senti um chamado pa",
        "escolaridade": "Ensino Superior Completo",
        "profissao": "Professor",
        "cursos": "Licenciatura em História, Pós-graduação em Educação Inclusiva",
        "rotina_diaria": "Acordo às 6h, vou para a escola onde leciono, à tarde estudo e à noite participo de grupos de oração",
        "aceitacao_familiar": "Minha família apoia minha decisão, embora tenham suas preocupações.",
        "estado_civil": "Solteiro(a)",
        "motivo_divorcio": None,
        "seminario_realizado_em": "2023-03-15",
        "deixou_religiao_anterior_em": "2020-05-20",
        "remedio_controlado_inicio": "2019-08-10",
        "remedio_controlado_termino": "2021-02-15",
        "sacramentos": ["eucaristia", "crisma", "teste"],
        "descricao_problema_saude": "Tive um período de depressão, mas atualmente estou bem e sem necessidade de medicação.",
    }

    mock_file, filename = mock_image_file
    file_storage = FileStorage(
        stream=mock_file, filename=filename, content_type="image/jpeg"
    )

    data = {
        "ficha_vocacional": json.dumps(ficha_vocacional_data),
        "foto_vocacional": (file_storage, filename),
    }

    response = test_client.post(
        "/vocacional/registrar-ficha-vocacional",
        data=data,
        content_type="multipart/form-data",
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert (
        response.json["error"]
        == "Usuário vocacional não encontrado, é necessário preencher o pré cadastro para seguir."
    )


def test_register_ficha_vocacional_image_nao_enviada(
    test_client: FlaskClient, seed_cadastro_vocacional_aprovado
):
    pre_cadastro, cadastro_vocacional = seed_cadastro_vocacional_aprovado

    ficha_vocacional_data = {
        "fk_usuario_vocacional_id": pre_cadastro.id,
        "motivacao_instituto": "Sestãoociedade.",
        "motivacao_admissao_vocacional": "De melhor através da minha vocação.",
        "referencia_conhecimento_instituto": "Conheci o instituto através de um amigo que já participou do processo vocacional.",
        "identificacao_instituto": "Me identifico com a forma como o instituto promove a justiça social e o desenvolvimento comunitário.",
        "testemunho_conversao": "Minha conversão começou após uma experiência profunda durante um retiro espiritual, onde senti um chamado pa",
        "escolaridade": "Ensino Superior Completo",
        "profissao": "Professor",
        "cursos": "Licenciatura em História, Pós-graduação em Educação Inclusiva",
        "rotina_diaria": "Acordo às 6h, vou para a escola onde leciono, à tarde estudo e à noite participo de grupos de oração",
        "aceitacao_familiar": "Minha família apoia minha decisão, embora tenham suas preocupações.",
        "estado_civil": "Solteiro(a)",
        "motivo_divorcio": None,
        "seminario_realizado_em": "2023-03-15",
        "deixou_religiao_anterior_em": "2020-05-20",
        "remedio_controlado_inicio": "2019-08-10",
        "remedio_controlado_termino": "2021-02-15",
        "sacramentos": ["eucaristia", "crisma", "teste"],
        "descricao_problema_saude": "Tive um período de depressão, mas atualmente estou bem e sem necessidade de medicação.",
    }

    data = {
        "ficha_vocacional": json.dumps(ficha_vocacional_data),
        "foto_vocacional": None,
    }

    response = test_client.post(
        "/vocacional/registrar-ficha-vocacional",
        data=data,
        content_type="multipart/form-data",
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json["error"] == "Arquivo da foto vocacional não fornecido."


def test_register_ficha_vocacional_ja_registrado(
    test_client: FlaskClient, mock_image_file, seed_ficha_vocacional
):

    pre_cadastro, cadastro_vocacional, new_ficha_vocacional = seed_ficha_vocacional

    ficha_vocacional_data = {
        "fk_usuario_vocacional_id": pre_cadastro.id,
        "motivacao_instituto": "Sestãoociedade.",
        "motivacao_admissao_vocacional": "De melhor através da minha vocação.",
        "referencia_conhecimento_instituto": "Conheci o instituto através de um amigo que já participou do processo vocacional.",
        "identificacao_instituto": "Me identifico com a forma como o instituto promove a justiça social e o desenvolvimento comunitário.",
        "testemunho_conversao": "Minha conversão começou após uma experiência profunda durante um retiro espiritual, onde senti um chamado pa",
        "escolaridade": "Ensino Superior Completo",
        "profissao": "Professor",
        "cursos": "Licenciatura em História, Pós-graduação em Educação Inclusiva",
        "rotina_diaria": "Acordo às 6h, vou para a escola onde leciono, à tarde estudo e à noite participo de grupos de oração",
        "aceitacao_familiar": "Minha família apoia minha decisão, embora tenham suas preocupações.",
        "estado_civil": "Solteiro(a)",
        "motivo_divorcio": None,
        "seminario_realizado_em": "2023-03-15",
        "deixou_religiao_anterior_em": "2020-05-20",
        "remedio_controlado_inicio": "2019-08-10",
        "sacramentos": ["eucaristia", "crisma", "teste"],
        "remedio_controlado_termino": "2021-02-15",
        "descricao_problema_saude": "Tive um período de depressão, mas atualmente estou bem e sem necessidade de medicação.",
    }

    mock_file, filename = mock_image_file
    file_storage = FileStorage(
        stream=mock_file, filename=filename, content_type="image/jpeg"
    )

    data = {
        "ficha_vocacional": json.dumps(ficha_vocacional_data),
        "foto_vocacional": (file_storage, filename),
    }

    response = test_client.post(
        "/vocacional/registrar-ficha-vocacional",
        data=data,
        content_type="multipart/form-data",
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json["error"] == "Fichal vocacional já preenchida."


def test_register_ficha_vocacional_data_ficha_nao_encontrado(
    test_client: FlaskClient, seed_cadastro_vocacional_aprovado, mock_image_file
):
    pre_cadastro, cadastro_vocacional = seed_cadastro_vocacional_aprovado

    mock_file, filename = mock_image_file
    file_storage = FileStorage(
        stream=mock_file, filename=filename, content_type="image/jpeg"
    )

    data = {"foto_vocacional": (file_storage, filename)}

    response = test_client.post(
        "/vocacional/registrar-ficha-vocacional",
        data=data,
        content_type="multipart/form-data",
    )

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
