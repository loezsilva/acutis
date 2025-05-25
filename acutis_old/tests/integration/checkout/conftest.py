import pytest
from builder import db
from tests.factories import UsuarioFactory
from tests.integration.checkout.factories import CampanhaFactory, CliforFactory, PedidoRecorrenteCanceladoFactory, PedidoRecorrenteFactory, ProcessamentoPedidoFactory


@pytest.fixture
def seed_pedido_recorrente():
    
    usuario = UsuarioFactory()
    
    db.session.add(usuario)
    db.session.flush()
    
    clifor = CliforFactory(
        fk_usuario_id=usuario.id
    )
    
    db.session.add(clifor)
    db.session.flush()
    
    campanha = CampanhaFactory()
    
    db.session.add(campanha)
    db.session.flush()
    
    pedido = PedidoRecorrenteFactory(fk_clifor_id=clifor.id, fk_campanha_id=campanha.id, usuario_criacao=usuario.id)
    
    db.session.add(pedido)
    db.session.flush()
    
    create_processamento_pedido = ProcessamentoPedidoFactory(
        fk_pedido_id=pedido.id, usuario_criacao=usuario.id, fk_clifor_id= clifor.id
    )
    db.session.add(create_processamento_pedido)
    db.session.commit()
    
    return pedido, create_processamento_pedido

@pytest.fixture
def seed_pedido_recorrente_cancelado():
    
    usuario = UsuarioFactory()
    
    db.session.add(usuario)
    db.session.flush()
    
    clifor = CliforFactory(
        fk_usuario_id=usuario.id
    )
    
    db.session.add(clifor)
    db.session.flush()
    
    campanha = CampanhaFactory()
    
    db.session.add(campanha)
    db.session.flush()
    
    pedido_cancelado = PedidoRecorrenteCanceladoFactory(fk_clifor_id=clifor.id, fk_campanha_id=campanha.id, usuario_criacao=usuario.id)
    
    db.session.add(pedido_cancelado)
    db.session.flush()
    
    create_processamento_pedido = ProcessamentoPedidoFactory(
        fk_pedido_id=pedido_cancelado.id, usuario_criacao=usuario.id, fk_clifor_id= clifor.id
    )
    db.session.add(create_processamento_pedido)
    db.session.commit()
    
    return pedido_cancelado, create_processamento_pedido
