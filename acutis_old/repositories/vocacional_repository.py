from ast import Dict
import datetime
from http import HTTPStatus
import re
from typing import Tuple
from flask import request
from flask_jwt_extended import current_user
from flask_sqlalchemy import SQLAlchemy
from exceptions.error_types.http_bad_request import BadRequestError
from exceptions.error_types.http_conflict import ConflictError
from exceptions.error_types.http_not_found import NotFoundError
from exceptions.errors_handler import errors_handler
from handlers.vocacional.utils.reenvia_email_vocacional import envia_email_vocacional
from models.endereco import Endereco
from models.perfil import ProfilesEnum
from models.schemas.vocacional.get.decodificar_token_vocacional_schema import (
    DecodificarTokenVocacionalResponse,
)
from models.schemas.vocacional.get.listar_fichas_vocacionais_schema import (
    FichaVocacionalResponseSchema,
)
from models.schemas.vocacional.get.listar_cadastros_vocacionais_schema import (
    CadastroVocacionalResponse,
    ListarCadastrosVocacionaisResponse,
)

from models.schemas.vocacional.get.listar_pre_cadastros_schema import (
    ListarPreCadastrosResponse,
    GetPreCadastroSchema,
)
from models.usuario import Usuario
from models.vocacional import cadastro_vocacional
from models.vocacional.cadastro_vocacional import CadastroVocacional
from models.vocacional.etapa_vocacional import (
    EtapaVocacional,
    VocationalStepsEnum,
    VocationalStepsStatusEnum,
)
from models.vocacional.ficha_vocacional import FichaVocacional
from models.vocacional.sacramento_vocacional import SacramentoVocacional
from repositories.interfaces.vocacional.vocacional_repository_interface import (
    InterfaceVocacionalRepository,
)
from models.vocacional.usuario_vocacional import UsuarioVocacional, VocationalGendersEnum
from repositories.schemas.vocacional_schema import ImageEtapaVocacional
from services.factories import file_service_factory
from templates.email_templates import send_email_cadastro_vocacional_recebido, send_email_ficha_vocacional_recebido, send_email_pre_cadastro_vocacional_recebido
from utils.send_email import send_email
from utils.functions import get_current_time
from utils.validator import cpf_cnpj_validator


class VocacionalRepository(InterfaceVocacionalRepository):
    def __init__(self, db: SQLAlchemy):
        self.__db = db

    def pre_register_vocacional(self, data: dict) -> tuple[Dict, HTTPStatus]:
        try:

            email_used = (
                self.__db.session.query(UsuarioVocacional)
                .filter(UsuarioVocacional.email == data.email)
                .first()
            )

            if email_used != None:
                raise ConflictError("Email já cadastrado")

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
                etapa="pre_cadastro",
                status="pendente",
            )

            self.__db.session.add(new_etapa)

            html_pre_cadastro_recebido = send_email_pre_cadastro_vocacional_recebido(
                new_pre_cadastro.nome, ImageEtapaVocacional.ETAPA_PRE_CADASTRO.value
            )
            send_email(
                "Recebemos seu cadastro no processo vocacional",
                new_pre_cadastro.email,
                html_pre_cadastro_recebido,
                6,
            )

            self.__db.session.commit()
            return

        except Exception as e:
            self.__db.session.rollback()
            raise e

    def get_pre_cadastro_vocacional(
        self, filters: dict, page: int, per_page: int, filtros_permissoes
    ) -> tuple[Dict, HTTPStatus]:
        try:

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
                    UsuarioVocacional.id == EtapaVocacional.fk_usuario_vocacional_id,
                )
                .outerjoin(
                    CadastroVocacional,
                    CadastroVocacional.fk_usuario_vocacional_id == UsuarioVocacional.id,
                )
                .outerjoin(Endereco, Endereco.id == CadastroVocacional.fk_endereco_id)
                .outerjoin(
                    FichaVocacional,
                    FichaVocacional.fk_usuario_vocacional_id == UsuarioVocacional.id,
                )
                .filter(
                    EtapaVocacional.etapa == "pre_cadastro",
                    EtapaVocacional.status.in_(
                        [
                            VocationalStepsStatusEnum.PENDENTE,
                            VocationalStepsStatusEnum.APROVADO,
                        ]
                    ),
                )
                .order_by(self.__db.desc(EtapaVocacional.created_at))
            )

            if filters.pais:
                query_pre_cadastros = query_pre_cadastros.filter(
                    UsuarioVocacional.pais == "brasil"
                    if filters.pais == "brasil"
                    else UsuarioVocacional.pais != "brasil"
                )

            if filters.telefone:
                query_pre_cadastros = query_pre_cadastros.filter(
                    UsuarioVocacional.telefone.ilike(
                        f"%{re.sub(r'[^0-9]', '', filters.telefone)}%"
                    )
                )

            if (
                filtros_permissoes["acessar"] == VocationalGendersEnum.MASCULINO
            ):
                query_pre_cadastros = query_pre_cadastros.filter(
                    UsuarioVocacional.genero == VocationalGendersEnum.MASCULINO
                )

            elif (
                filtros_permissoes["acessar"] == VocationalGendersEnum.FEMININO
            ):
                query_pre_cadastros = query_pre_cadastros.filter(
                    UsuarioVocacional.genero == VocationalGendersEnum.FEMININO
                )
            else:
                if filters.genero:
                    query_pre_cadastros = query_pre_cadastros.filter(
                        UsuarioVocacional.genero == filters.genero
                    )

            if filters.status:
                query_pre_cadastros = query_pre_cadastros.filter(
                    EtapaVocacional.status == filters.status
                )

            if filters.nome:
                query_pre_cadastros = query_pre_cadastros.filter(
                    UsuarioVocacional.nome.ilike(f"%{filters.nome}%")
                )

            if filters.email:
                query_pre_cadastros = query_pre_cadastros.filter(
                    UsuarioVocacional.email.ilike(f"%{filters.email}%")
                )

            if filters.data_inicial:
                query_pre_cadastros = query_pre_cadastros.filter(
                    self.__db.cast(EtapaVocacional.created_at, self.__db.Date)
                    >= self.__db.cast(filters.data_inicial, self.__db.Date)
                )

            if filters.data_final:
                query_pre_cadastros = query_pre_cadastros.filter(
                    self.__db.cast(EtapaVocacional.created_at, self.__db.Date)
                    <= self.__db.cast(filters.data_final, self.__db.Date),
                )

            paginacao = query_pre_cadastros.paginate(
                page=page, per_page=per_page, error_out=False
            )

            lista_pre_cadastros = []

            for (
                usuario_vocacional,
                cadastro_vocacional,
                ficha_vocacional,
                etapa,
                endereco,
            ) in paginacao.items:

                pre_cadastro = GetPreCadastroSchema(
                    pais=usuario_vocacional.pais,
                    id=usuario_vocacional.id,
                    nome=usuario_vocacional.nome,
                    email=usuario_vocacional.email,
                    telefone=usuario_vocacional.telefone,
                    created_at=usuario_vocacional.created_at,
                    status=self.detalhes_da_etapa_vocacional(
                        VocationalStepsEnum.PRE_CADASTRO, usuario_vocacional.id
                    ).status,
                    responsavel=self.detalhes_da_etapa_vocacional(
                        VocationalStepsEnum.PRE_CADASTRO, usuario_vocacional.id
                    ).nome,
                    justificativa=self.detalhes_da_etapa_vocacional(
                        VocationalStepsEnum.PRE_CADASTRO, usuario_vocacional.id
                    ).justificativa,
                ).dict()

                if cadastro_vocacional != None:
                    cadastro = CadastroVocacionalResponse(
                        fk_usuario_vocacional_id=usuario_vocacional.id,
                        id=cadastro_vocacional.id,
                        nome=usuario_vocacional.nome,
                        email=usuario_vocacional.email,
                        telefone=usuario_vocacional.telefone,
                        genero=usuario_vocacional.genero,
                        created_at=cadastro_vocacional.created_at.strftime("%d/%m/%Y"),
                        data_nascimento=cadastro_vocacional.data_nascimento.strftime(
                            "%d/%m/%Y"
                        ),
                        documento_identidade=cadastro_vocacional.documento_identidade,
                        rua=endereco.rua,
                        cidade=endereco.cidade,
                        estado=endereco.estado,
                        bairro=endereco.bairro,
                        numero=endereco.numero,
                        cep=endereco.cep,
                        detalhe_estrangeiro=endereco.detalhe_estrangeiro,
                        pais=usuario_vocacional.pais,
                        status=self.detalhes_da_etapa_vocacional(
                            VocationalStepsEnum.CADASTRO, usuario_vocacional.id
                        ).status,
                        responsavel=self.detalhes_da_etapa_vocacional(
                            VocationalStepsEnum.CADASTRO, usuario_vocacional.id
                        ).nome,
                        justificativa=self.detalhes_da_etapa_vocacional(
                            VocationalStepsEnum.CADASTRO, usuario_vocacional.id
                        ).justificativa,
                    ).dict()
                else:
                    cadastro = {}

                if ficha_vocacional != None:
                    sacramentos_list = []

                    get_sacramentos = (
                        self.__db.session.query(SacramentoVocacional)
                        .filter(
                            SacramentoVocacional.fk_ficha_vocacional_id
                            == ficha_vocacional.id
                        )
                        .all()
                    )

                    for sacramento in get_sacramentos:
                        sacramentos_list.append(sacramento.nome)

                    ficha = FichaVocacionalResponseSchema(
                        motivacao_instituto=ficha_vocacional.motivacao_instituto,
                        fk_usuario_vocacional_id=ficha_vocacional.fk_usuario_vocacional_id,
                        motivacao_admissao_vocacional=ficha_vocacional.motivacao_admissao_vocacional,
                        referencia_conhecimento_instituto=ficha_vocacional.referencia_conhecimento_instituto,
                        identificacao_instituto=ficha_vocacional.identificacao_instituto,
                        seminario_realizado_em=(
                            ficha_vocacional.seminario_realizado_em.strftime("%d/%m/%Y")
                            if ficha_vocacional.seminario_realizado_em
                            else None
                        ),
                        testemunho_conversao=ficha_vocacional.testemunho_conversao,
                        escolaridade=ficha_vocacional.escolaridade,
                        profissao=ficha_vocacional.profissao,
                        cursos=ficha_vocacional.cursos,
                        rotina_diaria=ficha_vocacional.rotina_diaria,
                        aceitacao_familiar=ficha_vocacional.aceitacao_familiar,
                        estado_civil=ficha_vocacional.estado_civil,
                        motivo_divorcio=ficha_vocacional.motivo_divorcio,
                        deixou_religiao_anterior_em=(
                            ficha_vocacional.deixou_religiao_anterior_em.strftime(
                                "%d/%m/%Y"
                            )
                            if ficha_vocacional.deixou_religiao_anterior_em
                            else None
                        ),
                        remedio_controlado_inicio=(
                            ficha_vocacional.remedio_controlado_inicio.strftime(
                                "%d/%m/%Y"
                            )
                            if ficha_vocacional.remedio_controlado_inicio
                            else None
                        ),
                        remedio_controlado_termino=(
                            ficha_vocacional.remedio_controlado_termino.strftime(
                                "%d/%m/%Y"
                            )
                            if ficha_vocacional.remedio_controlado_termino
                            else None
                        ),
                        descricao_problema_saude=ficha_vocacional.descricao_problema_saude,
                        foto_vocacional=self.__foto_vocacional(
                            ficha_vocacional.foto_vocacional
                        ),
                        sacramentos=sacramentos_list,
                        status=self.detalhes_da_etapa_vocacional(
                            VocationalStepsEnum.FICHA_VOCACIONAL, usuario_vocacional.id
                        ).status,
                        responsavel=self.detalhes_da_etapa_vocacional(
                            VocationalStepsEnum.FICHA_VOCACIONAL, usuario_vocacional.id
                        ).nome,
                        justificativa=self.detalhes_da_etapa_vocacional(
                            VocationalStepsEnum.FICHA_VOCACIONAL, usuario_vocacional.id
                        ).justificativa,
                    ).dict()
                else:
                    ficha = {}

                lista_pre_cadastros.append(
                    {
                        "pre_cadastro": pre_cadastro,
                        "cadastro_vocacional": cadastro,
                        "ficha_do_vocacional": ficha,
                    }
                )

            response = {
                "pre_cadastros": lista_pre_cadastros,
                "page": paginacao.page,
                "total": paginacao.total,
            }

            return response, HTTPStatus.OK

        except Exception as e:
            raise e

    def register_cadastro_vocacional(
        self, data_to_insert: Dict
    ) -> tuple[dict, HTTPStatus]:

        try:

            vocacional_user = self.get_usuario_vocacional(
                data_to_insert.fk_usuario_vocacional_id
            )

            self.__verify_pre_cadastro_aproved(
                data_to_insert.fk_usuario_vocacional_id, "pre_cadastro"
            )

            self.__verify_cadastro_vocacional_alredy_register(
                data_to_insert.fk_usuario_vocacional_id,
                data_to_insert.documento_identidade,
            )

            if vocacional_user.pais == "brasil":
                cpf_cnpj_validator(data_to_insert.documento_identidade, "cpf")

            new_endereco = Endereco(
                rua=data_to_insert.rua,
                numero=data_to_insert.numero,
                complemento=data_to_insert.complemento,
                bairro=data_to_insert.bairro,
                cidade=data_to_insert.cidade,
                estado=data_to_insert.estado,
                cep=data_to_insert.cep,
                detalhe_estrangeiro=data_to_insert.detalhe_estrangeiro,
            )

            self.__db.session.add(new_endereco)
            self.__db.session.flush()

            new_cadastro_vocacional = CadastroVocacional(
                fk_usuario_vocacional_id=data_to_insert.fk_usuario_vocacional_id,
                fk_endereco_id=new_endereco.id,
                data_nascimento=data_to_insert.data_nascimento,
                documento_identidade=data_to_insert.documento_identidade,
            )

            self.__db.session.add(new_cadastro_vocacional)
            self.__db.session.flush()

            new_etapa = EtapaVocacional(
                fk_usuario_vocacional_id=data_to_insert.fk_usuario_vocacional_id,
                etapa="cadastro",
                status="pendente",
            )

            self.__db.session.add(new_etapa)
            self.__db.session.commit()
            
            html_cadastro_recebido = send_email_cadastro_vocacional_recebido(
                vocacional_user.nome, ImageEtapaVocacional.ETAPA_CADASTRO.value
            )
            send_email(
                "Recebemos sua ficha de cadastro no processo vocacional",
                vocacional_user.email,
                html_cadastro_recebido,
                6,
            )

            return {"msg": "Cadastro vocacional realizado com sucesso."}, HTTPStatus.OK

        except Exception as e:
            self.__db.session.rollback()
            raise e

    def __verify_cadastro_vocacional_alredy_register(
        self, fk_usuario_vocacional_id, cpf
    ) -> None:
        register_exists = (
            self.__db.session.query(CadastroVocacional)
            .filter(
                CadastroVocacional.fk_usuario_vocacional_id == fk_usuario_vocacional_id,
            )
            .first()
        )

        if register_exists != None:
            raise ConflictError("Cadastro vocacional já registrado anteriormente.")

        cpf_alredy_exists = (
            self.__db.session.query(CadastroVocacional)
            .filter(CadastroVocacional.documento_identidade == cpf)
            .first()
        )

        if (
            cpf_alredy_exists != None
            and cpf_alredy_exists.fk_usuario_vocacional_id != fk_usuario_vocacional_id
        ):
            raise ConflictError("Número do documento de identificação já cadastrado.")

    def __verify_pre_cadastro_aproved(self, fk_usuario_vocacional_id: int, etapa: str):
        get_pre_cadastro = (
            self.__db.session.query(EtapaVocacional)
            .filter(
                EtapaVocacional.etapa == etapa,
                EtapaVocacional.fk_usuario_vocacional_id == fk_usuario_vocacional_id,
            )
            .order_by(self.__db.desc(EtapaVocacional.created_at))
            .first()
        )

        if get_pre_cadastro is None:
            raise NotFoundError(
                "Cadastro ou pré cadastro não encontrado, é necessário preencher o pré cadastro antes do cadastro."
            )

        if get_pre_cadastro.status == "desistencia":
            raise ConflictError(
                "Não é possível prosseguir pois encontramos um registro de desistência no seu processo vocacional."
            )

        if get_pre_cadastro.status == "pendente":
            raise ConflictError(f"É necessário ter o {etapa} aprovado para continuar.")

        if get_pre_cadastro.status == "reprovado":
            raise ConflictError(
                "Não é possível prosseguir pois seu cadastrado foi marcado como recusado anteriomente."
            )

    def get_all_cadastro_vocacional(
        self, filters: dict, page: int, per_page: int, filtros_permissoes
    ) -> Tuple[dict, HTTPStatus]:
        try:
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
                    EtapaVocacional.fk_usuario_vocacional_id == UsuarioVocacional.id,
                )
                .join(
                    CadastroVocacional,
                    CadastroVocacional.fk_usuario_vocacional_id == UsuarioVocacional.id,
                )
                .join(Endereco, Endereco.id == CadastroVocacional.fk_endereco_id)
                .outerjoin(
                    FichaVocacional,
                    FichaVocacional.fk_usuario_vocacional_id == UsuarioVocacional.id,
                )
                .filter(
                    EtapaVocacional.etapa == "cadastro",
                    EtapaVocacional.status.in_(
                        [
                            VocationalStepsStatusEnum.PENDENTE,
                            VocationalStepsStatusEnum.APROVADO,
                        ]
                    ),
                )
                .order_by(CadastroVocacional.created_at.desc())
            )

            if filters.pais:
                query_cadastros = query_cadastros.filter(
                    UsuarioVocacional.pais == "brasil"
                    if filters.pais == "brasil"
                    else UsuarioVocacional.pais != "brasil"
                )

            if filters.telefone:
                query_cadastros = query_cadastros.filter(
                    UsuarioVocacional.telefone.ilike(
                        f"%{re.sub(r'[^0-9]', '', filters.telefone)}%"
                    )
                )

            if (
                filtros_permissoes["acessar"] == VocationalGendersEnum.MASCULINO
            ):
                query_cadastros = query_cadastros.filter(
                    UsuarioVocacional.genero == VocationalGendersEnum.MASCULINO
                )

            elif (
                filtros_permissoes["acessar"] == VocationalGendersEnum.FEMININO
            ):
                query_cadastros = query_cadastros.filter(
                    UsuarioVocacional.genero == VocationalGendersEnum.FEMININO
                )
            else:
                if filters.genero:
                    query_cadastros = query_cadastros.filter(
                        UsuarioVocacional.genero == filters.genero
                    )

            if filters.status:
                query_cadastros = query_cadastros.filter(
                    EtapaVocacional.status == filters.status
                )

            if filters.nome:
                query_cadastros = query_cadastros.filter(
                    UsuarioVocacional.nome.ilike(f"%{filters.nome}%")
                )

            if filters.email:
                query_cadastros = query_cadastros.filter(
                    UsuarioVocacional.email.ilike(f"%{filters.email}%")
                )

            if filters.data_inicial:
                query_cadastros = query_cadastros.filter(
                    self.__db.cast(EtapaVocacional.created_at, self.__db.Date)
                    >= self.__db.cast(filters.data_inicial, self.__db.Date)
                )

            if filters.data_final:
                query_cadastros = query_cadastros.filter(
                    self.__db.cast(EtapaVocacional.created_at, self.__db.Date)
                    <= self.__db.cast(filters.data_final, self.__db.Date),
                )

            if filters.documento_identidade:
                query_cadastros = query_cadastros.filter(
                    CadastroVocacional.documento_identidade.ilike(
                        f"%{filters.documento_identidade}%"
                    )
                )

            paginacao = query_cadastros.paginate(
                page=page, per_page=per_page, error_out=False
            )

            lista_cadastros_vocacionais = []

            for (
                usuario_vocacional,
                cadastro_vocacional,
                ficha_vocacional,
                etapa,
                endereco,
            ) in paginacao.items:

                pre_cadastro = GetPreCadastroSchema(
                    pais=usuario_vocacional.pais,
                    id=usuario_vocacional.id,
                    nome=usuario_vocacional.nome,
                    email=usuario_vocacional.email,
                    telefone=usuario_vocacional.telefone,
                    created_at=usuario_vocacional.created_at,
                    status=self.detalhes_da_etapa_vocacional(
                        VocationalStepsEnum.PRE_CADASTRO, usuario_vocacional.id
                    ).status,
                    responsavel=self.detalhes_da_etapa_vocacional(
                        VocationalStepsEnum.PRE_CADASTRO, usuario_vocacional.id
                    ).nome,
                    justificativa=self.detalhes_da_etapa_vocacional(
                        VocationalStepsEnum.PRE_CADASTRO, usuario_vocacional.id
                    ).justificativa,
                ).dict()

                if cadastro_vocacional != None:
                    cadastro = CadastroVocacionalResponse(
                        fk_usuario_vocacional_id=usuario_vocacional.id,
                        id=cadastro_vocacional.id,
                        nome=usuario_vocacional.nome,
                        email=usuario_vocacional.email,
                        telefone=usuario_vocacional.telefone,
                        genero=usuario_vocacional.genero,
                        created_at=cadastro_vocacional.created_at.strftime("%d/%m/%Y"),
                        data_nascimento=cadastro_vocacional.data_nascimento.strftime(
                            "%d/%m/%Y"
                        ),
                        documento_identidade=cadastro_vocacional.documento_identidade,
                        rua=endereco.rua,
                        cidade=endereco.cidade,
                        estado=endereco.estado,
                        bairro=endereco.bairro,
                        numero=endereco.numero,
                        cep=endereco.cep,
                        detalhe_estrangeiro=endereco.detalhe_estrangeiro,
                        pais=usuario_vocacional.pais,
                        status=self.detalhes_da_etapa_vocacional(
                            VocationalStepsEnum.CADASTRO, usuario_vocacional.id
                        ).status,
                        responsavel=self.detalhes_da_etapa_vocacional(
                            VocationalStepsEnum.CADASTRO, usuario_vocacional.id
                        ).nome,
                        justificativa=self.detalhes_da_etapa_vocacional(
                            VocationalStepsEnum.CADASTRO, usuario_vocacional.id
                        ).justificativa,
                    ).dict()
                else:
                    cadastro = {}

                if ficha_vocacional != None:
                    sacramentos_list = []

                    get_sacramentos = (
                        self.__db.session.query(SacramentoVocacional)
                        .filter(
                            SacramentoVocacional.fk_ficha_vocacional_id
                            == ficha_vocacional.id
                        )
                        .all()
                    )

                    for sacramento in get_sacramentos:
                        sacramentos_list.append(sacramento.nome)

                    ficha = FichaVocacionalResponseSchema(
                        motivacao_instituto=ficha_vocacional.motivacao_instituto,
                        fk_usuario_vocacional_id=ficha_vocacional.fk_usuario_vocacional_id,
                        motivacao_admissao_vocacional=ficha_vocacional.motivacao_admissao_vocacional,
                        referencia_conhecimento_instituto=ficha_vocacional.referencia_conhecimento_instituto,
                        identificacao_instituto=ficha_vocacional.identificacao_instituto,
                        seminario_realizado_em=(
                            ficha_vocacional.seminario_realizado_em.strftime("%d/%m/%Y")
                            if ficha_vocacional.seminario_realizado_em
                            else None
                        ),
                        testemunho_conversao=ficha_vocacional.testemunho_conversao,
                        escolaridade=ficha_vocacional.escolaridade,
                        profissao=ficha_vocacional.profissao,
                        cursos=ficha_vocacional.cursos,
                        rotina_diaria=ficha_vocacional.rotina_diaria,
                        aceitacao_familiar=ficha_vocacional.aceitacao_familiar,
                        estado_civil=ficha_vocacional.estado_civil,
                        motivo_divorcio=ficha_vocacional.motivo_divorcio,
                        deixou_religiao_anterior_em=(
                            ficha_vocacional.deixou_religiao_anterior_em.strftime(
                                "%d/%m/%Y"
                            )
                            if ficha_vocacional.deixou_religiao_anterior_em
                            else None
                        ),
                        remedio_controlado_inicio=(
                            ficha_vocacional.remedio_controlado_inicio.strftime(
                                "%d/%m/%Y"
                            )
                            if ficha_vocacional.remedio_controlado_inicio
                            else None
                        ),
                        remedio_controlado_termino=(
                            ficha_vocacional.remedio_controlado_termino.strftime(
                                "%d/%m/%Y"
                            )
                            if ficha_vocacional.remedio_controlado_termino
                            else None
                        ),
                        descricao_problema_saude=ficha_vocacional.descricao_problema_saude,
                        foto_vocacional=self.__foto_vocacional(
                            ficha_vocacional.foto_vocacional
                        ),
                        sacramentos=sacramentos_list,
                        status=self.detalhes_da_etapa_vocacional(
                            VocationalStepsEnum.FICHA_VOCACIONAL, usuario_vocacional.id
                        ).status,
                        responsavel=self.detalhes_da_etapa_vocacional(
                            VocationalStepsEnum.FICHA_VOCACIONAL, usuario_vocacional.id
                        ).nome,
                        justificativa=self.detalhes_da_etapa_vocacional(
                            VocationalStepsEnum.FICHA_VOCACIONAL, usuario_vocacional.id
                        ).justificativa,
                    ).dict()
                else:
                    ficha = {}

                lista_cadastros_vocacionais.append(
                    {
                        "pre_cadastro": pre_cadastro,
                        "cadastro_vocacional": cadastro,
                        "ficha_do_vocacional": ficha,
                    }
                )

            response = {
                "cadastros_vocacionais": lista_cadastros_vocacionais,
                "page": paginacao.page,
                "total": paginacao.total,
            }

            return response, HTTPStatus.OK

        except Exception as e:
            return errors_handler(e)

    def register_ficha_vocacional(
        self, data_ficha_vocacional: Dict, nome_foto_vocacional: str
    ) -> tuple[Dict, HTTPStatus]:

        try:

            usuario_vocacional = (
                self.__db.session.query(UsuarioVocacional)
                .filter(
                    UsuarioVocacional.id
                    == data_ficha_vocacional.fk_usuario_vocacional_id
                )
                .first()
            )
            if usuario_vocacional is None:
                raise NotFoundError(
                    "Usuário vocacional não encontrado, é necessário preencher o pré cadastro para seguir."
                )

            ficha_preenchida = (
                self.__db.session.query(FichaVocacional)
                .filter(
                    FichaVocacional.fk_usuario_vocacional_id
                    == data_ficha_vocacional.fk_usuario_vocacional_id
                )
                .first()
            )
            if ficha_preenchida is not None:
                raise ConflictError("Fichal vocacional já preenchida.")

            self.__verify_pre_cadastro_aproved(
                data_ficha_vocacional.fk_usuario_vocacional_id, "cadastro"
            )

            new_ficha_vocacional = FichaVocacional(
                fk_usuario_vocacional_id=data_ficha_vocacional.fk_usuario_vocacional_id,
                motivacao_instituto=data_ficha_vocacional.motivacao_instituto,
                motivacao_admissao_vocacional=data_ficha_vocacional.motivacao_admissao_vocacional,
                referencia_conhecimento_instituto=data_ficha_vocacional.referencia_conhecimento_instituto,
                identificacao_instituto=data_ficha_vocacional.identificacao_instituto,
                foto_vocacional=nome_foto_vocacional,
                seminario_realizado_em=data_ficha_vocacional.seminario_realizado_em,
                testemunho_conversao=data_ficha_vocacional.testemunho_conversao,
                escolaridade=data_ficha_vocacional.escolaridade,
                profissao=data_ficha_vocacional.profissao,
                cursos=data_ficha_vocacional.cursos,
                rotina_diaria=data_ficha_vocacional.rotina_diaria,
                aceitacao_familiar=data_ficha_vocacional.aceitacao_familiar,
                estado_civil=data_ficha_vocacional.estado_civil,
                motivo_divorcio=data_ficha_vocacional.motivo_divorcio,
                deixou_religiao_anterior_em=data_ficha_vocacional.deixou_religiao_anterior_em,
                remedio_controlado_inicio=data_ficha_vocacional.remedio_controlado_inicio,
                remedio_controlado_termino=data_ficha_vocacional.remedio_controlado_termino,
                descricao_problema_saude=data_ficha_vocacional.descricao_problema_saude,
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
                fk_usuario_vocacional_id=data_ficha_vocacional.fk_usuario_vocacional_id,
                etapa="ficha_vocacional",
                status="pendente",
            )

            self.__db.session.add(new_etapa)
            self.__db.session.commit()

            html_cadastro_recebido = send_email_ficha_vocacional_recebido(
                usuario_vocacional.nome, ImageEtapaVocacional.ETAPA_FICHA_VOCACIONAL.value
            )
            send_email(
                "Recebemos sua ficha de cadastro no processo vocacional",
                usuario_vocacional.email,
                html_cadastro_recebido,
                6,
            )

            return {
                "msg": "Ficha vocacional preenchida com sucesso."
            }, HTTPStatus.CREATED

        except Exception as e:
            self.__db.session.rollback()
            return errors_handler(e)

    def get__all_fichas_vocacionais(
        self, filters: dict, page, per_page, filtros_permissoes
    ) -> Tuple[Dict, HTTPStatus]:

        subquery = (
            self.__db.session.query(
                EtapaVocacional.fk_usuario_vocacional_id,
                self.__db.func.max(EtapaVocacional.created_at).label("max_created_at"),
            )
            .filter(EtapaVocacional.etapa == "ficha_vocacional")
            .group_by(EtapaVocacional.fk_usuario_vocacional_id)
            .subquery()
        )

        query_fichas_vocacionais = (
            self.__db.session.query(
                UsuarioVocacional,
                EtapaVocacional,
                CadastroVocacional,
                FichaVocacional,
                Endereco,
            )
            .join(
                EtapaVocacional,
                EtapaVocacional.fk_usuario_vocacional_id == UsuarioVocacional.id,
            )
            .join(
                CadastroVocacional,
                CadastroVocacional.fk_usuario_vocacional_id == UsuarioVocacional.id,
            )
            .join(Endereco, Endereco.id == CadastroVocacional.fk_endereco_id)
            .join(
                FichaVocacional,
                FichaVocacional.fk_usuario_vocacional_id == UsuarioVocacional.id,
            )
            .join(
                subquery,
                (
                    EtapaVocacional.fk_usuario_vocacional_id
                    == subquery.c.fk_usuario_vocacional_id
                )
                & (EtapaVocacional.created_at == subquery.c.max_created_at),
            )
            .filter(EtapaVocacional.etapa == "ficha_vocacional")
            .order_by(CadastroVocacional.created_at.desc())
        )

        if filters.fk_usuario_vocacional_id:
            query_fichas_vocacionais = query_fichas_vocacionais.filter(
                UsuarioVocacional.id == filters.fk_usuario_vocacional_id
            )

        if filters.pais:
            query_fichas_vocacionais = query_fichas_vocacionais.filter(
                UsuarioVocacional.pais == "brasil"
                if filters.pais == "brasil"
                else UsuarioVocacional.pais != "brasil"
            )

        if filters.telefone:
            query_fichas_vocacionais = query_fichas_vocacionais.filter(
                UsuarioVocacional.telefone.ilike(
                    f"%{re.sub(r'[^0-9]', '', filters.telefone)}%"
                )
            )

        if filtros_permissoes["acessar"] == VocationalGendersEnum.MASCULINO:
            query_fichas_vocacionais = query_fichas_vocacionais.filter(
                UsuarioVocacional.genero == VocationalGendersEnum.MASCULINO
            )

        elif filtros_permissoes["acessar"] == VocationalGendersEnum.FEMININO:
            query_fichas_vocacionais = query_fichas_vocacionais.filter(
                UsuarioVocacional.genero == VocationalGendersEnum.FEMININO
            )
        else:
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
                UsuarioVocacional.nome.ilike(f"%{filters.nome}%")
            )

        if filters.email:
            query_fichas_vocacionais = query_fichas_vocacionais.filter(
                UsuarioVocacional.email.ilike(f"%{filters.email}%")
            )

        if filters.data_inicial:
            query_fichas_vocacionais = query_fichas_vocacionais.filter(
                self.__db.cast(FichaVocacional.created_at, self.__db.Date)
                >= self.__db.cast(filters.data_inicial, self.__db.Date)
            )

        if filters.data_final:
            query_fichas_vocacionais = query_fichas_vocacionais.filter(
                self.__db.cast(FichaVocacional.created_at, self.__db.Date)
                <= self.__db.cast(filters.data_final, self.__db.Date),
            )

        if filters.documento_identidade:
            query_fichas_vocacionais = query_fichas_vocacionais.filter(
                CadastroVocacional.documento_identidade.ilike(
                    f"%{filters.documento_identidade}%"
                )
            )

        pagination = query_fichas_vocacionais.paginate(
            page=page, per_page=per_page, error_out=False
        )

        fichas_vocacionais = []

        for (
            usuario_vocacional,
            etapa,
            cadastro,
            ficha_vocacional,
            endereco,
        ) in pagination.items:

            sacramentos_list = []

            get_sacramentos = (
                self.__db.session.query(SacramentoVocacional)
                .filter(
                    SacramentoVocacional.fk_ficha_vocacional_id == ficha_vocacional.id
                )
                .all()
            )

            for sacramento in get_sacramentos:
                sacramentos_list.append(sacramento.nome)

            ficha = FichaVocacionalResponseSchema(
                motivacao_instituto=ficha_vocacional.motivacao_instituto,
                fk_usuario_vocacional_id=ficha_vocacional.fk_usuario_vocacional_id,
                motivacao_admissao_vocacional=ficha_vocacional.motivacao_admissao_vocacional,
                referencia_conhecimento_instituto=ficha_vocacional.referencia_conhecimento_instituto,
                identificacao_instituto=ficha_vocacional.identificacao_instituto,
                seminario_realizado_em=(
                    ficha_vocacional.seminario_realizado_em.strftime("%d/%m/%Y")
                    if ficha_vocacional.seminario_realizado_em
                    else None
                ),
                testemunho_conversao=ficha_vocacional.testemunho_conversao,
                escolaridade=ficha_vocacional.escolaridade,
                profissao=ficha_vocacional.profissao,
                cursos=ficha_vocacional.cursos,
                rotina_diaria=ficha_vocacional.rotina_diaria,
                aceitacao_familiar=ficha_vocacional.aceitacao_familiar,
                estado_civil=ficha_vocacional.estado_civil,
                motivo_divorcio=ficha_vocacional.motivo_divorcio,
                deixou_religiao_anterior_em=(
                    ficha_vocacional.deixou_religiao_anterior_em.strftime("%d/%m/%Y")
                    if ficha_vocacional.deixou_religiao_anterior_em
                    else None
                ),
                remedio_controlado_inicio=(
                    ficha_vocacional.remedio_controlado_inicio.strftime("%d/%m/%Y")
                    if ficha_vocacional.remedio_controlado_inicio
                    else None
                ),
                remedio_controlado_termino=(
                    ficha_vocacional.remedio_controlado_termino.strftime("%d/%m/%Y")
                    if ficha_vocacional.remedio_controlado_termino
                    else None
                ),
                descricao_problema_saude=ficha_vocacional.descricao_problema_saude,
                foto_vocacional=self.__foto_vocacional(
                    ficha_vocacional.foto_vocacional
                ),
                sacramentos=sacramentos_list,
                status=self.detalhes_da_etapa_vocacional(
                    VocationalStepsEnum.FICHA_VOCACIONAL, usuario_vocacional.id
                ).status,
                responsavel=self.detalhes_da_etapa_vocacional(
                    VocationalStepsEnum.FICHA_VOCACIONAL, usuario_vocacional.id
                ).nome,
                justificativa=self.detalhes_da_etapa_vocacional(
                    VocationalStepsEnum.FICHA_VOCACIONAL, usuario_vocacional.id
                ).justificativa,
            ).dict()

            cadastro = CadastroVocacionalResponse(
                fk_usuario_vocacional_id=usuario_vocacional.id,
                id=cadastro.id,
                nome=usuario_vocacional.nome,
                email=usuario_vocacional.email,
                telefone=usuario_vocacional.telefone,
                genero=usuario_vocacional.genero,
                created_at=cadastro.created_at.strftime("%d/%m/%Y"),
                data_nascimento=cadastro.data_nascimento.strftime("%d/%m/%Y"),
                documento_identidade=cadastro.documento_identidade,
                rua=endereco.rua,
                cidade=endereco.cidade,
                estado=endereco.estado,
                bairro=endereco.bairro,
                numero=endereco.numero,
                cep=endereco.cep,
                detalhe_estrangeiro=endereco.detalhe_estrangeiro,
                pais=usuario_vocacional.pais,
                status=self.detalhes_da_etapa_vocacional(
                    VocationalStepsEnum.CADASTRO, usuario_vocacional.id
                ).status,
                responsavel=self.detalhes_da_etapa_vocacional(
                    VocationalStepsEnum.CADASTRO, usuario_vocacional.id
                ).nome,
                justificativa=self.detalhes_da_etapa_vocacional(
                    VocationalStepsEnum.CADASTRO, usuario_vocacional.id
                ).justificativa,
            ).dict()

            pre_cadastro = GetPreCadastroSchema(
                pais=usuario_vocacional.pais,
                id=usuario_vocacional.id,
                nome=usuario_vocacional.nome,
                email=usuario_vocacional.email,
                telefone=usuario_vocacional.telefone,
                created_at=usuario_vocacional.created_at,
                status=self.detalhes_da_etapa_vocacional(
                    VocationalStepsEnum.PRE_CADASTRO, usuario_vocacional.id
                ).status,
                responsavel=self.detalhes_da_etapa_vocacional(
                    VocationalStepsEnum.PRE_CADASTRO, usuario_vocacional.id
                ).nome,
                justificativa=self.detalhes_da_etapa_vocacional(
                    VocationalStepsEnum.PRE_CADASTRO, usuario_vocacional.id
                ).justificativa,
            ).dict()

            fichas_vocacionais.append(
                {
                    "cadastro_vocacional": cadastro,
                    "ficha_do_vocacional": ficha,
                    "pre_cadastro": pre_cadastro,
                }
            )

        response = {
            "fichas_vocacionais": fichas_vocacionais,
            "total": pagination.total,
            "page": pagination.page,
        }

        return response, HTTPStatus.OK

    def __foto_vocacional(self, nome_arquivo):
        s3_client = file_service_factory()
        return s3_client.get_public_url(nome_arquivo)

    def __get_responsavel_update_status(
        self, fk_usuario_update_status_id: int, etapa: str
    ):

        responsavel = (
            self.__db.session.query(Usuario)
            .join(EtapaVocacional, EtapaVocacional.responsavel == Usuario.id)
            .filter(
                Usuario.id == fk_usuario_update_status_id,
                EtapaVocacional.etapa == etapa,
            )
            .first()
        )

        responsavel_nome = responsavel.nome if responsavel != None else None

        return responsavel_nome

    def get_desistencias_vocacionais(
        self, filters: dict, page: int, per_page: int, filtros_permissoes
    ) -> Tuple[dict, HTTPStatus]:

        desistencias = (
            self.__db.session.query(
                UsuarioVocacional,
                CadastroVocacional,
                FichaVocacional,
                EtapaVocacional,
                Endereco,
            )
            .join(
                UsuarioVocacional,
                UsuarioVocacional.id == EtapaVocacional.fk_usuario_vocacional_id,
            )
            .outerjoin(
                CadastroVocacional,
                CadastroVocacional.fk_usuario_vocacional_id == UsuarioVocacional.id,
            )
            .outerjoin(Endereco, Endereco.id == CadastroVocacional.fk_endereco_id)
            .outerjoin(
                FichaVocacional,
                FichaVocacional.fk_usuario_vocacional_id == UsuarioVocacional.id,
            )
            .filter(EtapaVocacional.status == "desistencia")
            .order_by(self.__db.desc(EtapaVocacional.created_at))
        )

        if filters.pais:
            desistencias = desistencias.filter(
                UsuarioVocacional.pais == "brasil"
                if filters.pais == "brasil"
                else UsuarioVocacional.pais != "brasil"
            )

        if filters.telefone:
            desistencias = desistencias.filter(
                UsuarioVocacional.telefone.ilike(
                    f"%{re.sub(r'[^0-9]', '', filters.telefone)}%"
                )
            )

        if filtros_permissoes["acessar"] == VocationalGendersEnum.MASCULINO:
            desistencias = desistencias.filter(
                UsuarioVocacional.genero == VocationalGendersEnum.MASCULINO
            )

        elif filtros_permissoes["acessar"] == VocationalGendersEnum.FEMININO:
            desistencias = desistencias.filter(
                UsuarioVocacional.genero == VocationalGendersEnum.FEMININO
            )
        else:
            if filters.genero:
                desistencias = desistencias.filter(
                    UsuarioVocacional.genero == filters.genero
                )

        if filters.status:
            desistencias = desistencias.filter(EtapaVocacional.status == filters.status)

        if filters.nome:
            desistencias = desistencias.filter(
                UsuarioVocacional.nome.ilike(f"%{filters.nome}%")
            )

        if filters.email:
            desistencias = desistencias.filter(
                UsuarioVocacional.email.ilike(f"%{filters.email}%")
            )

        if filters.data_inicial:
            desistencias = desistencias.filter(
                self.__db.cast(EtapaVocacional.created_at, self.__db.Date)
                >= self.__db.cast(filters.data_inicial, self.__db.Date)
            )

        if filters.data_final:
            desistencias = desistencias.filter(
                self.__db.cast(EtapaVocacional.created_at, self.__db.Date)
                <= self.__db.cast(filters.data_final, self.__db.Date),
            )

        if filters.documento_identidade:
            desistencias = desistencias.filter(
                CadastroVocacional.documento_identidade.ilike(
                    f"%{filters.documento_identidade}%"
                )
            )

        paginacao = desistencias.paginate(page=page, per_page=per_page, error_out=False)

        lista_recusados_response = []

        for (
            usuario_vocacional,
            cadastro_vocacional,
            ficha_vocacional,
            etapa,
            endereco,
        ) in paginacao.items:

            informacoes_da_desistencia = {
                "etapa_desistencia": etapa.etapa,
                "desistencia_em": etapa.created_at.strftime("%d/%m/%Y %H:%M:%S"),
            }

            pre_cadastro = GetPreCadastroSchema(
                pais=usuario_vocacional.pais,
                id=usuario_vocacional.id,
                nome=usuario_vocacional.nome,
                email=usuario_vocacional.email,
                telefone=usuario_vocacional.telefone,
                created_at=usuario_vocacional.created_at,
                status=self.detalhes_da_etapa_vocacional(
                    VocationalStepsEnum.PRE_CADASTRO, usuario_vocacional.id
                ).status,
                responsavel=self.detalhes_da_etapa_vocacional(
                    VocationalStepsEnum.PRE_CADASTRO, usuario_vocacional.id
                ).nome,
                justificativa=self.detalhes_da_etapa_vocacional(
                    VocationalStepsEnum.PRE_CADASTRO, usuario_vocacional.id
                ).justificativa,
            ).dict()

            if cadastro_vocacional != None:
                cadastro = CadastroVocacionalResponse(
                    fk_usuario_vocacional_id=usuario_vocacional.id,
                    id=cadastro_vocacional.id,
                    nome=usuario_vocacional.nome,
                    email=usuario_vocacional.email,
                    telefone=usuario_vocacional.telefone,
                    genero=usuario_vocacional.genero,
                    created_at=cadastro_vocacional.created_at.strftime("%d/%m/%Y"),
                    data_nascimento=cadastro_vocacional.data_nascimento.strftime(
                        "%d/%m/%Y"
                    ),
                    documento_identidade=cadastro_vocacional.documento_identidade,
                    rua=endereco.rua,
                    cidade=endereco.cidade,
                    estado=endereco.estado,
                    bairro=endereco.bairro,
                    numero=endereco.numero,
                    cep=endereco.cep,
                    detalhe_estrangeiro=endereco.detalhe_estrangeiro,
                    pais=usuario_vocacional.pais,
                    status=self.detalhes_da_etapa_vocacional(
                        VocationalStepsEnum.CADASTRO, usuario_vocacional.id
                    ).status,
                    responsavel=self.detalhes_da_etapa_vocacional(
                        VocationalStepsEnum.CADASTRO, usuario_vocacional.id
                    ).nome,
                    justificativa=self.detalhes_da_etapa_vocacional(
                        VocationalStepsEnum.CADASTRO, usuario_vocacional.id
                    ).justificativa,
                ).dict()
            else:
                cadastro = {}

            if ficha_vocacional != None:
                sacramentos_list = []

                get_sacramentos = (
                    self.__db.session.query(SacramentoVocacional)
                    .filter(
                        SacramentoVocacional.fk_ficha_vocacional_id
                        == ficha_vocacional.id
                    )
                    .all()
                )

                for sacramento in get_sacramentos:
                    sacramentos_list.append(sacramento.nome)

                ficha = FichaVocacionalResponseSchema(
                    motivacao_instituto=ficha_vocacional.motivacao_instituto,
                    fk_usuario_vocacional_id=ficha_vocacional.fk_usuario_vocacional_id,
                    motivacao_admissao_vocacional=ficha_vocacional.motivacao_admissao_vocacional,
                    referencia_conhecimento_instituto=ficha_vocacional.referencia_conhecimento_instituto,
                    identificacao_instituto=ficha_vocacional.identificacao_instituto,
                    seminario_realizado_em=(
                        ficha_vocacional.seminario_realizado_em.strftime("%d/%m/%Y")
                        if ficha_vocacional.seminario_realizado_em
                        else None
                    ),
                    testemunho_conversao=ficha_vocacional.testemunho_conversao,
                    escolaridade=ficha_vocacional.escolaridade,
                    profissao=ficha_vocacional.profissao,
                    cursos=ficha_vocacional.cursos,
                    rotina_diaria=ficha_vocacional.rotina_diaria,
                    aceitacao_familiar=ficha_vocacional.aceitacao_familiar,
                    estado_civil=ficha_vocacional.estado_civil,
                    motivo_divorcio=ficha_vocacional.motivo_divorcio,
                    deixou_religiao_anterior_em=(
                        ficha_vocacional.deixou_religiao_anterior_em.strftime(
                            "%d/%m/%Y"
                        )
                        if ficha_vocacional.deixou_religiao_anterior_em
                        else None
                    ),
                    remedio_controlado_inicio=(
                        ficha_vocacional.remedio_controlado_inicio.strftime("%d/%m/%Y")
                        if ficha_vocacional.remedio_controlado_inicio
                        else None
                    ),
                    remedio_controlado_termino=(
                        ficha_vocacional.remedio_controlado_termino.strftime("%d/%m/%Y")
                        if ficha_vocacional.remedio_controlado_termino
                        else None
                    ),
                    descricao_problema_saude=ficha_vocacional.descricao_problema_saude,
                    foto_vocacional=self.__foto_vocacional(
                        ficha_vocacional.foto_vocacional
                    ),
                    sacramentos=sacramentos_list,
                    status=self.detalhes_da_etapa_vocacional(
                        VocationalStepsEnum.FICHA_VOCACIONAL, usuario_vocacional.id
                    ).status,
                    responsavel=self.detalhes_da_etapa_vocacional(
                        VocationalStepsEnum.FICHA_VOCACIONAL, usuario_vocacional.id
                    ).nome,
                    justificativa=self.detalhes_da_etapa_vocacional(
                        VocationalStepsEnum.FICHA_VOCACIONAL, usuario_vocacional.id
                    ).justificativa,
                ).dict()
            else:
                ficha = {}

            lista_recusados_response.append(
                {
                    "pre_cadastro": pre_cadastro,
                    "cadastro_vocacional": cadastro,
                    "ficha_do_vocacional": ficha,
                    "informacoes_da_desistencia": informacoes_da_desistencia,
                }
            )

        response = {
            "desistencias": lista_recusados_response,
            "page": paginacao.page,
            "total": paginacao.total,
        }

        return response, HTTPStatus.OK

    def get_vocacionais_recusados(
        self, filters: dict, page: int, per_page: int, filtros_permissoes
    ) -> Tuple[dict, HTTPStatus]:

        recusados = (
            self.__db.session.query(
                UsuarioVocacional,
                CadastroVocacional,
                FichaVocacional,
                EtapaVocacional,
                Endereco,
            )
            .join(
                UsuarioVocacional,
                UsuarioVocacional.id == EtapaVocacional.fk_usuario_vocacional_id,
            )
            .outerjoin(
                CadastroVocacional,
                CadastroVocacional.fk_usuario_vocacional_id == UsuarioVocacional.id,
            )
            .outerjoin(
                FichaVocacional,
                FichaVocacional.fk_usuario_vocacional_id == UsuarioVocacional.id,
            )
            .outerjoin(Endereco, Endereco.id == CadastroVocacional.fk_endereco_id)
            .filter(EtapaVocacional.status == "reprovado")
            .order_by(self.__db.desc(EtapaVocacional.created_at))
        )

        if filters.etapa:
            recusados = recusados.filter(EtapaVocacional.etapa == filters.etapa)

        if filters.pais:
            recusados = recusados.filter(
                UsuarioVocacional.pais == "brasil"
                if filters.pais == "brasil"
                else UsuarioVocacional.pais != "brasil"
            )

        if filters.telefone:
            recusados = recusados.filter(
                UsuarioVocacional.telefone.ilike(
                    f"%{re.sub(r'[^0-9]', '', filters.telefone)}%"
                )
            )

        if filtros_permissoes["acessar"] == VocationalGendersEnum.MASCULINO:
            recusados = recusados.filter(
                UsuarioVocacional.genero == VocationalGendersEnum.MASCULINO
            )

        elif filtros_permissoes["acessar"] == VocationalGendersEnum.FEMININO:
            recusados = recusados.filter(
                UsuarioVocacional.genero == VocationalGendersEnum.FEMININO
            )
        else:
            if filters.genero:
                recusados = recusados.filter(
                    UsuarioVocacional.genero == filters.genero
                )

        if filters.status:
            recusados = recusados.filter(EtapaVocacional.status == filters.status)

        if filters.nome:
            recusados = recusados.filter(
                UsuarioVocacional.nome.ilike(f"%{filters.nome}%")
            )

        if filters.email:
            recusados = recusados.filter(
                UsuarioVocacional.email.ilike(f"%{filters.email}%")
            )

        if filters.data_inicial:
            recusados = recusados.filter(
                self.__db.cast(EtapaVocacional.created_at, self.__db.Date)
                >= self.__db.cast(filters.data_inicial, self.__db.Date)
            )

        if filters.data_final:
            recusados = recusados.filter(
                self.__db.cast(EtapaVocacional.created_at, self.__db.Date)
                <= self.__db.cast(filters.data_final, self.__db.Date),
            )

        if filters.documento_identidade:
            recusados = recusados.filter(
                CadastroVocacional.documento_identidade.ilike(
                    f"%{filters.documento_identidade}%"
                )
            )

        paginacao = recusados.paginate(page=page, per_page=per_page, error_out=False)

        lista_recusados_response = []

        for (
            usuario_vocacional,
            cadastro_vocacional,
            ficha_vocacional,
            etapa,
            endereco,
        ) in paginacao.items:

            informacoes_da_reprovacao = {
                "recusado_em": etapa.etapa,
                "recusado_por": f"{self.__get_responsavel_update_status(etapa.responsavel, etapa.etapa)} - {etapa.created_at.strftime('%d/%m/%y %H:%M:%S')}",
                "justificativa": etapa.justificativa,
            }

            pre_cadastro = GetPreCadastroSchema(
                pais=usuario_vocacional.pais,
                id=usuario_vocacional.id,
                nome=usuario_vocacional.nome,
                email=usuario_vocacional.email,
                telefone=usuario_vocacional.telefone,
                created_at=usuario_vocacional.created_at,
                status=self.detalhes_da_etapa_vocacional(
                    VocationalStepsEnum.PRE_CADASTRO, usuario_vocacional.id
                ).status,
                responsavel=self.detalhes_da_etapa_vocacional(
                    VocationalStepsEnum.PRE_CADASTRO, usuario_vocacional.id
                ).nome,
                justificativa=self.detalhes_da_etapa_vocacional(
                    VocationalStepsEnum.PRE_CADASTRO, usuario_vocacional.id
                ).justificativa,
            ).dict()

            if cadastro_vocacional != None:
                cadastro = CadastroVocacionalResponse(
                    fk_usuario_vocacional_id=usuario_vocacional.id,
                    id=cadastro_vocacional.id,
                    nome=usuario_vocacional.nome,
                    email=usuario_vocacional.email,
                    telefone=usuario_vocacional.telefone,
                    genero=usuario_vocacional.genero,
                    created_at=cadastro_vocacional.created_at.strftime("%d/%m/%Y"),
                    data_nascimento=cadastro_vocacional.data_nascimento.strftime(
                        "%d/%m/%Y"
                    ),
                    documento_identidade=cadastro_vocacional.documento_identidade,
                    rua=endereco.rua,
                    cidade=endereco.cidade,
                    estado=endereco.estado,
                    bairro=endereco.bairro,
                    numero=endereco.numero,
                    cep=endereco.cep,
                    detalhe_estrangeiro=endereco.detalhe_estrangeiro,
                    pais=usuario_vocacional.pais,
                    status=self.detalhes_da_etapa_vocacional(
                        VocationalStepsEnum.CADASTRO, usuario_vocacional.id
                    ).status,
                    responsavel=self.detalhes_da_etapa_vocacional(
                        VocationalStepsEnum.CADASTRO, usuario_vocacional.id
                    ).nome,
                    justificativa=self.detalhes_da_etapa_vocacional(
                        VocationalStepsEnum.CADASTRO, usuario_vocacional.id
                    ).justificativa,
                ).dict()
            else:
                cadastro = {}

            if ficha_vocacional != None:
                sacramentos_list = []

                get_sacramentos = (
                    self.__db.session.query(SacramentoVocacional)
                    .filter(
                        SacramentoVocacional.fk_ficha_vocacional_id
                        == ficha_vocacional.id
                    )
                    .all()
                )

                for sacramento in get_sacramentos:
                    sacramentos_list.append(sacramento.nome)

                ficha = FichaVocacionalResponseSchema(
                    motivacao_instituto=ficha_vocacional.motivacao_instituto,
                    fk_usuario_vocacional_id=ficha_vocacional.fk_usuario_vocacional_id,
                    motivacao_admissao_vocacional=ficha_vocacional.motivacao_admissao_vocacional,
                    referencia_conhecimento_instituto=ficha_vocacional.referencia_conhecimento_instituto,
                    identificacao_instituto=ficha_vocacional.identificacao_instituto,
                    seminario_realizado_em=(
                        ficha_vocacional.seminario_realizado_em.strftime("%d/%m/%Y")
                        if ficha_vocacional.seminario_realizado_em
                        else None
                    ),
                    testemunho_conversao=ficha_vocacional.testemunho_conversao,
                    escolaridade=ficha_vocacional.escolaridade,
                    profissao=ficha_vocacional.profissao,
                    cursos=ficha_vocacional.cursos,
                    rotina_diaria=ficha_vocacional.rotina_diaria,
                    aceitacao_familiar=ficha_vocacional.aceitacao_familiar,
                    estado_civil=ficha_vocacional.estado_civil,
                    motivo_divorcio=ficha_vocacional.motivo_divorcio,
                    deixou_religiao_anterior_em=(
                        ficha_vocacional.deixou_religiao_anterior_em.strftime(
                            "%d/%m/%Y"
                        )
                        if ficha_vocacional.deixou_religiao_anterior_em
                        else None
                    ),
                    remedio_controlado_inicio=(
                        ficha_vocacional.remedio_controlado_inicio.strftime("%d/%m/%Y")
                        if ficha_vocacional.remedio_controlado_inicio
                        else None
                    ),
                    remedio_controlado_termino=(
                        ficha_vocacional.remedio_controlado_termino.strftime("%d/%m/%Y")
                        if ficha_vocacional.remedio_controlado_termino
                        else None
                    ),
                    descricao_problema_saude=ficha_vocacional.descricao_problema_saude,
                    foto_vocacional=self.__foto_vocacional(
                        ficha_vocacional.foto_vocacional
                    ),
                    sacramentos=sacramentos_list,
                    status=self.detalhes_da_etapa_vocacional(
                        VocationalStepsEnum.FICHA_VOCACIONAL, usuario_vocacional.id
                    ).status,
                    responsavel=self.detalhes_da_etapa_vocacional(
                        VocationalStepsEnum.FICHA_VOCACIONAL, usuario_vocacional.id
                    ).nome,
                    justificativa=self.detalhes_da_etapa_vocacional(
                        VocationalStepsEnum.FICHA_VOCACIONAL, usuario_vocacional.id
                    ).justificativa,
                ).dict()
            else:
                ficha = {}

            lista_recusados_response.append(
                {
                    "pre_cadastro": pre_cadastro,
                    "cadastro_vocacional": cadastro,
                    "ficha_do_vocacional": ficha,
                    "informacoes_da_reprovacao": informacoes_da_reprovacao,
                }
            )

        response = {
            "recusados": lista_recusados_response,
            "page": paginacao.page,
            "total": paginacao.total,
        }

        return response, HTTPStatus.OK

    def register_desistencia(
        self, fk_usuario_vocacional_id: int
    ) -> tuple[dict, HTTPStatus]:
        try:
            etapa = self.__get_current_etapa(fk_usuario_vocacional_id)

            if etapa.status == "desistencia":
                raise ConflictError("Desistência já realizada anteriormente.")

            register_desistencia = EtapaVocacional(
                fk_usuario_vocacional_id=fk_usuario_vocacional_id,
                etapa=etapa.etapa,
                status="desistencia",
            )

            self.__db.session.add(register_desistencia)
            self.__db.session.commit()

            return {"msg": "Sua desistência foi registrada com sucesso."}, HTTPStatus.OK

        except Exception as e:
            return errors_handler(e)

    def __get_current_etapa(self, fk_usuario_vocacional_id) -> EtapaVocacional:

        get_usuario_vocaciobal = (
            self.__db.session.query(UsuarioVocacional)
            .filter(UsuarioVocacional.id == fk_usuario_vocacional_id)
            .first()
        )

        if get_usuario_vocaciobal is None:
            raise NotFoundError("Vocacional não encontrado")

        current_etapa = (
            self.__db.session.query(EtapaVocacional)
            .filter(
                EtapaVocacional.fk_usuario_vocacional_id == fk_usuario_vocacional_id
            )
            .order_by(self.__db.desc(EtapaVocacional.created_at))
            .first()
        )

        if current_etapa is None:
            raise NotFoundError("Nenhuma etapa encontrada")

        return current_etapa

    def aprove_or_recuse_vocacional(
        self, fk_usuario_vocacional_id: int, acao: str, http_request: dict
    ):
        try:

            if acao not in ["aprovar", "reprovar"]:
                raise BadRequestError("Ação não disponível")

            if acao == "aprovar":
                return self.__aprove_to_next_step(fk_usuario_vocacional_id)

            if acao == "reprovar":
                return self.__reprove_to_next_step(
                    fk_usuario_vocacional_id, http_request
                )

        except Exception as e:
            return errors_handler(e)

    def detalhes_da_etapa_vocacional(
        self, etapa_vocacional: VocationalStepsEnum, fk_usuario_vocacional_id: int
    ):
        return (
            self.__db.session.query(
                EtapaVocacional.etapa,
                EtapaVocacional.status,
                EtapaVocacional.justificativa,
                Usuario.nome,
            )
            .outerjoin(Usuario, Usuario.id == EtapaVocacional.responsavel)
            .filter(
                EtapaVocacional.etapa == etapa_vocacional,
                EtapaVocacional.fk_usuario_vocacional_id == fk_usuario_vocacional_id,
            )
            .order_by(self.__db.desc(EtapaVocacional.created_at))
            .first()
        )

    def __reprove_to_next_step(self, fk_usuario_vocacional_id: int, http_request: dict):
        try:
            get_current_step = self.__get_current_etapa(fk_usuario_vocacional_id)

            if get_current_step.status == "reprovado":
                raise ConflictError("Vocacional já reprovado anteriormente.")

            get_current_step.status = "reprovado"
            get_current_step.responsavel = current_user["id"]
            get_current_step.updated_at = get_current_time()
            get_current_step.justificativa = http_request.get("justificativa")

            self.__db.session.commit()

            return {
                "msg": f"Vocacional {get_current_step.status} com sucesso."
            }, HTTPStatus.OK

        except Exception as e:
            return errors_handler(e)

    def __aprove_to_next_step(self, fk_usuario_vocacional_id: int):

        try:

            get_current_step = self.__get_current_etapa(fk_usuario_vocacional_id)

            if get_current_step.status == "pendente":
                get_current_step.status = "aprovado"
                get_current_step.responsavel = current_user["id"]
                get_current_step.updated_at = get_current_time()
            else:
                raise ConflictError("Usuário já aprovado, reprovado ou desistiu.")

            self.__db.session.commit()

            vocacional = (
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
                    EtapaVocacional.fk_usuario_vocacional_id == UsuarioVocacional.id,
                )
                .filter(
                    EtapaVocacional.fk_usuario_vocacional_id
                    == fk_usuario_vocacional_id,
                )
                .order_by(self.__db.desc(EtapaVocacional.created_at))
                .first()
            )

            envia_email_vocacional(vocacional)

            return {
                "msg": f"Vocacional {get_current_step.status} com sucesso."
            }, HTTPStatus.OK

        except Exception as e:
            return errors_handler(e)

    def delete_vocacional(self, fk_usuario_vocacional_id):
        try:

            get_vocacional = (
                self.__db.session.query(UsuarioVocacional)
                .filter(UsuarioVocacional.id == fk_usuario_vocacional_id)
                .first()
            )

            if get_vocacional is None:
                raise NotFoundError("Vocacional não encontrado.")

            self.__db.session.delete(get_vocacional)
            self.__db.session.commit()

            return {"msg": "Usuário vocacional deletado com sucesso."}

        except Exception as e:
            self.__db.session.rollback()
            return errors_handler(e)

    def get_info_token(self, data_decode_token):
        try:
            result = (
                self.__db.session.query(
                    UsuarioVocacional.nome,
                    UsuarioVocacional.email,
                    EtapaVocacional.etapa,
                    EtapaVocacional.status,
                    UsuarioVocacional.telefone,
                    UsuarioVocacional.pais,
                    UsuarioVocacional.id.label("fk_usuario_vocacional_id"),
                )
                .join(
                    EtapaVocacional,
                    EtapaVocacional.fk_usuario_vocacional_id
                    == data_decode_token["fk_usuario_vocacional_id"],
                )
                .filter(
                    UsuarioVocacional.id
                    == data_decode_token["fk_usuario_vocacional_id"]
                )
                .order_by(self.__db.desc(EtapaVocacional.created_at))
                .first()
            )

            if result is None:
                raise NotFoundError("Vocacional não encontrado.")

            return result

        except Exception as e:
            raise e

    def get_usuario_vocacional(self, usuario_vocacional_id):

        get_vocacional = (
            self.__db.session.query(
                UsuarioVocacional.nome,
                UsuarioVocacional.email,
                UsuarioVocacional.telefone,
                UsuarioVocacional.pais,
                UsuarioVocacional.id,
                UsuarioVocacional.genero,
                EtapaVocacional.status,
                EtapaVocacional.etapa,
            )
            .join(
                EtapaVocacional,
                EtapaVocacional.fk_usuario_vocacional_id == UsuarioVocacional.id,
            )
            .filter(
                EtapaVocacional.fk_usuario_vocacional_id == usuario_vocacional_id,
            )
            .order_by(self.__db.desc(EtapaVocacional.created_at))
            .first()
        )

        if get_vocacional == None:
            raise NotFoundError("Vocacional não encontrado.")

        return get_vocacional
