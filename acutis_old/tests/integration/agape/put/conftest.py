import pytest

from builder import db as database
from tests.factories import (
    AcaoAgapeFactory,
    EnderecoFactory,
    EstoqueAgapeFactory,
    InstanciaAcaoAgapeFactory,
    ItemInstanciaAgapeFactory,
    StatusAcaoAgapeEnum,
)


@pytest.fixture
def seed_agape_action_instance_not_started():
    endereco = EnderecoFactory()
    database.session.add(endereco)
    database.session.flush()

    acao_agape = AcaoAgapeFactory()
    database.session.add(acao_agape)
    database.session.flush()

    instancia_acao_agape = InstanciaAcaoAgapeFactory(
        fk_acao_agape_id=acao_agape.id,
        fk_endereco_id=endereco.id,
        status=StatusAcaoAgapeEnum.nao_iniciado,
    )
    database.session.add(instancia_acao_agape)
    database.session.commit()

    return instancia_acao_agape


@pytest.fixture
def seed_agape_action_instance_started():
    endereco = EnderecoFactory()
    database.session.add(endereco)
    database.session.flush()

    acao_agape = AcaoAgapeFactory()
    database.session.add(acao_agape)
    database.session.flush()

    instancia_acao_agape = InstanciaAcaoAgapeFactory(
        fk_acao_agape_id=acao_agape.id,
        fk_endereco_id=endereco.id,
        status=StatusAcaoAgapeEnum.em_andamento,
    )
    database.session.add(instancia_acao_agape)
    database.session.commit()

    return instancia_acao_agape


@pytest.fixture
def seed_agape_action_with_instance_already_started():
    endereco = EnderecoFactory()
    database.session.add(endereco)
    database.session.flush()

    acao_agape = AcaoAgapeFactory()
    database.session.add(acao_agape)
    database.session.flush()

    instancia_acao_agape_nao_iniciado = InstanciaAcaoAgapeFactory(
        fk_acao_agape_id=acao_agape.id,
        fk_endereco_id=endereco.id,
        status=StatusAcaoAgapeEnum.nao_iniciado,
    )
    database.session.add(instancia_acao_agape_nao_iniciado)

    instancia_acao_agape_em_andamento = InstanciaAcaoAgapeFactory(
        fk_acao_agape_id=acao_agape.id,
        fk_endereco_id=endereco.id,
        status=StatusAcaoAgapeEnum.em_andamento,
    )
    database.session.add(instancia_acao_agape_em_andamento)
    database.session.commit()

    return instancia_acao_agape_nao_iniciado


@pytest.fixture
def seed_agape_action_instance_ending():
    estoque_agape = EstoqueAgapeFactory(quantidade=20)
    database.session.add(estoque_agape)
    database.session.flush()

    endereco = EnderecoFactory()
    database.session.add(endereco)
    database.session.flush()

    acao_agape = AcaoAgapeFactory()
    database.session.add(acao_agape)
    database.session.flush()

    instancia_acao_agape = InstanciaAcaoAgapeFactory(
        fk_acao_agape_id=acao_agape.id,
        fk_endereco_id=endereco.id,
        status=StatusAcaoAgapeEnum.em_andamento,
    )
    database.session.add(instancia_acao_agape)
    database.session.flush()

    item_instancia_agape = ItemInstanciaAgapeFactory(
        fk_instancia_acao_agape_id=instancia_acao_agape.id,
        fk_estoque_agape_id=estoque_agape.id,
        quantidade=30,
    )
    database.session.add(item_instancia_agape)
    database.session.commit()

    return instancia_acao_agape, item_instancia_agape, estoque_agape


@pytest.fixture
def seed_update_agape_action():
    itens = EstoqueAgapeFactory.build_batch(5, quantidade=10)
    database.session.add_all(itens)
    database.session.flush()

    endereco = EnderecoFactory()
    database.session.add(endereco)
    database.session.flush()

    acao_agape = AcaoAgapeFactory()
    database.session.add(acao_agape)
    database.session.flush()

    instancia_acao_agape = InstanciaAcaoAgapeFactory(
        fk_acao_agape_id=acao_agape.id,
        fk_endereco_id=endereco.id,
        status=StatusAcaoAgapeEnum.nao_iniciado,
    )
    database.session.add(instancia_acao_agape)
    database.session.flush()

    for i in range(3):
        item_instancia_agape = ItemInstanciaAgapeFactory(
            fk_instancia_acao_agape_id=instancia_acao_agape.id,
            fk_estoque_agape_id=itens[i].id,
        )
        database.session.add(item_instancia_agape)
    database.session.commit()

    return instancia_acao_agape, itens
