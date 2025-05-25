from datetime import datetime

import pytest
from faker import Faker

from acutis_api.domain.entities.cadastro_vocacional import CadastroVocacional
from acutis_api.domain.entities.etapa_vocacional import (
    EtapaVocacional,
    PassosVocacionalEnum,
    PassosVocacionalStatusEnum,
)
from acutis_api.domain.entities.usuario_vocacional import GeneroVocacionalEnum
from acutis_api.infrastructure.extensions import database
from tests.factories import (
    EnderecoFactory,
    EtapaVocacionalFactory,
    FichaVocacionalFactory,
    LeadFactory,
    MembroFactory,
    UsuarioVocacionalFactory,
)

faker = Faker('pt_BR')


@pytest.fixture
def seed_pre_cadastro_vocacional_pendentes():
    registros = []

    for _ in range(10):
        new_pre_cadastro = UsuarioVocacionalFactory()
        database.session.add(new_pre_cadastro)
        database.session.flush()

        new_etapa = EtapaVocacionalFactory(
            fk_usuario_vocacional_id=new_pre_cadastro.id
        )

        database.session.add(new_etapa)
        database.session.commit()
        registros.append((new_pre_cadastro, new_etapa))

    return registros


@pytest.fixture
def seed_pre_cadastro_vocacional_aprovado():
    new_pre_cadastro = UsuarioVocacionalFactory()

    database.session.add(new_pre_cadastro)
    database.session.flush()

    new_etapa = EtapaVocacional(
        fk_usuario_vocacional_id=new_pre_cadastro.id,
        etapa=PassosVocacionalEnum.pre_cadastro,
        status=PassosVocacionalStatusEnum.aprovado,
        justificativa=None,
        fk_responsavel_id=None,
    )

    database.session.add(new_etapa)
    database.session.commit()

    return new_pre_cadastro, new_etapa


@pytest.fixture
def seed_pre_cadastro_vocacional_aprovado_brasil():
    new_pre_cadastro = UsuarioVocacionalFactory(pais='brasil')

    database.session.add(new_pre_cadastro)
    database.session.flush()

    new_etapa = EtapaVocacional(
        fk_usuario_vocacional_id=new_pre_cadastro.id,
        etapa=PassosVocacionalEnum.pre_cadastro,
        status=PassosVocacionalStatusEnum.aprovado,
        justificativa=None,
        fk_responsavel_id=None,
    )

    database.session.add(new_etapa)
    database.session.commit()

    return new_pre_cadastro, new_etapa


@pytest.fixture
def seed_pre_cadastro_vocacional_reprovado():
    new_pre_cadastro = UsuarioVocacionalFactory()

    database.session.add(new_pre_cadastro)
    database.session.flush()

    new_etapa = EtapaVocacional(
        fk_usuario_vocacional_id=new_pre_cadastro.id,
        etapa=PassosVocacionalEnum.pre_cadastro,
        status=PassosVocacionalStatusEnum.reprovado,
        justificativa='justificando a reprovação',
        fk_responsavel_id=None,
    )

    database.session.add(new_etapa)
    database.session.commit()

    return new_pre_cadastro, new_etapa


@pytest.fixture
def seed_pre_cadastro_vocacional_desistencia():
    def _pre_cadastro_vocacional_desistencia(  # noqa: PLR0913 PLR0917
        pais: str | None = None,
        nome: str | None = None,
        telefone: str | None = None,
        email: str | None = None,
        genero: str | None = None,
        etapa: str | None = None,
    ):
        if pais:
            new_pre_cadastro = UsuarioVocacionalFactory(pais=pais)
        elif email:
            new_pre_cadastro = UsuarioVocacionalFactory(email=email)
        elif telefone:
            new_pre_cadastro = UsuarioVocacionalFactory(telefone=telefone)
        elif nome:
            new_pre_cadastro = UsuarioVocacionalFactory(nome=nome)
        elif genero:
            new_pre_cadastro = UsuarioVocacionalFactory(genero=genero)
        else:
            new_pre_cadastro = UsuarioVocacionalFactory()

        database.session.add(new_pre_cadastro)
        database.session.flush()

        new_etapa = EtapaVocacional(
            fk_usuario_vocacional_id=new_pre_cadastro.id,
            etapa=PassosVocacionalEnum.pre_cadastro,
            status=PassosVocacionalStatusEnum.desistencia,
            justificativa=None,
            fk_responsavel_id=None,
        )

        if etapa:
            new_etapa.etapa = etapa

        database.session.add(new_etapa)
        database.session.commit()

        return new_pre_cadastro, new_etapa

    return _pre_cadastro_vocacional_desistencia


@pytest.fixture
def seed_cadastro_vocacional_pendente():
    new_pre_cadastro = UsuarioVocacionalFactory(pais='uruguai')

    database.session.add(new_pre_cadastro)
    database.session.flush()

    new_endereco = EnderecoFactory()

    database.session.add(new_endereco)
    database.session.flush()

    new_etapa_pre_cadastro = EtapaVocacional(
        fk_usuario_vocacional_id=new_pre_cadastro.id,
        etapa=PassosVocacionalEnum.pre_cadastro,
        status=PassosVocacionalStatusEnum.aprovado,
        justificativa=None,
        fk_responsavel_id=None,
    )

    database.session.add(new_etapa_pre_cadastro)
    database.session.flush()

    new_cadastro_vocacional = CadastroVocacional(
        fk_usuario_vocacional_id=new_pre_cadastro.id,
        fk_endereco_id=new_endereco.id,
        data_nascimento=datetime.strptime(faker.date(), '%Y-%m-%d').date(),
        documento_identidade='20994073046',
    )

    database.session.add(new_cadastro_vocacional)
    database.session.flush()

    new_etapa_cadastro = EtapaVocacional(
        fk_usuario_vocacional_id=new_pre_cadastro.id,
        etapa=PassosVocacionalEnum.cadastro,
        status=PassosVocacionalStatusEnum.pendente,
        justificativa=None,
        fk_responsavel_id=None,
    )

    database.session.add(new_etapa_cadastro)

    database.session.commit()

    return new_cadastro_vocacional


@pytest.fixture
def seed_cadastro_vocacional_aprovado():
    def _cadastro_vocacional_aprovado(  # noqa: PLR0913 PLR0917
        pais: str | None = None,
        documento_identidade: str | None = None,
        nome: str | None = None,
        telefone: str | None = None,
        email: str | None = None,
        status: str | None = None,
        genero: GeneroVocacionalEnum | None = None,
    ):
        new_pre_cadastro = UsuarioVocacionalFactory()

        if pais:
            new_pre_cadastro.pais = pais
        if email:
            new_pre_cadastro.email = email
        if telefone:
            new_pre_cadastro.telefone = telefone
        if nome:
            new_pre_cadastro.nome = nome
        if genero:
            new_pre_cadastro.genero = genero

        database.session.add(new_pre_cadastro)
        database.session.flush()

        new_etapa_pre_cadastro = EtapaVocacional(
            fk_usuario_vocacional_id=new_pre_cadastro.id,
            etapa=PassosVocacionalEnum.pre_cadastro,
            status=PassosVocacionalStatusEnum.aprovado,
            justificativa=None,
            fk_responsavel_id=None,
        )

        database.session.add(new_etapa_pre_cadastro)
        database.session.flush()

        new_endereco = EnderecoFactory()

        if pais:
            new_endereco.pais = pais

        database.session.add(new_endereco)
        database.session.flush()

        new_cadastro_vocacional = CadastroVocacional(
            fk_usuario_vocacional_id=new_pre_cadastro.id,
            fk_endereco_id=new_endereco.id,
            data_nascimento=datetime.strptime(faker.date(), '%Y-%m-%d').date(),
            documento_identidade=faker.random_int(min=12),
        )

        if documento_identidade:
            new_cadastro_vocacional.documento_identidade = documento_identidade
        database.session.add(new_cadastro_vocacional)
        database.session.flush()

        new_etapa_cadastro = EtapaVocacional(
            fk_usuario_vocacional_id=new_pre_cadastro.id,
            etapa=PassosVocacionalEnum.cadastro,
            status=PassosVocacionalStatusEnum.aprovado,
            justificativa=None,
            fk_responsavel_id=None,
        )

        if status:
            new_etapa_cadastro.status = status

        database.session.add(new_etapa_cadastro)

        database.session.commit()

        return new_pre_cadastro, new_cadastro_vocacional

    return _cadastro_vocacional_aprovado


@pytest.fixture
def seed_ficha_vocacional(seed_cadastro_vocacional_aprovado):
    def _ficha_vocacional(  # noqa: PLR0913 PLR0917
        pais: str | None = None,
        documento_identidade: str | None = None,
        nome: str | None = None,
        telefone: str | None = None,
        email: str | None = None,
        status: str | None = None,
        genero: GeneroVocacionalEnum | None = None,
    ):
        if pais:
            pre_cadastro, cadastro_vocacional = (
                seed_cadastro_vocacional_aprovado(
                    pais=pais,
                )
            )
        elif email:
            pre_cadastro, cadastro_vocacional = (
                seed_cadastro_vocacional_aprovado(
                    email=email,
                )
            )
        elif telefone:
            pre_cadastro, cadastro_vocacional = (
                seed_cadastro_vocacional_aprovado(
                    telefone=telefone,
                )
            )
        elif nome:
            pre_cadastro, cadastro_vocacional = (
                seed_cadastro_vocacional_aprovado(
                    nome=nome,
                )
            )
        elif documento_identidade:
            pre_cadastro, cadastro_vocacional = (
                seed_cadastro_vocacional_aprovado(
                    documento_identidade=documento_identidade,
                )
            )
        elif genero:
            pre_cadastro, cadastro_vocacional = (
                seed_cadastro_vocacional_aprovado(
                    genero=genero,
                )
            )
        else:
            pre_cadastro, cadastro_vocacional = (
                seed_cadastro_vocacional_aprovado()
            )

        new_ficha_vocacional = FichaVocacionalFactory(
            fk_usuario_vocacional_id=pre_cadastro.id
        )

        database.session.add(new_ficha_vocacional)
        database.session.flush()

        new_etapa_ficha_vocacional = EtapaVocacional(
            fk_usuario_vocacional_id=pre_cadastro.id,
            etapa=PassosVocacionalEnum.ficha_vocacional,
            status=PassosVocacionalStatusEnum.pendente,
            justificativa=None,
            fk_responsavel_id=None,
        )

        if status:
            new_etapa_ficha_vocacional.status = status

        database.session.add(new_etapa_ficha_vocacional)

        database.session.commit()

        return pre_cadastro, cadastro_vocacional, new_ficha_vocacional

    return _ficha_vocacional


@pytest.fixture
def seed_vocacionais_reprovados():
    usuarios = []
    etapas = []

    lead = LeadFactory(nome='Yan Takabixiga')
    lead.senha = 'Teste123@'
    database.session.add(lead)

    endereco = EnderecoFactory()
    database.session.add(endereco)

    responsavel = MembroFactory(fk_lead_id=lead.id, fk_endereco_id=endereco.id)

    database.session.add(responsavel)
    database.session.flush()

    for _ in range(5):
        new_pre_cadastro = UsuarioVocacionalFactory()
        database.session.add(new_pre_cadastro)
        database.session.flush()

        new_etapa = EtapaVocacional(
            fk_usuario_vocacional_id=new_pre_cadastro.id,
            etapa=PassosVocacionalEnum.pre_cadastro,
            status=PassosVocacionalStatusEnum.reprovado,
            justificativa='fsfs',
            fk_responsavel_id=responsavel.id,
        )
        usuarios.append(new_pre_cadastro)
        etapas.append(new_etapa)

        database.session.add(new_etapa)
        database.session.commit()

    return usuarios, etapas


@pytest.fixture
def seed_vocacional_reprovado():
    def _vocacional_reprovado(  # noqa: PLR0913 PLR0917
        nome: str | None = None,
        telefone: str | None = None,
        email: str | None = None,
        genero: str | None = None,
        etapa: str | None = None,
        pais: str | None = None,
    ):
        new_pre_cadastro = UsuarioVocacionalFactory()

        if nome:
            new_pre_cadastro.nome = nome
        if telefone:
            new_pre_cadastro.telefone = telefone
        if email:
            new_pre_cadastro.email = email
        if genero:
            new_pre_cadastro.genero = genero
        if pais:
            new_pre_cadastro.pais = pais

        database.session.add(new_pre_cadastro)
        database.session.flush()

        new_etapa = EtapaVocacional(
            fk_usuario_vocacional_id=new_pre_cadastro.id,
            etapa=PassosVocacionalEnum.pre_cadastro,
            status=PassosVocacionalStatusEnum.reprovado,
            justificativa=None,
            fk_responsavel_id=None,
        )
        if etapa:
            new_etapa.etapa = etapa

        database.session.add(new_etapa)
        database.session.commit()

        return new_pre_cadastro, new_etapa

    return _vocacional_reprovado
