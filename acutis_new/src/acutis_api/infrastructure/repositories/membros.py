import uuid
from typing import Any

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import case, func, or_, select

from acutis_api.communication.requests.membros import (
    AtualizarDadosMembroRequest,
)
from acutis_api.domain.entities.benfeitor import Benfeitor
from acutis_api.domain.entities.campanha import Campanha
from acutis_api.domain.entities.campanha_doacao import CampanhaDoacao
from acutis_api.domain.entities.cargo_oficial import CargosOficiais
from acutis_api.domain.entities.doacao import Doacao
from acutis_api.domain.entities.endereco import Endereco
from acutis_api.domain.entities.lead import Lead
from acutis_api.domain.entities.lead_campanha import LeadCampanha
from acutis_api.domain.entities.lembrete_doacao_recorrente import (
    LembreteDoacaoRecorrente,
)
from acutis_api.domain.entities.membro import Membro
from acutis_api.domain.entities.metadado_lead import MetadadoLead
from acutis_api.domain.entities.oficial import Oficial
from acutis_api.domain.entities.pagamento_doacao import PagamentoDoacao
from acutis_api.domain.entities.processamento_doacao import (
    ProcessamentoDoacao,
    StatusProcessamentoEnum,
)
from acutis_api.domain.entities.template_lp import TemplateLP
from acutis_api.domain.repositories.enums.membros_oficiais import (
    StatusMembroOficialEnum,
)
from acutis_api.domain.repositories.membros import (
    MembrosRepositoryInterface,
)
from acutis_api.domain.repositories.schemas.membros import (
    CampoAdicionalSchema,
    CardDoacoesMembroBenfeitorSchema,
    DoacaoMembroBenfeitorSchema,
    HistoricoDoacaoSchema,
    RegistrarNovoEnderecoSchema,
    RegistrarNovoLeadSchema,
    RegistrarNovoMembroSchema,
)
from acutis_api.domain.repositories.schemas.membros_oficiais import (
    RegistraMembroOficialSchema,
)
from acutis_api.domain.repositories.schemas.paginacao import PaginacaoQuery


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

    def excluir_conta(self, lead: Lead) -> None:
        self._database.session.delete(lead)

    def remove_referencias_lead_id(self, fk_lead_id: uuid.UUID) -> None:
        modelo_colunas_map = {
            CargosOficiais: [
                CargosOficiais.criado_por,
                CargosOficiais.atualizado_por,
            ],
            Campanha: [Campanha.criado_por],
            LembreteDoacaoRecorrente: [LembreteDoacaoRecorrente.criado_por],
            TemplateLP: [TemplateLP.criado_por],
            Oficial: [Oficial.atualizado_por],
        }

        for modelo, colunas in modelo_colunas_map.items():
            filtros = [coluna == fk_lead_id for coluna in colunas]

            self._database.session.query(modelo).filter(or_(*filtros)).update(
                {coluna: None for coluna in colunas}, synchronize_session=False
            )

    def listar_doacoes(
        self, filtros: PaginacaoQuery, benfeitor_id: uuid.UUID
    ) -> tuple[list[DoacaoMembroBenfeitorSchema], int]:
        query = (
            self._database.session.query(
                Campanha.nome.label('nome_campanha'),
                Campanha.capa.label('foto_campanha'),
                case(
                    (PagamentoDoacao.recorrente == True, 'Recorrente'),
                    else_='Única',
                ).label('tipo_doacao'),
                Doacao.id.label('doacao_id'),
            )
            .select_from(Benfeitor)
            .join(Membro, Benfeitor.id == Membro.fk_benfeitor_id)
            .join(Lead, Membro.fk_lead_id == Lead.id)
            .join(Doacao, Benfeitor.id == Doacao.fk_benfeitor_id)
            .join(
                CampanhaDoacao,
                Doacao.fk_campanha_doacao_id == CampanhaDoacao.id,
            )
            .join(
                Campanha,
                CampanhaDoacao.fk_campanha_id == Campanha.id,
            )
            .join(PagamentoDoacao, Doacao.id == PagamentoDoacao.fk_doacao_id)
            .join(
                ProcessamentoDoacao,
                PagamentoDoacao.id
                == ProcessamentoDoacao.fk_pagamento_doacao_id,
            )
            .filter(
                Benfeitor.contabilizar,
                Doacao.contabilizar,
                PagamentoDoacao.anonimo == False,
                Benfeitor.id == benfeitor_id,
            )
            .order_by(Doacao.criado_em.desc())
        )

        doacoes_paginate = query.paginate(
            page=filtros.pagina, per_page=filtros.por_pagina, error_out=False
        )

        doacoes, total = doacoes_paginate.items, doacoes_paginate.total

        return doacoes, total

    def buscar_doacao_por_id(self, id: uuid.UUID) -> Doacao | None:
        doacao = self._database.session.get(Doacao, id)
        return doacao

    def buscar_historico_doacao_por_doacao_id(
        self, filtros: PaginacaoQuery, id: uuid.UUID
    ) -> tuple[list[HistoricoDoacaoSchema], int]:
        query = (
            self._database.session.query(
                case(
                    (
                        ProcessamentoDoacao.processado_em.isnot(None),
                        ProcessamentoDoacao.processado_em,
                    ),
                    else_=ProcessamentoDoacao.criado_em,
                ).label('data_doacao'),
                ProcessamentoDoacao.forma_pagamento,
                ProcessamentoDoacao.status.label('status_processamento'),
                PagamentoDoacao.valor.label('valor_doacao'),
            )
            .select_from(Doacao)
            .join(PagamentoDoacao, Doacao.id == PagamentoDoacao.fk_doacao_id)
            .join(
                ProcessamentoDoacao,
                PagamentoDoacao.id
                == ProcessamentoDoacao.fk_pagamento_doacao_id,
            )
            .filter(Doacao.id == id)
            .order_by('data_doacao')
        )

        query_paginate = query.paginate(
            page=filtros.pagina, per_page=filtros.por_pagina, error_out=False
        )

        historico_doacoes, total = query_paginate.items, query_paginate.total

        return historico_doacoes, total

    def atualizar_dados_membro(
        self, request: AtualizarDadosMembroRequest, membro: Membro
    ):
        if request.nome_social is not None:
            membro.nome_social = request.nome_social

        if request.data_nascimento is not None:
            membro.data_nascimento = request.data_nascimento

        if request.endereco is not None:
            membro.endereco.codigo_postal = request.endereco.codigo_postal
            membro.endereco.tipo_logradouro = request.endereco.tipo_logradouro
            membro.endereco.logradouro = request.endereco.logradouro
            membro.endereco.numero = request.endereco.numero
            membro.endereco.complemento = request.endereco.complemento
            membro.endereco.bairro = request.endereco.bairro
            membro.endereco.cidade = request.endereco.cidade
            membro.endereco.estado = request.endereco.estado
            membro.endereco.pais = request.endereco.pais

        membro.cadastro_atualizado_em = func.now()
        self._database.session.add(membro)

    def buscar_card_doacoes_membro_benfeitor(
        self, benfeitor_id: uuid.UUID
    ) -> CardDoacoesMembroBenfeitorSchema:
        query = self._database.session.execute(
            select(
                func.max(ProcessamentoDoacao.processado_em).label(
                    'ultima_doacao'
                ),
                func.count(ProcessamentoDoacao.id).label('quantidade_doacoes'),
                func.coalesce(func.sum(PagamentoDoacao.valor), 0.0).label(
                    'valor_doado'
                ),
            )
            .select_from(Doacao)
            .join(Benfeitor, Doacao.fk_benfeitor_id == Benfeitor.id)
            .join(PagamentoDoacao, Doacao.id == PagamentoDoacao.fk_doacao_id)
            .join(
                ProcessamentoDoacao,
                PagamentoDoacao.id
                == ProcessamentoDoacao.fk_pagamento_doacao_id,
            )
            .where(
                ProcessamentoDoacao.status == StatusProcessamentoEnum.pago,
                Benfeitor.contabilizar == True,
                Doacao.contabilizar == True,
                PagamentoDoacao.anonimo == False,
                Doacao.fk_benfeitor_id == benfeitor_id,
            )
        )

        card_doacoes = query.first()
        return card_doacoes
