import pytest
from builder import db

from models.agape.instancia_acao_agape import (
    StatusAcaoAgapeEnum,
)
from tests.factories import (
    AcaoAgapeFactory,
    EnderecoFactory,
    EstoqueAgapeFactory,
    FamiliaAgapeFactory,
    InstanciaAcaoAgapeFactory,
    ItemInstanciaAgapeFactory,
)


@pytest.fixture
def base_agape_action():
    """Fixture base que cria uma ação ágape com itens de estoque"""

    def _create_agape(num_items=2, quantidade=30):
        acao_agape = AcaoAgapeFactory()
        db.session.add(acao_agape)
        db.session.flush()

        itens_estoque = EstoqueAgapeFactory.build_batch(
            num_items, quantidade=quantidade
        )

        db.session.add_all(itens_estoque)
        db.session.commit()

        return acao_agape, itens_estoque

    return _create_agape


@pytest.fixture
def seed_register_agape_action(base_agape_action):
    """Cria uma ação ágape padrão com 2 itens de estoque"""
    return base_agape_action()


@pytest.fixture
def seed_register_agape_action_conflict(base_agape_action):
    """Cria uma ação ágape com endereço e instância em andamento"""
    endereco = EnderecoFactory()
    db.session.add(endereco)
    db.session.flush()

    acao_agape, itens_estoque = base_agape_action()

    instancia_acao_agape = InstanciaAcaoAgapeFactory(
        fk_endereco_id=endereco.id,
        fk_acao_agape_id=acao_agape.id,
        status=StatusAcaoAgapeEnum.em_andamento,
    )
    db.session.add(instancia_acao_agape)
    db.session.commit()

    return acao_agape, itens_estoque


@pytest.fixture
def seed_register_agape_action_insufficient_stock(base_agape_action):
    """Cria uma ação ágape com estoque insuficiente"""
    return base_agape_action(num_items=1, quantidade=2)


@pytest.fixture
def seed_register_agape_donation(base_agape_action):
    endereco = EnderecoFactory()
    db.session.add(endereco)
    db.session.flush()

    familia_agape = FamiliaAgapeFactory(
        fk_endereco_id=endereco.id, status=True
    )
    db.session.add(familia_agape)

    acao_agape, itens_estoque = base_agape_action(num_items=1)

    instancia_acao_agape = InstanciaAcaoAgapeFactory(
        fk_endereco_id=endereco.id,
        fk_acao_agape_id=acao_agape.id,
        status=StatusAcaoAgapeEnum.em_andamento,
    )
    db.session.add(instancia_acao_agape)
    db.session.flush()

    item_instancia_agape = ItemInstanciaAgapeFactory(
        fk_instancia_acao_agape_id=instancia_acao_agape.id,
        fk_estoque_agape_id=itens_estoque[0].id,
        quantidade=20,
    )
    db.session.add(item_instancia_agape)
    db.session.commit()

    return familia_agape, instancia_acao_agape, item_instancia_agape


@pytest.fixture
def seed_family_inactive():
    endereco = EnderecoFactory()
    db.session.add(endereco)
    db.session.flush()

    familia_agape = FamiliaAgapeFactory(
        fk_endereco_id=endereco.id, status=False
    )
    db.session.add(familia_agape)
    db.session.commit()

    return familia_agape


@pytest.fixture
def seed_agape_action_instance():
    endereco = EnderecoFactory()
    db.session.add(endereco)
    db.session.flush()

    familia_agape = FamiliaAgapeFactory(
        fk_endereco_id=endereco.id, status=True
    )
    db.session.add(familia_agape)

    acao_agape = AcaoAgapeFactory()
    db.session.add(acao_agape)
    db.session.flush()

    instancia_acao_agape = InstanciaAcaoAgapeFactory(
        fk_endereco_id=endereco.id,
        fk_acao_agape_id=acao_agape.id,
        status=StatusAcaoAgapeEnum.nao_iniciado,
    )
    db.session.add(instancia_acao_agape)
    db.session.commit()

    return familia_agape, instancia_acao_agape
