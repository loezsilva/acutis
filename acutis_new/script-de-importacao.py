import logging
import secrets
from urllib.parse import quote_plus

from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import MetaData, Table, create_engine, select
from sqlalchemy.orm import sessionmaker

from acutis_api.api.app import app
from acutis_api.domain.entities.campanha import Campanha
from acutis_api.domain.entities.campo_adicional import CampoAdicional
from acutis_api.domain.entities.cargo_oficial import CargosOficiais
from acutis_api.domain.entities.endereco import Endereco
from acutis_api.domain.entities.lead import Lead
from acutis_api.domain.entities.lead_campanha import LeadCampanha
from acutis_api.domain.entities.membro import Membro
from acutis_api.domain.entities.metadado_lead import MetadadoLead
from acutis_api.domain.entities.oficial import Oficial
from acutis_api.infrastructure.extensions import database


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env', env_file_encoding='utf-8', extra='ignore'
    )

    PROD_DATABASE_HOST: str
    PROD_DATABASE_USERNAME: str
    PROD_DATABASE_PASSWORD: str
    PROD_DATABASE_NAME: str
    PROD_DATABASE_PORT: str

    DATABASE_HOST: str
    DATABASE_USERNAME: str
    DATABASE_PASSWORD: str
    DATABASE_NAME: str
    DATABASE_PORT: str


settings = Settings()

connection_acutis_v0_database = f'mssql+pyodbc://{settings.PROD_DATABASE_USERNAME}:{quote_plus(settings.PROD_DATABASE_PASSWORD)}@{settings.PROD_DATABASE_HOST},{settings.PROD_DATABASE_PORT}/{settings.PROD_DATABASE_NAME}?driver=ODBC+Driver+17+for+SQL+Server' # noqa

engine_acutis_v0 = create_engine(connection_acutis_v0_database)
metadata = MetaData()

UsuarioV0 = Table('usuario', metadata, autoload_with=engine_acutis_v0)
CliforV0 = Table('clifor', metadata, autoload_with=engine_acutis_v0)
AcaoLeadsV0 = Table('actions_leads', metadata, autoload_with=engine_acutis_v0)
FotoLeadsV0 = Table('foto_leads', metadata, autoload_with=engine_acutis_v0)
CampanhaV0 = Table('campanha', metadata, autoload_with=engine_acutis_v0)
CargoV0 = Table('cargo', metadata, autoload_with=engine_acutis_v0)
CargoUsuarioV0 = Table(
    'cargo_usuario', metadata, autoload_with=engine_acutis_v0
)
ConteudoLandpageV0 = Table(
    'conteudo_landpage', metadata, autoload_with=engine_acutis_v0
)
EnderecoV0 = Table('endereco', metadata, autoload_with=engine_acutis_v0)
GeneralV0 = Table('generais', metadata, autoload_with=engine_acutis_v0)
LandpageV0 = Table('landpage', metadata, autoload_with=engine_acutis_v0)
UsersImportsV0 = Table(
    'users_imports', metadata, autoload_with=engine_acutis_v0
)

session_acutis_v0 = sessionmaker(engine_acutis_v0)


def script_equalizacao_cadastros():
    with app.app_context():
        _importar_cargos()
        _importar_campanhas()

        with session_acutis_v0() as session:
            clifors_v0 = session.execute(select(CliforV0)).all()

        _importar_clifor(clifors_v0)
        _importar_generais_e_campos_adicionais(clifors_v0)
        _importar_users_imports()


def _importar_cargos():
    with session_acutis_v0() as session:
        cargos_oficiais_v0 = session.execute(select(CargoV0)).all()
        for cargo_v0 in cargos_oficiais_v0:
            cargo_existente_v1 = database.session.scalar(
                select(CargosOficiais).where(
                    CargosOficiais.nome_cargo.contains(cargo_v0.nome)
                )
            )

            if cargo_existente_v1:
                continue

            cargo_v1 = CargosOficiais(
                nome_cargo=cargo_v0.nome.lower(),
                criado_por='62D192FC-7EC3-42B1-B6F6-B0679F4CE375',
                atualizado_por=None,
                atualizado_em=None,
            )
            database.session.add(cargo_v1)
        database.session.commit()

    logging.warning('---> Importar Cargos Finalizado')


def _importar_campanhas():
    with session_acutis_v0() as session:
        campanhas_v0 = session.execute(select(CampanhaV0)).all()

    for campanha_v0 in campanhas_v0:
        campanha_existente_v1 = database.session.scalar(
            select(
                Campanha
            ).where(Campanha.nome.contains(campanha_v0.titulo))
        )
        if campanha_existente_v1:
            continue

        campanha = Campanha(
            fk_cargo_oficial_id=None,
            objetivo=campanha_v0.objetivo,
            nome=campanha_v0.titulo,
            publica=campanha_v0.publica,
            ativa=campanha_v0.status,
            meta=(campanha_v0.cadastros_meta
                  if campanha_v0.objetivo == 'cadastro'
                  else campanha_v0.valor_meta
                ),
            capa=campanha_v0.filename,
            chave_pix=campanha_v0.chave_pix,
            criado_por='62D192FC-7EC3-42B1-B6F6-B0679F4CE375',
            superior_obrigatorio=False,
        )
        database.session.add(campanha)
    database.session.commit()

    logging.warning('---> Importar Campanhas Finalizado')


def _importar_clifor(clifors_v0):
    logging.warning('---> Iniciando importação de clifors')
    erros = 0
    contador = 0
    qtd_registros = len(clifors_v0)
    with session_acutis_v0() as session:
        for clifor_v0 in clifors_v0:
            try:
                contador += 1
                logging.warning(f'---> _importar_clifor -> Adicionando {contador}° de {qtd_registros}')
                if clifor_v0.email is None:
                    continue

                lead_v1: Lead | None = database.session.scalar(
                    select(Lead).where(Lead.email == clifor_v0.email)
                )
                if lead_v1 and lead_v1.membro is not None:
                    continue

                usuario_v0 = session.execute(
                    select(
                        UsuarioV0
                    ).where(UsuarioV0.c.id == clifor_v0.fk_usuario_id)
                ).first()

                endereco_v0 = session.execute(
                    select(
                        EnderecoV0
                    ).where(EnderecoV0.c.fk_clifor_id == clifor_v0.id)
                ).first()

                cep_formatado = (''.join(filter(str.isdigit, endereco_v0.cep))
                                if endereco_v0 and endereco_v0.cep else None)

                novo_endereco_v1 = Endereco(
                    codigo_postal=cep_formatado,
                    tipo_logradouro=None,
                    logradouro=endereco_v0.rua if endereco_v0 else None,
                    numero=endereco_v0.numero if endereco_v0 else None,
                    complemento=endereco_v0.complemento if endereco_v0 else None,
                    bairro=endereco_v0.bairro if endereco_v0 else None,
                    cidade=endereco_v0.cidade if endereco_v0 else None,
                    estado=endereco_v0.estado if endereco_v0 else None,
                    pais=endereco_v0.pais_origem if endereco_v0 else None,
                    obriga_atualizar_endereco=True,
                )
                database.session.add(novo_endereco_v1)

                novo_lead_v1 = Lead(
                    nome=clifor_v0.nome,
                    email=clifor_v0.email,
                    telefone=(
                        clifor_v0.telefone1
                        if clifor_v0.telefone1 else '00000000000'
                    ),
                    pais=usuario_v0.country if usuario_v0.country else 'brasil',
                    origem_cadastro='acutis',
                    status=False,
                    ultimo_acesso=None,
                )
                novo_lead_v1.senha = secrets.token_hex(16)
                database.session.add(novo_lead_v1)

                novo_membro_v1 = Membro(
                    fk_lead_id=novo_lead_v1.id,
                    fk_benfeitor_id=None,
                    fk_endereco_id=novo_endereco_v1.id,
                    nome_social=usuario_v0.nome_social,
                    data_nascimento=clifor_v0.data_nascimento,
                    numero_documento=clifor_v0.cpf_cnpj,
                    sexo=clifor_v0.sexo,
                    foto=usuario_v0.avatar
                )
                database.session.add(novo_membro_v1)
                database.session.commit()
            except:
                erros += 1
                database.session.rollback()
                logging.warning(f"---> Ocorreu {erros} ao tentar importar clifor")
    logging.warning('---> Importação de clifors finalizada')


def _importar_generais_e_campos_adicionais(clifors_v0):
    logging.warning('---> Iniciando importação de generais e campos adicionais')
    erros = 0
    contador = 0
    qtd_registros = len(clifors_v0)
    with session_acutis_v0() as session:
        for clifor_v0 in clifors_v0:
            try:
                contador += 1
                logging.warning(f'---> _importar_generais_e_campos_adicionais -> Adicionando {contador}° de {qtd_registros}')

                if clifor_v0.email is None:
                    continue
                usuario_v0 = session.execute(
                    select(
                        UsuarioV0
                    ).where(UsuarioV0.c.id == clifor_v0.fk_usuario_id)
                ).first()

                general_v0 = session.execute(
                    select(
                        GeneralV0
                    ).where(GeneralV0.c.fk_usuario_id == usuario_v0.id)
                ).first()

                novo_lead_v1 = database.session.scalar(
                    select(Lead).where(
                        Lead.email == usuario_v0.email
                    )
                )

                if novo_lead_v1 is None:
                    continue

                if general_v0:
                    oficial_existente = database.session.scalar(
                        select(Oficial).where(
                            Oficial.fk_membro_id == novo_lead_v1.membro.id
                        )
                    )
                    if oficial_existente:
                        continue

                    campanha_general_v1 = database.session.scalar(
                        select(Campanha).where(Campanha.nome == 'Membro Oficial')
                    )

                    vinculo_lead_campanha_v1 = LeadCampanha(
                        fk_lead_id=novo_lead_v1.id,
                        fk_campanha_id=campanha_general_v1.id,
                    )
                    database.session.add(vinculo_lead_campanha_v1)

                    superior_v1 = None
                    if general_v0.fk_usuario_superior_id:
                        usuario_superior_v0 = session.execute(
                            select(
                                UsuarioV0
                            ).where(
                                UsuarioV0.c.id == general_v0.fk_usuario_superior_id
                            )
                        ).first()

                        superior_v1 = database.session.scalar(
                            select(Lead).where(
                                Lead.email == usuario_superior_v0.email
                            )
                        )

                    general_v1 = database.session.scalar(
                        select(CargosOficiais).where(
                            CargosOficiais.nome_cargo == 'general'
                        )
                    )

                    marechal_v1 = database.session.scalar(
                        select(CargosOficiais).where(
                            CargosOficiais.nome_cargo == 'marechal'
                        )
                    )

                    oficial_v1 = Oficial(
                        fk_membro_id=novo_lead_v1.membro.id,
                        fk_superior_id=superior_v1.membro.id if superior_v1 else None,
                        fk_cargo_oficial_id=general_v1.id if general_v0.fk_cargo_id == 2 else marechal_v1.id,
                        status='pendente' if general_v0.status == 0 else 'aprovado',
                    )
                    database.session.add(oficial_v1)

                    ca_qtd_membro_grupo = database.session.scalar(
                        select(CampoAdicional).where(
                            CampoAdicional.nome_campo == 'quantidade_membros_grupo'
                        )
                    )

                    ca_nome_grupo = database.session.scalar(
                        select(CampoAdicional).where(
                            CampoAdicional.nome_campo == 'nome_grupo'
                        )
                    )

                    ca_link_grupo = database.session.scalar(
                        select(CampoAdicional).where(
                            CampoAdicional.nome_campo == 'link_grupo'
                        )
                    )

                    ca_tempo_de_administrador = database.session.scalar(
                        select(CampoAdicional).where(
                            CampoAdicional.nome_campo == 'tempo_de_administrador'
                        )
                    )

                    metadata_lead_membro_grupo = MetadadoLead(
                        fk_lead_id=novo_lead_v1.id,
                        fk_campo_adicional_id=ca_qtd_membro_grupo.id,
                        valor_campo=general_v0.quant_membros_grupo
                    )
                    database.session.add(metadata_lead_membro_grupo)

                    metadata_lead_nome_grupo = MetadadoLead(
                        fk_lead_id=novo_lead_v1.id,
                        fk_campo_adicional_id=ca_nome_grupo.id,
                        valor_campo=general_v0.nome_grupo
                    )
                    database.session.add(metadata_lead_nome_grupo)

                    metadata_lead_link_grupo = MetadadoLead(
                        fk_lead_id=novo_lead_v1.id,
                        fk_campo_adicional_id=ca_link_grupo.id,
                        valor_campo=general_v0.link_grupo
                    )
                    database.session.add(metadata_lead_link_grupo)

                    metadata_lead_tempo_de_administrador = MetadadoLead(
                        fk_lead_id=novo_lead_v1.id,
                        fk_campo_adicional_id=ca_tempo_de_administrador.id,
                        valor_campo=general_v0.tempo_de_administrador
                    )
                    database.session.add(metadata_lead_tempo_de_administrador)

                else:
                    if usuario_v0.campanha_origem:
                        campanha_v0 = session.execute(
                            select(CampanhaV0).where(
                                CampanhaV0.c.id == usuario_v0.campanha_origem
                            )
                        ).first()

                        campanha_v1 = database.session.scalar(
                            select(Campanha).where(
                                Campanha.nome == campanha_v0.titulo
                            )
                        )

                        vinculo_existente = database.session.scalar(
                            select(LeadCampanha).where(
                                LeadCampanha.fk_lead_id == novo_lead_v1.id,
                                LeadCampanha.fk_campanha_id == campanha_v1.id,
                            )
                        )
                        if vinculo_existente:
                            continue

                        vinculo_lead_campanha_v1 = LeadCampanha(
                            fk_lead_id=novo_lead_v1.id,
                            fk_campanha_id=campanha_v1.id,
                        )
                        database.session.add(vinculo_lead_campanha_v1)
                    database.session.commit()
            except:
                erros += 1
                database.session.rollback()
                logging.warning(f"---> Ocorreu {erros} ao tentar importar generais e campos adicionais")
    logging.warning('---> Importação de generais e campos adicionais finalizado')


def _importar_users_imports():
    logging.warning('---> Iniciando importação de users imports e campos adicionais')
    with session_acutis_v0() as session:
        leads_v0 = session.execute(select(UsersImportsV0)).all()
        erros = 0
        contador = 0
        qtd_registros = len(leads_v0)
        for lead_v0 in leads_v0:
            try:
                contador += 1
                logging.warning(f'---> _importar_users_imports -> Adicionando {contador}° de {qtd_registros}')
                lead_v1 = database.session.scalar(
                    select(Lead).where(Lead.email == lead_v0.email)
                )

                if lead_v1:
                    continue

                novo_lead_v1 = Lead(
                    nome=lead_v0.nome,
                    email=lead_v0.email,
                    telefone=(
                        lead_v0.phone
                        if lead_v0.phone else '00000000000'
                    ),
                    pais='brasil',
                    origem_cadastro='acutis',
                    status=False,
                    ultimo_acesso=None
                )
                novo_lead_v1.senha = secrets.token_hex(16)
                database.session.add(novo_lead_v1)

                if lead_v0.origem_cadastro == 3:
                    campanha_v1 = database.session.scalar(
                        select(Campanha).where(
                            Campanha.nome == 'Campanha de Oração pela sua família'
                        )
                    )

                    vinculo_existente = database.session.scalar(
                        select(LeadCampanha).where(
                            LeadCampanha.fk_lead_id == novo_lead_v1.id,
                            LeadCampanha.fk_campanha_id == campanha_v1.id,
                        )
                    )
                    if vinculo_existente:
                        continue

                    vinculo_lead_campanha_v1 = LeadCampanha(
                        fk_lead_id=novo_lead_v1.id,
                        fk_campanha_id=campanha_v1.id,
                    )
                    database.session.add(vinculo_lead_campanha_v1)

                    ca_envie_a_foto_da_sua_familia = database.session.scalar(
                        select(CampoAdicional).where(
                            CampoAdicional.nome_campo == 'envie_a_foto_da_sua_família'
                        )
                    )

                    foto_lead_v0 = session.execute(
                        select(FotoLeadsV0).where(
                            FotoLeadsV0.c.fk_user_import_id == lead_v0.id
                        )
                    ).first()

                    if foto_lead_v0:
                        metadata_lead_envie_a_foto_da_sua_familia = MetadadoLead(
                            fk_lead_id=novo_lead_v1.id,
                            fk_campo_adicional_id=ca_envie_a_foto_da_sua_familia.id,
                            valor_campo=foto_lead_v0.foto
                        )
                        database.session.add(metadata_lead_envie_a_foto_da_sua_familia)

                    ca_intencao = database.session.scalar(
                        select(CampoAdicional).where(
                            CampoAdicional.nome_campo == 'intencao'
                        )
                    )

                    metadata_lead_intencao = MetadadoLead(
                        fk_lead_id=novo_lead_v1.id,
                        fk_campo_adicional_id=ca_intencao.id,
                        valor_campo=lead_v0.intencao
                    )
                    database.session.add(metadata_lead_intencao)

                else:
                    acao_lead_v0 = session.execute(
                        select(AcaoLeadsV0).where(
                            AcaoLeadsV0.c.id == lead_v0.origem_cadastro
                        )
                    ).first()

                    campanha_v1 = database.session.scalar(
                        select(Campanha).where(
                            Campanha.nome == acao_lead_v0.nome
                        )
                    )

                    vinculo_existente = database.session.scalar(
                        select(LeadCampanha).where(
                            LeadCampanha.fk_lead_id == novo_lead_v1.id,
                            LeadCampanha.fk_campanha_id == campanha_v1.id,
                        )
                    )
                    if vinculo_existente:
                        continue

                    vinculo_lead_campanha_v1 = LeadCampanha(
                        fk_lead_id=novo_lead_v1.id,
                        fk_campanha_id=campanha_v1.id,
                    )
                    database.session.add(vinculo_lead_campanha_v1)
                database.session.commit()
            except:
                erros += 1
                database.session.rollback()
                logging.warning(f"---> Ocorreu {erros} ao tentar importar users imports")


if __name__ == '__main__':
    script_equalizacao_cadastros()
