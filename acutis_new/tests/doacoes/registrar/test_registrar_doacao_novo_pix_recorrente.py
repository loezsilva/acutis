import uuid
from http import HTTPStatus
from unittest.mock import patch

from flask.testing import FlaskClient

from acutis_api.application.use_cases.doacoes.registrar import (
    RegistrarDoacaoNovoPixRecorrenteUseCase,
)
from acutis_api.application.utils.funcoes_auxiliares import gerar_token
from acutis_api.communication.responses.doacoes import (
    RegistrarDoacaoPixResponse,
)
from acutis_api.domain.entities.pagamento_doacao import FormaPagamentoEnum
from acutis_api.domain.entities.processamento_doacao import (
    ProcessamentoDoacao,
    StatusProcessamentoEnum,
)
from acutis_api.domain.services.schemas.gateway_pagamento import (
    BuscarPagamentoPixResponse,
)
from acutis_api.infrastructure.extensions import database
from acutis_api.infrastructure.services.itau import ItauPixService


@patch.object(ItauPixService, 'criar_pagamento_pix')
def test_registrar_doacao_novo_pix_recorrente_sucesso(
    mock_criar_pagamento_pix,
    client: FlaskClient,
    seed_campanha_doacao,
    seed_dados_doacao,
):
    pix_copia_cola = str(uuid.uuid4())
    qrcode = str(uuid.uuid4())
    transacao_id = uuid.uuid4().hex

    mock_criar_pagamento_pix.return_value = BuscarPagamentoPixResponse(
        pix_copia_cola=pix_copia_cola,
        qrcode=qrcode,
        transacao_id=transacao_id,
    )

    campanha = seed_campanha_doacao
    lead, doacao = seed_dados_doacao(
        campanha=campanha,
        status_doacao=StatusProcessamentoEnum.pendente,
    )

    processamento_doacao = ProcessamentoDoacao(
        fk_pagamento_doacao_id=doacao.pagamento_doacao.id,
        forma_pagamento=FormaPagamentoEnum.pix,
    )
    database.session.add(processamento_doacao)
    database.session.commit()

    usuario_objeto = {
        'processamento_doacao_id': str(processamento_doacao.id),
        'numero_documento': lead.membro.numero_documento,
        'nome': lead.nome,
        'chave_pix': campanha.campanha_doacao.chave_pix,
    }

    token = gerar_token(
        objeto=usuario_objeto, salt='4eed38b8-b906-4dc1-bdd6-d219b722d958'
    )

    response = client.post(
        f'/api/doacoes/pagamento/pix/recorrencia?token={token}'
    )

    assert response.status_code == HTTPStatus.CREATED
    assert RegistrarDoacaoPixResponse.model_validate(response.json)


@patch.object(ItauPixService, 'buscar_pagamento_pix')
def test_buscar_doacao_novo_pix_recorrente_sucesso(
    mock_buscar_pagamento_pix,
    client: FlaskClient,
    seed_campanha_doacao,
    seed_dados_doacao,
):
    pix_copia_cola = str(uuid.uuid4())
    qrcode = str(uuid.uuid4())
    transacao_id = uuid.uuid4().hex

    mock_buscar_pagamento_pix.return_value = BuscarPagamentoPixResponse(
        pix_copia_cola=pix_copia_cola,
        qrcode=qrcode,
        transacao_id=transacao_id,
    )

    campanha = seed_campanha_doacao
    lead, doacao = seed_dados_doacao(
        campanha=campanha,
        status_doacao=StatusProcessamentoEnum.pendente,
    )

    processamento_doacao = ProcessamentoDoacao(
        fk_pagamento_doacao_id=doacao.pagamento_doacao.id,
        forma_pagamento=FormaPagamentoEnum.pix,
        codigo_transacao=str(uuid.uuid4()),
    )
    database.session.add(processamento_doacao)
    database.session.commit()

    usuario_objeto = {
        'processamento_doacao_id': str(processamento_doacao.id),
        'numero_documento': lead.membro.numero_documento,
        'nome': lead.nome,
        'chave_pix': campanha.campanha_doacao.chave_pix,
    }

    token = gerar_token(
        objeto=usuario_objeto, salt='4eed38b8-b906-4dc1-bdd6-d219b722d958'
    )

    response = client.post(
        f'/api/doacoes/pagamento/pix/recorrencia?token={token}'
    )

    assert response.status_code == HTTPStatus.CREATED
    assert RegistrarDoacaoPixResponse.model_validate(response.json)


@patch.object(RegistrarDoacaoNovoPixRecorrenteUseCase, 'execute')
def test_registrar_doacao_novo_pix_recorrente_erro_interno_servidor(
    mock_target, client: FlaskClient
):
    token = str(uuid.uuid4())
    mock_target.side_effect = Exception('Erro interno no servidor')

    response = client.post(
        f'/api/doacoes/pagamento/pix/recorrencia?token={token}'
    )

    assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
    assert response.json == [{'msg': 'Erro interno no servidor.'}]
