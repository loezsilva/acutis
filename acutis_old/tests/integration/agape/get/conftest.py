import secrets
import pytest
from builder import db as database

from models.agape.estoque_agape import EstoqueAgape
from models.agape.familia_agape import FamiliaAgape
from models.agape.instancia_acao_agape import StatusAcaoAgapeEnum
from models.agape.item_doacao_agape import ItemDoacaoAgape
from models.agape.item_instancia_agape import ItemInstanciaAgape
from models.agape.membro_agape import MembroAgape
from tests.factories import (
    AcaoAgapeFactory,
    AquisicaoAgapeFactory,
    DoacaoAgapeFactory,
    EnderecoFactory,
    EstoqueAgapeFactory,
    FamiliaAgapeFactory,
    FotoFamiliaAgapeFactory,
    HistoricoMovimentacaoAgapeFactory,
    InstanciaAcaoAgapeFactory,
    ItemDoacaoAgapeFactory,
    ItemInstanciaAgapeFactory,
    MembroAgapeFactory,
    ReciboAgapeFactory,
    UsuarioFactory,
)
from utils.functions import get_current_time


@pytest.fixture
def seed_stock_items():
    items = EstoqueAgapeFactory.build_batch(5)
    database.session.add_all(items)
    database.session.commit()

    return items


@pytest.fixture
def seed_agape_family_members():
    address = EnderecoFactory()
    database.session.add(address)
    database.session.flush()

    family = FamiliaAgapeFactory(fk_endereco_id=address.id)
    database.session.add(family)
    database.session.flush()

    members = MembroAgapeFactory.build_batch(10, fk_familia_agape_id=family.id)
    database.session.add_all(members)
    database.session.commit()

    return members, family


@pytest.fixture
def seed_agape_families_infos():
    address = EnderecoFactory()
    database.session.add(address)
    database.session.flush()

    usuario = UsuarioFactory()
    usuario.password = secrets.token_hex(8)
    database.session.add(usuario)
    database.session.flush()

    family = FamiliaAgapeFactory(
        fk_endereco_id=address.id, status=True, cadastrada_por=usuario.id
    )
    database.session.add(family)
    database.session.flush()

    fotos_familia = FotoFamiliaAgapeFactory.create_batch(2, fk_familia_agape_id=family.id)
    database.session.add_all(fotos_familia)

    members = MembroAgapeFactory.build_batch(10, fk_familia_agape_id=family.id)
    database.session.add_all(members)

    donations = DoacaoAgapeFactory.build_batch(
        5, fk_familia_agape_id=family.id
    )
    database.session.add_all(donations)
    database.session.commit()

    return family


@pytest.fixture
def seed_get_all_agape_actions():
    acoes_agape = AcaoAgapeFactory.build_batch(2)
    database.session.add_all(acoes_agape)
    database.session.flush()

    endereco = EnderecoFactory()
    database.session.add(endereco)
    database.session.flush()

    todas_instancias = []
    for acao in acoes_agape:
        instancias_acao_agape = InstanciaAcaoAgapeFactory.build_batch(
            3,
            fk_acao_agape_id=acao.id,
            fk_endereco_id=endereco.id,
            status=StatusAcaoAgapeEnum.finalizado,
        )
        todas_instancias.extend(instancias_acao_agape)
        database.session.add_all(instancias_acao_agape)
    database.session.commit()

    return acoes_agape


@pytest.fixture
def seed_get_beneficiaries_and_items():
    estoques_agape = EstoqueAgapeFactory.build_batch(2)
    database.session.add_all(estoques_agape)
    database.session.flush()

    endereco = EnderecoFactory()
    database.session.add(endereco)
    database.session.flush()

    familia_agape = FamiliaAgapeFactory(fk_endereco_id=endereco.id)
    database.session.add(familia_agape)
    database.session.flush()

    fotos_familia = FotoFamiliaAgapeFactory.create_batch(3, fk_familia_agape_id=familia_agape.id)
    database.session.add_all(fotos_familia)

    membro_agape = MembroAgapeFactory(
        fk_familia_agape_id=familia_agape.id, cpf="36208571480"
    )
    database.session.add(membro_agape)
    database.session.flush()

    acao_agape = AcaoAgapeFactory()
    database.session.add(acao_agape)
    database.session.flush()

    instancia_acao_agape = InstanciaAcaoAgapeFactory(
        fk_acao_agape_id=acao_agape.id,
        fk_endereco_id=endereco.id,
        status=StatusAcaoAgapeEnum.finalizado,
    )
    database.session.add(instancia_acao_agape)
    database.session.flush()

    itens_instancia_agape = []
    for estoque in estoques_agape:
        item_instancia_agape = ItemInstanciaAgapeFactory(
            fk_instancia_acao_agape_id=instancia_acao_agape.id,
            fk_estoque_agape_id=estoque.id,
        )
        itens_instancia_agape.append(item_instancia_agape)
    database.session.add_all(itens_instancia_agape)
    database.session.flush()

    doacao_agape = DoacaoAgapeFactory(fk_familia_agape_id=familia_agape.id)
    database.session.add(doacao_agape)
    database.session.flush()

    for item_instancia_agape in itens_instancia_agape:
        item_doacao_agape = ItemDoacaoAgapeFactory(
            fk_item_instancia_agape_id=item_instancia_agape.id,
            fk_doacao_agape_id=doacao_agape.id,
        )
        database.session.add(item_doacao_agape)
    database.session.flush()

    recibos = ReciboAgapeFactory.build_batch(
        2, fk_doacao_agape_id=doacao_agape.id
    )
    database.session.add_all(recibos)
    database.session.commit()

    return (
        instancia_acao_agape,
        acao_agape,
        membro_agape,
        familia_agape,
        doacao_agape,
    )


@pytest.fixture
def seed_items_balance_history():
    itens = EstoqueAgapeFactory.build_batch(5)
    database.session.add_all(itens)
    database.session.commit()

    for item in itens:
        historico_movimentacao = HistoricoMovimentacaoAgapeFactory(
            fk_estoque_agape_id=item.id,
        )
        database.session.add(historico_movimentacao)
    database.session.commit()


@pytest.fixture
def seed_many_agape_actions():
    acoes_agape = AcaoAgapeFactory.build_batch(10)
    database.session.add_all(acoes_agape)
    database.session.commit()


@pytest.fixture
def seed_families_statistics():
    database.session.query(MembroAgape).delete()
    database.session.query(FamiliaAgape).delete()
    database.session.commit()

    endereco = EnderecoFactory()
    database.session.add(endereco)
    database.session.flush()

    status_list = [
        True,
        True,
        True,
        True,
        True,
        True,
        False,
        False,
        False,
        False,
    ]
    familias = []

    for status in status_list:
        familia = FamiliaAgapeFactory(
            fk_endereco_id=endereco.id, status=status
        )
        familias.append(familia)
    database.session.add_all(familias)
    database.session.flush()

    for familia in familias:
        membros = MembroAgapeFactory.build_batch(
            5, fk_familia_agape_id=familia.id, renda=1000
        )
        database.session.add_all(membros)

    database.session.commit()


@pytest.fixture
def seed_stock_statistics():
    database.session.query(EstoqueAgape).delete()
    database.session.query(ItemInstanciaAgape).delete()
    database.session.query(ItemDoacaoAgape).delete()
    database.session.commit()

    estoques_agape = EstoqueAgapeFactory.build_batch(10, quantidade=10)
    database.session.add_all(estoques_agape)
    database.session.flush()

    endereco = EnderecoFactory()
    database.session.add(endereco)
    database.session.flush()

    familia_agape = FamiliaAgapeFactory(fk_endereco_id=endereco.id)
    database.session.add(familia_agape)
    database.session.flush()

    acao_agape = AcaoAgapeFactory()
    database.session.add(acao_agape)
    database.session.flush()

    instancia_acao_agape = InstanciaAcaoAgapeFactory(
        fk_acao_agape_id=acao_agape.id,
        fk_endereco_id=endereco.id,
        status=StatusAcaoAgapeEnum.finalizado,
        data_termino=get_current_time(),
    )
    database.session.add(instancia_acao_agape)
    database.session.flush()

    itens_instancia_agape = []
    for estoque in estoques_agape:
        item_instancia_agape = ItemInstanciaAgapeFactory(
            fk_instancia_acao_agape_id=instancia_acao_agape.id,
            fk_estoque_agape_id=estoque.id,
        )
        itens_instancia_agape.append(item_instancia_agape)
    database.session.add_all(itens_instancia_agape)

    doacao_agape = DoacaoAgapeFactory(fk_familia_agape_id=familia_agape.id)
    database.session.add(doacao_agape)
    database.session.flush()

    for item_instancia_agape in itens_instancia_agape:
        item_doacao_agape = ItemDoacaoAgapeFactory(
            fk_item_instancia_agape_id=item_instancia_agape.id,
            fk_doacao_agape_id=doacao_agape.id,
            quantidade=10,
        )
        database.session.add(item_doacao_agape)
    database.session.flush()

    for i in range(5):
        aquisicao_agape = AquisicaoAgapeFactory(
            fk_estoque_agape_id=estoques_agape[i].id,
            quantidade=estoques_agape[i].quantidade,
            created_at=get_current_time(),
        )
        database.session.add(aquisicao_agape)

    database.session.commit()

    return instancia_acao_agape, familia_agape, doacao_agape


@pytest.fixture
def seed_agape_family_income():
    endereco = EnderecoFactory()
    database.session.add(endereco)
    database.session.flush()

    familia = FamiliaAgapeFactory(fk_endereco_id=endereco.id)
    database.session.add(familia)
    database.session.flush()

    membros = MembroAgapeFactory.build_batch(
        5, fk_familia_agape_id=familia.id, renda=1518
    )
    database.session.add_all(membros)
    database.session.commit()

    return familia
