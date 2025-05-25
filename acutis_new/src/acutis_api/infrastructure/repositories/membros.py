import uuid
from typing import Any

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func, select

from acutis_api.domain.entities.campanha import Campanha
from acutis_api.domain.entities.endereco import Endereco
from acutis_api.domain.entities.lead import Lead
from acutis_api.domain.entities.lead_campanha import LeadCampanha
from acutis_api.domain.entities.membro import Membro
from acutis_api.domain.entities.metadado_lead import MetadadoLead
from acutis_api.domain.entities.oficial import Oficial
from acutis_api.domain.repositories.enums.membros_oficiais import (
    StatusMembroOficialEnum,
)
from acutis_api.domain.repositories.membros import (
    MembrosRepositoryInterface,
)
from acutis_api.domain.repositories.schemas.membros import (
    CampoAdicionalSchema,
    RegistrarNovoEnderecoSchema,
    RegistrarNovoLeadSchema,
    RegistrarNovoMembroSchema,
)
from acutis_api.domain.repositories.schemas.membros_oficiais import (
    RegistraMembroOficialSchema,
)


class MembrosRepository(MembrosRepositoryInterface):
    def __init__(self, database: SQLAlchemy):
        self._database = database

    def salvar_alteracoes(self):
        self._database.session.commit()

    def verificar_cadastro_por_documento_e_email(
        self, documento: str, email: str
    ) -> Membro | None:
        db_membro = self._database.session.execute(
            select(
                Lead.email,
                Membro.numero_documento,
            )
            .outerjoin(Membro, Lead.id == Membro.fk_lead_id)
            .where(
                (Membro.numero_documento == documento) | (Lead.email == email)
            )
        ).first()
        return db_membro

    def buscar_lead_por_email(self, email: str) -> Lead | None:
        db_lead = self._database.session.scalar(
            select(Lead).where(Lead.email == email)
        )
        return db_lead

    def atualizar_dados_lead(
        self, lead: Lead, nome: str, email: str, telefone: str, pais: str
    ):
        lead.nome = nome
        lead.email = email
        lead.telefone = telefone
        lead.pais = pais

        self._database.session.add(lead)

    def registrar_novo_lead(self, dados: RegistrarNovoLeadSchema) -> Lead:
        lead = Lead(
            nome=dados.nome,
            email=dados.email,
            telefone=dados.telefone,
            pais=dados.pais,
            origem_cadastro=dados.origem_cadastro,
            status=dados.status,
        )
        lead.senha = dados.senha.get_secret_value()
        self._database.session.add(lead)

        return lead

    def registrar_novo_endereco(
        self, dados_endereco: RegistrarNovoEnderecoSchema
    ) -> Endereco:
        endereco = Endereco(
            codigo_postal=dados_endereco.codigo_postal,
            tipo_logradouro=dados_endereco.tipo_logradouro,
            logradouro=dados_endereco.logradouro,
            numero=dados_endereco.numero,
            complemento=dados_endereco.complemento,
            bairro=dados_endereco.bairro,
            cidade=dados_endereco.cidade,
            estado=dados_endereco.estado,
            pais=dados_endereco.pais,
        )
        self._database.session.add(endereco)

        return endereco

    def registrar_novo_membro(
        self,
        dados_membro: RegistrarNovoMembroSchema,
    ) -> Membro:
        membro = Membro(
            fk_lead_id=dados_membro.lead_id,
            fk_endereco_id=dados_membro.endereco_id,
            fk_benfeitor_id=dados_membro.benfeitor_id,
            nome_social=dados_membro.nome_social,
            data_nascimento=dados_membro.data_nascimento,
            numero_documento=dados_membro.numero_documento,
            sexo=dados_membro.sexo,
            foto=dados_membro.foto,
        )
        self._database.session.add(membro)

        return membro

    def buscar_membro_por_lead_id(self, id: uuid.UUID) -> Membro | None:
        membro = self._database.session.scalar(
            select(Membro).where(Membro.fk_lead_id == id)
        )
        return membro

    def buscar_campanha_por_id(self, id: uuid.UUID) -> Campanha | None:
        campanha = self._database.session.get(Campanha, id)
        return campanha

    def vincular_lead_a_campanha_registro(
        self, lead_id: uuid.UUID, campanha_id: uuid.UUID
    ):
        lead_campanha = LeadCampanha(
            fk_lead_id=lead_id,
            fk_campanha_id=campanha_id,
        )
        self._database.session.add(lead_campanha)

    def buscar_vinculo_de_lead_a_campanha_registro(
        self, lead_id: uuid.UUID, campanha_id: uuid.UUID
    ) -> LeadCampanha | None:
        vinculo_existente = self._database.session.scalar(
            select(LeadCampanha).where(
                LeadCampanha.fk_lead_id == lead_id,
                LeadCampanha.fk_campanha_id == campanha_id,
            )
        )
        return vinculo_existente

    def registrar_campo_adicional_metadado_lead(
        self, lead_id: uuid.UUID, campo: CampoAdicionalSchema
    ):
        metadata_lead = MetadadoLead(
            fk_lead_id=lead_id,
            fk_campo_adicional_id=campo.campo_adicional_id,
            valor_campo=campo.valor_campo,
        )
        self._database.session.add(metadata_lead)

    def buscar_campo_adicional_metadado_lead(
        self, lead_id: uuid.UUID, campo_adicional_id: uuid.UUID
    ) -> MetadadoLead | None:
        metadata_lead = self._database.session.scalar(
            select(MetadadoLead).where(
                MetadadoLead.fk_lead_id == lead_id,
                MetadadoLead.fk_campo_adicional_id == campo_adicional_id,
            )
        )
        return metadata_lead

    def atualizar_campo_adicional_metadado_lead(
        self, metadado_lead: MetadadoLead, valor_campo: Any
    ):
        metadado_lead.valor_campo = valor_campo
        self._database.session.add(metadado_lead)

    @staticmethod
    def ativa_conta_com_senha(senha_hashed: str, lead: Lead) -> None:
        lead.password_hashed = senha_hashed
        lead.status = True

    def buscar_lead_por_telefone(self, telefone: str) -> Lead | None:
        db_lead = self._database.session.scalar(
            select(Lead).where(Lead.telefone == telefone)
        )
        return db_lead

    def buscar_oficial_por_fk_membro_id(
        self, fk_membro_id: uuid.UUID
    ) -> Oficial:
        return (
            self._database.session.query(Oficial)
            .filter(Oficial.fk_membro_id == fk_membro_id)
            .first()
        )

    def registrar_novo_membro_oficial(
        self, dados_da_requisicao: RegistraMembroOficialSchema
    ):
        novo_membro_oficial = Oficial(
            fk_membro_id=dados_da_requisicao.fk_membro_id,
            fk_cargo_oficial_id=dados_da_requisicao.fk_cargo_oficial_id,
            fk_superior_id=dados_da_requisicao.fk_superior_id,
            status=StatusMembroOficialEnum.pendente,
            atualizado_por=None,
        )

        self._database.session.add(novo_membro_oficial)
        return novo_membro_oficial

    @staticmethod
    def alterar_senha(usuario: Lead, nova_senha: str):
        usuario.senha = nova_senha

    def atualizar_data_ultimo_acesso(self, lead: Lead):
        lead.ultimo_acesso = func.now()
        self._database.session.add(lead)
