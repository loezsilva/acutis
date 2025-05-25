import json
from http import HTTPStatus
from io import BytesIO

import pytest
from faker import Faker
from flask.testing import FlaskClient
from werkzeug.datastructures import FileStorage

faker = Faker('pt-BR')


@pytest.fixture
def mock_image_file():
    return BytesIO(b'fake image data'), 'test_image.jpg'


def test_registrar_ficha_vocacional_successo(
    client: FlaskClient, seed_cadastro_vocacional_aprovado, mock_image_file
):
    pre_cadastro, _ = seed_cadastro_vocacional_aprovado()

    ficha_vocacional_data = {
        'fk_usuario_vocacional_id': str(pre_cadastro.id),
        'motivacao_instituto': 'Sestãoociedade.',
        'motivacao_admissao_vocacional': 'De melhor através da minha vocação.',
        'referencia_conhecimento_instituto': 'Conheci o instituto através de \
            um amigo que já participou do processo vocacional.',
        'identificacao_instituto': 'Me identifico com a forma como o instituto\
            promove a justiça social e o desenvolvimento comunitário.',
        'testemunho_conversao': 'Minha conversão começou após uma experiência \
            profunda durante um retiro espiritual, onde senti um chamado pa',
        'escolaridade': 'Ensino Superior Completo',
        'profissao': 'Professor',
        'cursos': 'Licenciatura em História, Pós-graduação em Educação \
            Inclusiva',
        'rotina_diaria': 'Acordo às 6h, vou para a escola onde leciono, \
            à tarde estudo e à noite participo de grupos de oração',
        'aceitacao_familiar': 'Minha família apoia minha decisão, \
            embora tenham suas preocupações.',
        'estado_civil': 'Divorciado(a)',
        'motivo_divorcio': 'Não me adaptei ao estilo de vida do meu \
            ex-cônjuge.',
        'seminario_realizado_em': '2023-03-15',
        'deixou_religiao_anterior_em': '2020-05-20',
        'remedio_controlado_inicio': '2019-08-10',
        'sacramentos': ['eucaristia', 'crisma'],
        'remedio_controlado_termino': '2021-02-15',
        'descricao_problema_saude': 'Tive um período de depressão, \
            mas atualmente estou bem e sem necessidade de medicação.',
    }

    mock_file, filename = mock_image_file
    file_storage = FileStorage(
        stream=mock_file, filename=filename, content_type='image/jpeg'
    )

    data = {
        'ficha_vocacional': json.dumps(ficha_vocacional_data),
        'foto_vocacional': (file_storage, filename),
    }

    response = client.post(
        '/api/vocacional/registrar-ficha-vocacional',
        data=data,
        content_type='multipart/form-data',
    )

    assert response.json == {'msg': 'Ficha vocacional preenchida com sucesso.'}
    assert response.status_code == HTTPStatus.CREATED


def test_registrar_ficha_vocacional_pre_cadastro_nao_encontrado(
    client: FlaskClient, seed_cadastro_vocacional_aprovado, mock_image_file
):
    _, _ = seed_cadastro_vocacional_aprovado()

    ficha_vocacional_data = {
        'fk_usuario_vocacional_id': '57F2F4B9-178C-4B4D-A228-288535C6CA79',
        'motivacao_instituto': 'Sestãoociedade.',
        'motivacao_admissao_vocacional': 'De melhor através da minha vocação.',
        'referencia_conhecimento_instituto': 'Conheci o instituto através de \
            um amigo que já participou do processo vocacional.',
        'identificacao_instituto': 'Me identifico com a forma como o instituto\
            promove a justiça social e o desenvolvimento comunitário.',
        'testemunho_conversao': 'Minha conversão começou após uma experiência \
            profunda durante um retiro espiritual, onde senti um chamado pa',
        'escolaridade': 'Ensino Superior Completo',
        'profissao': 'Professor',
        'cursos': 'Licenciatura em História, Pós-graduação em Educação \
            Inclusiva',
        'rotina_diaria': 'Acordo às 6h, vou para a escola onde leciono, \
            à tarde estudo e à noite participo de grupos de oração',
        'aceitacao_familiar': 'Minha família apoia minha decisão, \
            embora tenham suas preocupações.',
        'estado_civil': 'Divorciado(a)',
        'motivo_divorcio': 'Não me adaptei ao estilo de vida do meu \
            ex-cônjuge.',
        'seminario_realizado_em': '2023-03-15',
        'deixou_religiao_anterior_em': '2020-05-20',
        'remedio_controlado_inicio': '2019-08-10',
        'sacramentos': ['eucaristia', 'crisma'],
        'remedio_controlado_termino': '2021-02-15',
        'descricao_problema_saude': 'Tive um período de depressão, \
            mas atualmente estou bem e sem necessidade de medicação.',
    }

    mock_file, filename = mock_image_file
    file_storage = FileStorage(
        stream=mock_file, filename=filename, content_type='image/jpeg'
    )

    data = {
        'ficha_vocacional': json.dumps(ficha_vocacional_data),
        'foto_vocacional': (file_storage, filename),
    }

    response = client.post(
        '/api/vocacional/registrar-ficha-vocacional',
        data=data,
        content_type='multipart/form-data',
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json == [
        {
            'msg': 'Usuário vocacional não encontrado, \
                        é necessário preencher o pré cadastro para seguir.'
        }
    ]


def test_registrar_ficha_vocacional_ja_registrado(
    client: FlaskClient, mock_image_file, seed_ficha_vocacional
):
    pre_cadastro, _, _ = seed_ficha_vocacional()
    ficha_vocacional_data = {
        'fk_usuario_vocacional_id': str(pre_cadastro.id),
        'motivacao_instituto': 'Sestãoociedade.',
        'motivacao_admissao_vocacional': 'De melhor através da minha vocação.',
        'referencia_conhecimento_instituto': 'Conheci o instituto através de \
            um amigo que já participou do processo vocacional.',
        'identificacao_instituto': 'Me identifico com a forma como o instituto\
            promove a justiça social e o desenvolvimento comunitário.',
        'testemunho_conversao': 'Minha conversão começou após uma experiência \
            profunda durante um retiro espiritual, onde senti um chamado pa',
        'escolaridade': 'Ensino Superior Completo',
        'profissao': 'Professor',
        'cursos': 'Licenciatura em História, Pós-graduação em Educação \
            Inclusiva',
        'rotina_diaria': 'Acordo às 6h, vou para a escola onde leciono, \
            à tarde estudo e à noite participo de grupos de oração',
        'aceitacao_familiar': 'Minha família apoia minha decisão, \
            embora tenham suas preocupações.',
        'estado_civil': 'Divorciado(a)',
        'motivo_divorcio': 'Não me adaptei ao estilo de vida do meu \
            ex-cônjuge.',
        'seminario_realizado_em': '2023-03-15',
        'deixou_religiao_anterior_em': '2020-05-20',
        'remedio_controlado_inicio': '2019-08-10',
        'sacramentos': ['eucaristia', 'crisma'],
        'remedio_controlado_termino': '2021-02-15',
        'descricao_problema_saude': 'Tive um período de depressão, \
            mas atualmente estou bem e sem necessidade de medicação.',
    }

    mock_file, filename = mock_image_file
    file_storage = FileStorage(
        stream=mock_file, filename=filename, content_type='image/jpeg'
    )

    data = {
        'ficha_vocacional': json.dumps(ficha_vocacional_data),
        'foto_vocacional': (file_storage, filename),
    }

    response = client.post(
        '/api/vocacional/registrar-ficha-vocacional',
        data=data,
        content_type='multipart/form-data',
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json == [{'msg': 'Fichal vocacional já preenchida.'}]


def test_registrar_ficha_vocacional_json_invalido(
    client: FlaskClient, seed_cadastro_vocacional_aprovado
):
    pre_cadastro, _ = seed_cadastro_vocacional_aprovado()

    ficha_vocacional_data = {
        'fk_usuario_vocacional_id': str(pre_cadastro.id),
        'motivacao_instituto': 'Sestãoociedade.',
        'motivacao_admissao_vocacional': 'De melhor através da minha vocação.',
        'referencia_conhecimento_instituto': 'Conheci o instituto através de \
            um amigo que já participou do processo vocacional.',
        'identificacao_instituto': 'Me identifico com a forma como o instituto\
            promove a justiça social e o desenvolvimento comunitário.',
        'testemunho_conversao': 'Minha conversão começou após uma experiência \
            profunda durante um retiro espiritual, onde senti um chamado pa',
        'escolaridade': 'Ensino Superior Completo',
        'profissao': 'Professor',
        'cursos': 'Licenciatura em História, Pós-graduação em Educação \
            Inclusiva',
        'rotina_diaria': 'Acordo às 6h, vou para a escola onde leciono, \
            à tarde estudo e à noite participo de grupos de oração',
        'aceitacao_familiar': 'Minha família apoia minha decisão, \
            embora tenham suas preocupações.',
        'estado_civil': 'Divorciado(a)',
        'motivo_divorcio': 'Não me adaptei ao estilo de vida do meu \
            ex-cônjuge.',
        'seminario_realizado_em': '2023-03-15',
        'deixou_religiao_anterior_em': '2020-05-20',
        'remedio_controlado_inicio': '2019-08-10',
        'sacramentos': ['eucaristia', 'crisma'],
        'remedio_controlado_termino': '2021-02-15',
        'descricao_problema_saude': 'Tive um período de depressão, \
            mas atualmente estou bem e sem necessidade de medicação.',
    }

    data = {
        'ficha_vocacional': ficha_vocacional_data,
    }

    response = client.post(
        '/api/vocacional/registrar-ficha-vocacional',
        data=data,
        content_type='multipart/form-data',
    )

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert response.json[0]['msg'] == (
        'O campo "ficha_vocacional" deve ser um JSON válido.'
    )
