import re
from datetime import datetime
from typing import Dict
from uuid import UUID

from flask_sqlalchemy import SQLAlchemy
from flask_sqlalchemy.pagination import Pagination
from sqlalchemy import label

from acutis_api.domain.entities import (
    CadastroVocacional,
    EtapaVocacional,
    FichaVocacional,
    UsuarioVocacional,
)
from acutis_api.domain.entities.endereco import Endereco
from acutis_api.domain.entities.lead import Lead
from acutis_api.domain.entities.membro import Membro
from acutis_api.domain.entities.sacramento_vocacional import (
    SacramentoVocacional,
)
from acutis_api.domain.repositories.enums.vocacional import (
    PassosVocacionalEnum,
    PassosVocacionalStatusEnum,
)
from acutis_api.domain.repositories.schemas.vocacional import (
    DecodificarTokenVocacionalSchema,
    ListarCadastrosVocacionaisSchema,
    ListarDesistenciaVocacionaisSchema,
    ListarFichasVocacionaisSchema,
    ListarPreCadastrosSchema,
    ListarVocacionaisRecusadosSchema,
)
from acutis_api.domain.repositories.vocacional import (
    InterfaceVocacionalRepository,
)


class VocacionalRepository(InterfaceVocacionalRepository):  # noqa: PLR0904
    def __init__(self, db: SQLAlchemy):
        self.__db = db

    def salvar_alteracoes(self):
        self.__db.session.commit()

    def deletar_vocacional(self, vocacional: UsuarioVocacional):
        self.__db.session.delete(vocacional)
        self.__db.session.commit()

    def verificar_usuario_vocacional_por_email(
        self, data: dict
    ) -> UsuarioVocacional | None:
        db_cadastro_vocacional = (
            self.__db.session.query(UsuarioVocacional)
            .filter(UsuarioVocacional.email == data.email)
            .first()
        )
        return db_cadastro_vocacional

    def pre_cadastro_vocacional(self, data: dict) -> UsuarioVocacional | None:
        new_pre_cadastro = UsuarioVocacional(
            nome=data.nome,
            email=data.email,
            telefone=data.telefone,
            genero=data.genero,
            pais=data.pais,
        )

        self.__db.session.add(new_pre_cadastro)
        self.__db.session.flush()

        new_etapa = EtapaVocacional(
            fk_usuario_vocacional_id=new_pre_cadastro.id,
            etapa=PassosVocacionalEnum.pre_cadastro,
            status=PassosVocacionalStatusEnum.pendente,
            justificativa=None,
            fk_responsavel_id=None,
        )
        self.__db.session.add(new_etapa)

        return new_pre_cadastro

    def busca_pre_cadastro_vocacional(  # noqa: PLR0912
        self, filters: ListarPreCadastrosSchema
    ) -> Pagination:
        query_pre_cadastros = (
            self.__db.session.query(
                UsuarioVocacional,
                CadastroVocacional,
                FichaVocacional,
                EtapaVocacional,
                Endereco,
            )
            .join(
                UsuarioVocacional,
                UsuarioVocacional.id
                == EtapaVocacional.fk_usuario_vocacional_id,
            )
            .outerjoin(
                CadastroVocacional,
                CadastroVocacional.fk_usuario_vocacional_id
                == UsuarioVocacional.id,
            )
            .outerjoin(
                Endereco, Endereco.id == CadastroVocacional.fk_endereco_id
            )
            .outerjoin(
                FichaVocacional,
                FichaVocacional.fk_usuario_vocacional_id
                == UsuarioVocacional.id,
            )
            .filter(
                EtapaVocacional.etapa == PassosVocacionalEnum.pre_cadastro,
                EtapaVocacional.status.in_([
                    PassosVocacionalStatusEnum.pendente,
                    PassosVocacionalStatusEnum.aprovado,
                ]),
            )
            .order_by(self.__db.desc(EtapaVocacional.criado_em))
        )

        if filters.pais:
            query_pre_cadastros = query_pre_cadastros.filter(
                UsuarioVocacional.pais == 'brasil'
                if filters.pais == 'brasil'
                else UsuarioVocacional.pais != 'brasil'
            )

        if filters.telefone:
            query_pre_cadastros = query_pre_cadastros.filter(
                UsuarioVocacional.telefone.ilike(
                    f'%{re.sub(r"\D", "", filters.telefone)}%'
                )
            )
        # if (
        #     str(current_user['nome_perfil']).lower()
        #     == PerfilEnum.vocacional_masculino.lower()
        # ):
        #     query_pre_cadastros = query_pre_cadastros.filter(
        #         UsuarioVocacional.genero == 'masculino'
        #     )

        # elif (
        #     str(current_user['nome_perfil']).lower()
        #     == PerfilEnum.vocacional_feminino.lower()
        # ):
        #     query_pre_cadastros = query_pre_cadastros.filter(
        #         UsuarioVocacional.genero == 'feminino'
        #     )
        # elif filters.genero:
        #     query_pre_cadastros = query_pre_cadastros.filter(
        #         UsuarioVocacional.genero == filters.genero
        #     )
        if filters.status:
            query_pre_cadastros = query_pre_cadastros.filter(
                EtapaVocacional.status == filters.status
            )

        if filters.nome:
            query_pre_cadastros = query_pre_cadastros.filter(
                UsuarioVocacional.nome.ilike(f'%{filters.nome}%')
            )

        if filters.email:
            query_pre_cadastros = query_pre_cadastros.filter(
                UsuarioVocacional.email.ilike(f'%{filters.email}%')
            )

        if filters.data_inicial:
            query_pre_cadastros = query_pre_cadastros.filter(
                self.__db.cast(EtapaVocacional.criado_em, self.__db.Date)
                >= self.__db.cast(filters.data_inicial, self.__db.Date)
            )

        if filters.data_final:
            query_pre_cadastros = query_pre_cadastros.filter(
                self.__db.cast(EtapaVocacional.criado_em, self.__db.Date)
                <= self.__db.cast(filters.data_final, self.__db.Date),
            )

        paginacao = query_pre_cadastros.paginate(
            page=filters.pagina, per_page=filters.por_pagina, error_out=False
        )

        return paginacao

    def detalhes_da_etapa_vocacional(
        self,
        etapa_vocacional: PassosVocacionalEnum,
        fk_usuario_vocacional_id: UUID,
    ):
        return (
            self.__db.session.query(
                EtapaVocacional.etapa,
                EtapaVocacional.status,
                EtapaVocacional.justificativa,
                label('lead_nome', Lead.nome),
                label('membro_id', Membro.id),
            )  # antes era usuario.nome
            .outerjoin(Membro, Membro.id == EtapaVocacional.fk_responsavel_id)
            .outerjoin(Lead, Lead.id == Membro.fk_lead_id)
            .filter(
                EtapaVocacional.etapa == etapa_vocacional,
                EtapaVocacional.fk_usuario_vocacional_id
                == fk_usuario_vocacional_id,
            )
            .order_by(self.__db.desc(EtapaVocacional.criado_em))
            .first()
        )

    def busca_etapa_atual(self, fk_usuario_vocacional_id) -> EtapaVocacional:
        etapa_atual = (
            self.__db.session.query(EtapaVocacional)
            .filter(
                EtapaVocacional.fk_usuario_vocacional_id
                == fk_usuario_vocacional_id
            )
            .order_by(self.__db.desc(EtapaVocacional.criado_em))
            .first()
        )
        return etapa_atual

    def busca_sacramento_vocacional(self, ficha_vocacional_id: UUID):
        sacramento = (
            self.__db.session.query(SacramentoVocacional)
            .filter(
                SacramentoVocacional.fk_ficha_vocacional_id
                == ficha_vocacional_id
            )
            .all()
        )

        return sacramento

    def verifica_usuario_vocacional(self, fk_usuario_vocacional_id):
        usuario_vocacional = self.__db.session.get(
            UsuarioVocacional, fk_usuario_vocacional_id
        )
        return usuario_vocacional

    def busca_vocacional(
        self, usuario_vocacional_id
    ) -> EtapaVocacional | None:
        busca_vocacional = (
            self.__db.session.query(
                UsuarioVocacional.nome,
                UsuarioVocacional.email,
                UsuarioVocacional.telefone,
                UsuarioVocacional.pais,
                UsuarioVocacional.id,
                EtapaVocacional.status,
                EtapaVocacional.etapa,
            )
            .join(
                EtapaVocacional,
                EtapaVocacional.fk_usuario_vocacional_id
                == UsuarioVocacional.id,
            )
            .filter(
                EtapaVocacional.fk_usuario_vocacional_id
                == usuario_vocacional_id,
            )
            .order_by(self.__db.desc(EtapaVocacional.criado_em))
            .first()
        )
        return busca_vocacional

    @staticmethod
    def aprovar_para_proximo_passo(etapa_atual: EtapaVocacional):
        etapa_atual.status = PassosVocacionalStatusEnum.aprovado
        # etapa_atual.fk_responsavel_id = current_user['id']
        etapa_atual.atualizado_em = datetime.now()

    @staticmethod
    def reprovar_para_proximo_passo(
        etapa_atual: EtapaVocacional, justificativa: str | None
    ):
        etapa_atual.status = PassosVocacionalStatusEnum.reprovado
        # etapa_atual.fk_responsavel_id = current_user['id']
        etapa_atual.atualizado_em = datetime.now()
        etapa_atual.justificativa = justificativa

    def registrar_desistencia(
        self, fk_usuario_vocacional_id: UUID, etapa: EtapaVocacional
    ):
        register_desistencia = EtapaVocacional(
            fk_usuario_vocacional_id=fk_usuario_vocacional_id,
            etapa=etapa.etapa,
            status=PassosVocacionalStatusEnum.desistencia,
            justificativa=None,
            fk_responsavel_id=None,
        )
        self.__db.session.add(register_desistencia)

    def busca_etapa_vocacional_por_usuario_e_etapa(
        self, fk_usuario_vocacional_id: UUID, etapa: str
    ):
        busca_etapa = (
            self.__db.session.query(EtapaVocacional)
            .filter(
                EtapaVocacional.etapa == etapa,
                EtapaVocacional.fk_usuario_vocacional_id
                == fk_usuario_vocacional_id,
            )
            .order_by(self.__db.desc(EtapaVocacional.criado_em))
            .first()
        )

        return busca_etapa

    def verifica_cadastro_vocacional(self, fk_usuario_vocacional_id):
        cadastro_vocacional = (
            self.__db.session.query(CadastroVocacional)
            .filter(
                CadastroVocacional.fk_usuario_vocacional_id
                == fk_usuario_vocacional_id,
            )
            .first()
        )

        return cadastro_vocacional

    def verifica_cpf_cadastrado(self, cpf):
        cpf_cadastrado = (
            self.__db.session.query(CadastroVocacional)
            .filter(CadastroVocacional.documento_identidade == cpf)
            .first()
        )

        return cpf_cadastrado

    def registrar_cadastro_vocacional(
        self, data_to_insert: Dict
    ) -> CadastroVocacional:
        new_endereco = Endereco(
            logradouro=data_to_insert.logradouro,
            numero=data_to_insert.numero,
            complemento=data_to_insert.complemento,
            bairro=data_to_insert.bairro,
            cidade=data_to_insert.cidade,
            estado=data_to_insert.estado,
            codigo_postal=data_to_insert.codigo_postal,
            pais=data_to_insert.pais,
            tipo_logradouro=data_to_insert.tipo_logradouro,
        )

        self.__db.session.add(new_endereco)
        self.__db.session.flush()

        new_cadastro_vocacional = CadastroVocacional(
            fk_usuario_vocacional_id=(data_to_insert.fk_usuario_vocacional_id),
            fk_endereco_id=new_endereco.id,
            data_nascimento=data_to_insert.data_nascimento,
            documento_identidade=data_to_insert.documento_identidade,
        )

        self.__db.session.add(new_cadastro_vocacional)
        self.__db.session.flush()

        new_etapa = EtapaVocacional(
            fk_usuario_vocacional_id=(data_to_insert.fk_usuario_vocacional_id),
            etapa=PassosVocacionalEnum.cadastro,
            status=PassosVocacionalStatusEnum.pendente,
            justificativa=None,
            fk_responsavel_id=None,
        )

        self.__db.session.add(new_etapa)

        return new_cadastro_vocacional

    def buscar_cadastros_vocacional(  # noqa: PLR0912
        self, filters: ListarCadastrosVocacionaisSchema
    ) -> Pagination:
        query_cadastros = (
            self.__db.session.query(
                UsuarioVocacional,
                CadastroVocacional,
                FichaVocacional,
                EtapaVocacional,
                Endereco,
            )
            .join(
                EtapaVocacional,
                EtapaVocacional.fk_usuario_vocacional_id
                == UsuarioVocacional.id,
            )
            .join(
                CadastroVocacional,
                CadastroVocacional.fk_usuario_vocacional_id
                == UsuarioVocacional.id,
            )
            .join(Endereco, Endereco.id == CadastroVocacional.fk_endereco_id)
            .outerjoin(
                FichaVocacional,
                FichaVocacional.fk_usuario_vocacional_id
                == UsuarioVocacional.id,
            )
            .filter(
                EtapaVocacional.etapa == PassosVocacionalEnum.cadastro,
                EtapaVocacional.status.in_([
                    PassosVocacionalStatusEnum.pendente,
                    PassosVocacionalStatusEnum.aprovado,
                ]),
            )
            .order_by(CadastroVocacional.criado_em.desc())
        )

        if filters.pais:
            query_cadastros = query_cadastros.filter(
                UsuarioVocacional.pais == 'brasil'
                if filters.pais == 'brasil'
                else UsuarioVocacional.pais != 'brasil'
            )

        if filters.telefone:
            query_cadastros = query_cadastros.filter(
                UsuarioVocacional.telefone.ilike(
                    f'%{re.sub(r"\D", "", filters.telefone)}%'
                )
            )

        # if (
        #     str(current_user['nome_perfil']).lower()
        #     == ProfilesEnum.vocacional_masculino.lower()
        # ):
        #     query_cadastros = query_cadastros.filter(
        #         UsuarioVocacional.genero == 'masculino'
        #     )

        # elif (
        #     str(current_user['nome_perfil']).lower()
        #     == ProfilesEnum.vocacional_feminino.lower()
        # ):
        #     query_cadastros = query_cadastros.filter(
        #         UsuarioVocacional.genero == 'feminino'
        #     )
        # elif filters.genero:
        #     query_cadastros = query_cadastros.filter(
        #         UsuarioVocacional.genero == filters.genero
        #     )

        if filters.status:
            query_cadastros = query_cadastros.filter(
                EtapaVocacional.status == filters.status
            )

        if filters.nome:
            query_cadastros = query_cadastros.filter(
                UsuarioVocacional.nome.ilike(f'%{filters.nome}%')
            )

        if filters.email:
            query_cadastros = query_cadastros.filter(
                UsuarioVocacional.email.ilike(f'%{filters.email}%')
            )

        if filters.data_inicial:
            query_cadastros = query_cadastros.filter(
                self.__db.cast(EtapaVocacional.criado_em, self.__db.Date)
                >= self.__db.cast(filters.data_inicial, self.__db.Date)
            )

        if filters.data_final:
            query_cadastros = query_cadastros.filter(
                self.__db.cast(EtapaVocacional.criado_em, self.__db.Date)
                <= self.__db.cast(filters.data_final, self.__db.Date),
            )

        if filters.documento_identidade:
            query_cadastros = query_cadastros.filter(
                CadastroVocacional.documento_identidade.ilike(
                    f'%{filters.documento_identidade}%'
                )
            )
        paginacao = query_cadastros.paginate(
            page=filters.pagina, per_page=filters.por_pagina, error_out=False
        )
        return paginacao

    def verifica_ficha_vocacional(
        self, usuario_vocacional_id
    ) -> FichaVocacional | None:
        ficha_vocacional = (
            self.__db.session.query(FichaVocacional)
            .filter(
                FichaVocacional.fk_usuario_vocacional_id
                == usuario_vocacional_id
            )
            .first()
        )

        return ficha_vocacional

    def registrar_ficha_vocacional(  # noqa: PLR0912
        self, data_ficha_vocacional: Dict, nome_foto_vocacional: str
    ):
        new_ficha_vocacional = FichaVocacional(
            fk_usuario_vocacional_id=(
                data_ficha_vocacional.fk_usuario_vocacional_id
            ),
            motivacao_instituto=data_ficha_vocacional.motivacao_instituto,
            motivacao_admissao_vocacional=(
                data_ficha_vocacional.motivacao_admissao_vocacional
            ),
            referencia_conhecimento_instituto=(
                data_ficha_vocacional.referencia_conhecimento_instituto
            ),
            identificacao_instituto=(
                data_ficha_vocacional.identificacao_instituto
            ),
            foto_vocacional=nome_foto_vocacional,
            seminario_realizado_em=(
                data_ficha_vocacional.seminario_realizado_em
            ),
            testemunho_conversao=(data_ficha_vocacional.testemunho_conversao),
            escolaridade=data_ficha_vocacional.escolaridade,
            profissao=data_ficha_vocacional.profissao,
            cursos=data_ficha_vocacional.cursos,
            rotina_diaria=data_ficha_vocacional.rotina_diaria,
            aceitacao_familiar=data_ficha_vocacional.aceitacao_familiar,
            estado_civil=data_ficha_vocacional.estado_civil,
            motivo_divorcio=data_ficha_vocacional.motivo_divorcio,
            deixou_religiao_anterior_em=(
                data_ficha_vocacional.deixou_religiao_anterior_em
            ),
            remedio_controlado_inicio=(
                data_ficha_vocacional.remedio_controlado_inicio
            ),
            remedio_controlado_termino=(
                data_ficha_vocacional.remedio_controlado_termino
            ),
            descricao_problema_saude=(
                data_ficha_vocacional.descricao_problema_saude
            ),
        )

        self.__db.session.add(new_ficha_vocacional)
        self.__db.session.flush()

        for sac in data_ficha_vocacional.sacramentos:
            add_sacramento = SacramentoVocacional(
                fk_ficha_vocacional_id=new_ficha_vocacional.id, nome=sac
            )

            self.__db.session.add(add_sacramento)
            self.__db.session.flush()

        new_etapa = EtapaVocacional(
            fk_usuario_vocacional_id=(
                data_ficha_vocacional.fk_usuario_vocacional_id
            ),
            etapa='ficha_vocacional',
            status='pendente',
            justificativa=None,
            fk_responsavel_id=None,
        )

        self.__db.session.add(new_etapa)

    def buscar_fichas_vocacionais(
        self, filters: ListarFichasVocacionaisSchema
    ) -> Pagination:
        subquery = (
            self.__db.session.query(
                EtapaVocacional.fk_usuario_vocacional_id,
                self.__db.func.max(EtapaVocacional.criado_em).label(
                    'max_criado_em'
                ),
            )
            .filter(
                EtapaVocacional.etapa == PassosVocacionalEnum.ficha_vocacional
            )
            .group_by(EtapaVocacional.fk_usuario_vocacional_id)
            .subquery()
        )

        query_fichas_vocacionais = (
            self.__db.session.query(
                UsuarioVocacional,
                CadastroVocacional,
                FichaVocacional,
                EtapaVocacional,
                Endereco,
            )
            .join(
                EtapaVocacional,
                EtapaVocacional.fk_usuario_vocacional_id
                == UsuarioVocacional.id,
            )
            .join(
                CadastroVocacional,
                CadastroVocacional.fk_usuario_vocacional_id
                == UsuarioVocacional.id,
            )
            .join(Endereco, Endereco.id == CadastroVocacional.fk_endereco_id)
            .join(
                FichaVocacional,
                FichaVocacional.fk_usuario_vocacional_id
                == UsuarioVocacional.id,
            )
            .join(
                subquery,
                (
                    EtapaVocacional.fk_usuario_vocacional_id
                    == subquery.c.fk_usuario_vocacional_id
                )
                & (EtapaVocacional.criado_em == subquery.c.max_criado_em),
            )
            .filter(EtapaVocacional.etapa == 'ficha_vocacional')
            .order_by(CadastroVocacional.criado_em.desc())
        )

        if filters.fk_usuario_vocacional_id:
            query_fichas_vocacionais = query_fichas_vocacionais.filter(
                UsuarioVocacional.id == filters.fk_usuario_vocacional_id
            )

        if filters.pais:
            query_fichas_vocacionais = query_fichas_vocacionais.filter(
                UsuarioVocacional.pais == 'brasil'
                if filters.pais == 'brasil'
                else UsuarioVocacional.pais != 'brasil'
            )

        if filters.telefone:
            query_fichas_vocacionais = query_fichas_vocacionais.filter(
                UsuarioVocacional.telefone.ilike(
                    f'%{re.sub(r"\D", "", filters.telefone)}%'
                )
            )

        if filters.genero:
            query_fichas_vocacionais = query_fichas_vocacionais.filter(
                UsuarioVocacional.genero == filters.genero
            )

        if filters.status:
            query_fichas_vocacionais = query_fichas_vocacionais.filter(
                EtapaVocacional.status == filters.status
            )

        if filters.nome:
            query_fichas_vocacionais = query_fichas_vocacionais.filter(
                UsuarioVocacional.nome.ilike(f'%{filters.nome}%')
            )

        if filters.email:
            query_fichas_vocacionais = query_fichas_vocacionais.filter(
                UsuarioVocacional.email.ilike(f'%{filters.email}%')
            )

        if filters.data_inicial:
            query_fichas_vocacionais = query_fichas_vocacionais.filter(
                self.__db.cast(FichaVocacional.criado_em, self.__db.Date)
                >= self.__db.cast(filters.data_inicial, self.__db.Date)
            )

        if filters.data_final:
            query_fichas_vocacionais = query_fichas_vocacionais.filter(
                self.__db.cast(FichaVocacional.criado_em, self.__db.Date)
                <= self.__db.cast(filters.data_final, self.__db.Date),
            )

        if filters.documento_identidade:
            query_fichas_vocacionais = query_fichas_vocacionais.filter(
                CadastroVocacional.documento_identidade.ilike(
                    f'%{filters.documento_identidade}%'
                )
            )

        paginacao = query_fichas_vocacionais.paginate(
            page=filters.pagina, per_page=filters.por_pagina, error_out=False
        )
        return paginacao

    def buscar_desistencias_vocacionais(
        self, filters: ListarDesistenciaVocacionaisSchema
    ) -> Pagination:
        desistencias = (
            self.__db.session.query(UsuarioVocacional, EtapaVocacional)
            .join(
                UsuarioVocacional,
                UsuarioVocacional.id
                == EtapaVocacional.fk_usuario_vocacional_id,
            )
            .filter(
                EtapaVocacional.status
                == PassosVocacionalStatusEnum.desistencia
            )
            .order_by(self.__db.desc(EtapaVocacional.criado_em))
        )

        if filters.etapa:
            desistencias = desistencias.filter(
                EtapaVocacional.etapa == filters.etapa
            )

        if filters.pais:
            desistencias = desistencias.filter(
                UsuarioVocacional.pais == 'brasil'
                if filters.pais == 'brasil'
                else UsuarioVocacional.pais != 'brasil'
            )

        if filters.telefone:
            desistencias = desistencias.filter(
                UsuarioVocacional.telefone.ilike(
                    f'%{re.sub(r"\D", "", filters.telefone)}%'
                )
            )

        if filters.genero:
            desistencias = desistencias.filter(
                UsuarioVocacional.genero == filters.genero
            )

        if filters.nome:
            desistencias = desistencias.filter(
                UsuarioVocacional.nome.ilike(f'%{filters.nome}%')
            )

        if filters.email:
            desistencias = desistencias.filter(
                UsuarioVocacional.email.ilike(f'%{filters.email}%')
            )

        if filters.data_inicial:
            desistencias = desistencias.filter(
                self.__db.cast(EtapaVocacional.criado_em, self.__db.Date)
                >= self.__db.cast(filters.data_inicial, self.__db.Date)
            )

        if filters.data_final:
            desistencias = desistencias.filter(
                self.__db.cast(EtapaVocacional.criado_em, self.__db.Date)
                <= self.__db.cast(filters.data_final, self.__db.Date),
            )

        paginacao = desistencias.paginate(
            page=filters.pagina, per_page=filters.por_pagina, error_out=False
        )

        return paginacao

    def buscar_vocacionais_recusados(
        self, filters: ListarVocacionaisRecusadosSchema
    ) -> Pagination:
        recusados = (
            self.__db.session.query(UsuarioVocacional, EtapaVocacional)
            .join(
                UsuarioVocacional,
                UsuarioVocacional.id
                == EtapaVocacional.fk_usuario_vocacional_id,
            )
            .filter(EtapaVocacional.status == 'reprovado')
            .order_by(self.__db.desc(EtapaVocacional.criado_em))
        )

        if filters.etapa:
            recusados = recusados.filter(
                EtapaVocacional.etapa == filters.etapa
            )

        if filters.pais:
            recusados = recusados.filter(
                UsuarioVocacional.pais == 'brasil'
                if filters.pais == 'brasil'
                else UsuarioVocacional.pais != 'brasil'
            )

        if filters.telefone:
            recusados = recusados.filter(
                UsuarioVocacional.telefone.ilike(
                    f'%{re.sub(r"\D", "", filters.telefone)}%'
                )
            )

        if filters.genero:
            recusados = recusados.filter(
                UsuarioVocacional.genero == filters.genero
            )

        if filters.nome:
            recusados = recusados.filter(
                UsuarioVocacional.nome.ilike(f'%{filters.nome}%')
            )

        if filters.email:
            recusados = recusados.filter(
                UsuarioVocacional.email.ilike(f'%{filters.email}%')
            )

        if filters.data_inicial:
            recusados = recusados.filter(
                self.__db.cast(EtapaVocacional.criado_em, self.__db.Date)
                >= self.__db.cast(filters.data_inicial, self.__db.Date)
            )

        if filters.data_final:
            recusados = recusados.filter(
                self.__db.cast(EtapaVocacional.criado_em, self.__db.Date)
                <= self.__db.cast(filters.data_final, self.__db.Date),
            )

        paginacao = recusados.paginate(
            page=filters.pagina, per_page=filters.por_pagina, error_out=False
        )

        return paginacao

    def busca_responsavel_atualizou_status(
        self, fk_usuario_atualizou_status_id: UUID, etapa: str
    ):
        responsavel = (
            self.__db.session.query(Membro)
            .join(
                EtapaVocacional, EtapaVocacional.fk_responsavel_id == Membro.id
            )
            .filter(
                Membro.id == fk_usuario_atualizou_status_id,
                EtapaVocacional.etapa == etapa,
            )
            .first()
        )

        responsavel_nome = (
            responsavel.nome_social if (responsavel is not None) else None
        )

        return responsavel_nome

    def busca_info_token(
        self, data_token_decodificado
    ) -> DecodificarTokenVocacionalSchema | None:
        resultado = (
            self.__db.session.query(
                UsuarioVocacional.nome,
                UsuarioVocacional.email,
                EtapaVocacional.etapa,
                EtapaVocacional.status,
                UsuarioVocacional.telefone,
                UsuarioVocacional.pais,
                UsuarioVocacional.id.label('fk_usuario_vocacional_id'),
            )
            .join(
                EtapaVocacional,
                EtapaVocacional.fk_usuario_vocacional_id
                == data_token_decodificado['fk_usuario_vocacional_id'],
            )
            .filter(
                UsuarioVocacional.id
                == data_token_decodificado['fk_usuario_vocacional_id']
            )
            .order_by(self.__db.desc(EtapaVocacional.criado_em))
            .first()
        )

        return resultado
