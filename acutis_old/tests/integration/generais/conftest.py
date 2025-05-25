from faker import Faker
import pytest 
from builder import db
from models.generais import Generais
from models.usuario import Usuario
from models.clifor import Clifor
from models.endereco import Endereco
from models.pedido import Pedido
from models.perfil import Perfil
from models.permissao_usuario import PermissaoUsuario
from models.forma_pagamento import FormaPagamento
from datetime import datetime

faker = Faker("pt_BR")


@pytest.fixture(scope="function")
def seed_general_not_aproved():
    nome = faker.name()
    email = faker.email(domain="gmail.com")
    cpf = faker.cpf()
    user = Usuario(
        nome=nome,
        email=email,
        country="brasil",
        password="sem@Senha123",
        status=True,
    )
    db.session.add(user)
    db.session.flush()

    clifor = Clifor(
        fk_usuario_id=user.id,
        nome=nome,
        email=email,
        cpf_cnpj=cpf,
        telefone1="11987456789",
        data_nascimento=datetime.now().date(),
        usuario_criacao=user.id,
    )
    db.session.add(clifor)
    db.session.flush()

    address = Endereco(fk_clifor_id=clifor.id, usuario_criacao=user.id)
    db.session.add(address)

    perfil = Perfil.query.filter_by(nome="Benfeitor").first()

    user_permission = PermissaoUsuario(
        fk_usuario_id=user.id, fk_perfil_id=perfil.id, usuario_criacao=0
    )
    db.session.add(user_permission)

    forma_pagamento = FormaPagamento.query.filter_by(descricao="Pix").first()

    pedido = Pedido(
        fk_clifor_id=clifor.id,
        anonimo=False,
        fk_forma_pagamento_id=forma_pagamento.id,
        periodicidade=1,
        usuario_criacao=0,
    )
    db.session.add(pedido)
    
    general = Generais(
        id=faker.random_number(digits=3),
        fk_cargo_id=2,
        fk_usuario_id=user.id,
        quant_membros_grupo=12,
        created_at=datetime.now(),
        link_grupo="https://chat.whatsapp.com/DblqghuoMsmKEDzxtl1Ifd",
        nome_grupo="Grupo de Benfeitores",
        tempo_de_administrador=40,
        status=0,
        deleted_at=None,
        
    )
    
    db.session.add(general)
    db.session.flush()
    db.session.commit()


    return user, clifor, address, pedido, general



@pytest.fixture(scope="function")
def seed_marechal():
    nome = faker.name()
    email = faker.email(domain="hotmail.com")
    cpf = faker.cpf()
    user = Usuario(
        nome=nome,
        email=email,
        country="brasil",
        password="sem@Senhdasda",
        status=True,
    )
    db.session.add(user)
    db.session.flush()

    clifor = Clifor(
        fk_usuario_id=user.id,
        nome=nome,
        email=email,
        cpf_cnpj=cpf,
        telefone1="11945672358",
        data_nascimento=datetime.now().date(),
        usuario_criacao=user.id,
    )
    db.session.add(clifor)
    db.session.flush()

    address = Endereco(fk_clifor_id=clifor.id, usuario_criacao=user.id)
    db.session.add(address)

    perfil = Perfil.query.filter_by(nome="Benfeitor").first()

    user_permission = PermissaoUsuario(
        fk_usuario_id=user.id, fk_perfil_id=perfil.id, usuario_criacao=0
    )
    db.session.add(user_permission)

    forma_pagamento = FormaPagamento.query.filter_by(descricao="Pix").first()

    pedido = Pedido(
        fk_clifor_id=clifor.id,
        anonimo=False,
        fk_forma_pagamento_id=forma_pagamento.id,
        periodicidade=1,
        usuario_criacao=0,
    )
    db.session.add(pedido)
    
    marechal = Generais(
        fk_cargo_id=1,
        fk_usuario_id=user.id,
        quant_membros_grupo=34,
        created_at=datetime.now(),
        link_grupo="https://chat.whatsapp.com/24567huoMsmKEDzxtl1Ifd",
        nome_grupo="Grupo mar azul",
        tempo_de_administrador=50,
        status=1,
        deleted_at=None,
    )
    
    db.session.add(marechal)
    db.session.commit()

    return user, clifor, address, pedido, marechal


@pytest.fixture(scope="function")
def seed_general_link_to_marechal(seed_marechal):
    for _ in range(4):
        registros = []
        
        *_ , marechal = seed_marechal
        
        nome = faker.name()
        email = faker.email(domain="gmail.com")
        cpf = faker.cpf()
        user = Usuario(
            nome=nome,
            email=email,
            country="brasil",
            password="sem@Senha123",
            status=True,
        )
        db.session.add(user)
        db.session.flush()

        clifor = Clifor(
            fk_usuario_id=user.id,
            nome=nome,
            email=email,
            cpf_cnpj=cpf,
            telefone1="119768496039",
            data_nascimento=datetime.now().date(),
            usuario_criacao=user.id,
        )
        db.session.add(clifor)
        db.session.flush()

        address = Endereco(fk_clifor_id=clifor.id, usuario_criacao=user.id)
        db.session.add(address)

        perfil = Perfil.query.filter_by(nome="Benfeitor").first()

        user_permission = PermissaoUsuario(
            fk_usuario_id=user.id, fk_perfil_id=perfil.id, usuario_criacao=0
        )
        db.session.add(user_permission)

        forma_pagamento = FormaPagamento.query.filter_by(descricao="Pix").first()

        pedido = Pedido(
            fk_clifor_id=clifor.id,
            anonimo=False,
            fk_forma_pagamento_id=forma_pagamento.id,
            periodicidade=1,
            usuario_criacao=0,
        )
        db.session.add(pedido)
        
        general = Generais(
            fk_cargo_id=2,
            fk_usuario_superior_id=marechal.id,
            fk_usuario_id=user.id,
            quant_membros_grupo=12,
            created_at=datetime.now(),
            link_grupo="https://chat.whatsapp.com/DblqghujngtKEDzxtl1Ifd",
            nome_grupo="Grupo de Benfeitores",
            tempo_de_administrador=40,
            status=1,
            deleted_at=None,
            
        )
        
        db.session.add(general)
        registros.append((user, clifor, address, pedido, general))
        
    db.session.commit()

    return registros 

