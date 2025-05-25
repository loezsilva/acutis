import pytest

from builder import db as database
from models.agape.instancia_acao_agape import (
    StatusAcaoAgapeEnum,
)
from tests.factories import (
    AcaoAgapeFactory,
    DoacaoAgapeFactory,
    EnderecoFactory,
    EstoqueAgapeFactory,
    FamiliaAgapeFactory,
    InstanciaAcaoAgapeFactory,
    MembroAgapeFactory,
)
from utils.functions import get_current_time
from utils.regex import format_string


@pytest.fixture
def seed_agape_family():
    endereco = EnderecoFactory()
    database.session.add(endereco)
    database.session.flush()

    familia = FamiliaAgapeFactory(fk_endereco_id=endereco.id)
    database.session.add(familia)
    database.session.commit()

    return endereco, familia


@pytest.fixture
def seed_family_deleted():
    endereco = EnderecoFactory()
    database.session.add(endereco)
    database.session.flush()

    familia_agape = FamiliaAgapeFactory(
        fk_endereco_id=endereco.id, deleted_at=get_current_time()
    )
    database.session.add(familia_agape)
    database.session.commit()

    return familia_agape


@pytest.fixture
def seed_agape_member():
    endereco = EnderecoFactory()
    database.session.add(endereco)
    database.session.flush()

    familia = FamiliaAgapeFactory(fk_endereco_id=endereco.id)
    database.session.add(familia)
    database.session.flush()

    membro = MembroAgapeFactory(fk_familia_agape_id=familia.id)
    database.session.add(membro)
    database.session.commit()

    return membro


@pytest.fixture
def seed_agape_family_with_members():
    endereco = EnderecoFactory()
    database.session.add(endereco)
    database.session.flush()

    familia = FamiliaAgapeFactory(fk_endereco_id=endereco.id)
    database.session.add(familia)
    database.session.flush()

    membros = MembroAgapeFactory.build_batch(2, fk_familia_agape_id=familia.id)
    for membro in membros:
        membro.cpf = format_string(membro.cpf, only_digits=True)
    database.session.add_all(membros)
    database.session.commit()

    return familia, membros


@pytest.fixture
def seed_agape_stock():
    stock = EstoqueAgapeFactory()
    database.session.add(stock)
    database.session.commit()

    return stock


@pytest.fixture
def seed_agape_donation():
    endereco = EnderecoFactory()
    database.session.add(endereco)
    database.session.flush()

    familia = FamiliaAgapeFactory(fk_endereco_id=endereco.id)
    database.session.add(familia)
    database.session.flush()

    doacao_agape = DoacaoAgapeFactory(fk_familia_agape_id=familia.id)
    database.session.add(doacao_agape)
    database.session.commit()

    return doacao_agape


@pytest.fixture
def seed_agape_action():
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

    return instancia_acao_agape, endereco


@pytest.fixture
def seed_agape_families():
    enderecos = EnderecoFactory.build_batch(4)
    database.session.add_all(enderecos)
    database.session.flush()

    for endereco in enderecos:
        familia = FamiliaAgapeFactory(fk_endereco_id=endereco.id)
        database.session.add(familia)
    database.session.commit()

    return


@pytest.fixture
def seed_agape_action_instance_already_started():
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
