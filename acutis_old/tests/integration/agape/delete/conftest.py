import pytest
from builder import db
from models.agape.instancia_acao_agape import StatusAcaoAgapeEnum
from tests.factories import (
    AcaoAgapeFactory,
    EnderecoFactory,
    EstoqueAgapeFactory,
    InstanciaAcaoAgapeFactory,
    ItemInstanciaAgapeFactory,
)


@pytest.fixture
def seed_agape_action_instance_with_items():
    estoques = EstoqueAgapeFactory.build_batch(3, quantidade=10)
    db.session.add_all(estoques)
    db.session.flush()

    endereco = EnderecoFactory()
    db.session.add(endereco)
    db.session.flush()

    acao_agape = AcaoAgapeFactory()
    db.session.add(acao_agape)
    db.session.flush()

    instancia_acao_agape = InstanciaAcaoAgapeFactory(
        fk_acao_agape_id=acao_agape.id,
        fk_endereco_id=endereco.id,
        status=StatusAcaoAgapeEnum.nao_iniciado,
    )
    db.session.add(instancia_acao_agape)
    db.session.flush()

    for estoque in estoques:
        item_instancia_agape = ItemInstanciaAgapeFactory(
            fk_instancia_acao_agape_id=instancia_acao_agape.id,
            fk_estoque_agape_id=estoque.id,
            quantidade=10,
        )
        db.session.add(item_instancia_agape)
    db.session.commit()

    return estoques, instancia_acao_agape
