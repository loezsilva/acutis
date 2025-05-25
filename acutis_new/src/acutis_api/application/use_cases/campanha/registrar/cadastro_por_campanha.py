import uuid
from uuid import UUID

from flask_jwt_extended import get_jwt_identity

from acutis_api.application.use_cases.base_classes import (
    CamposAdicionaisValidators,
)
from acutis_api.application.utils.funcoes_auxiliares import (
    decodificar_base64_para_arquivo,
)
from acutis_api.communication.enums.campanhas import ObjetivosCampanhaEnum
from acutis_api.communication.requests.campanha import (
    CadastroPorCampanhaFormData,
)
from acutis_api.communication.requests.membros import CampoAdicionalSchema
from acutis_api.communication.responses.padrao import ResponsePadraoSchema
from acutis_api.domain.entities.campo_adicional import CampoAdicional
from acutis_api.domain.repositories.membros import MembrosRepositoryInterface
from acutis_api.domain.repositories.schemas.membros import (
    RegistrarNovoLeadSchema,
    RegistrarNovoMembroSchema,
)
from acutis_api.domain.repositories.schemas.membros_oficiais import (
    RegistraMembroOficialSchema,
)
from acutis_api.domain.services.file_service import FileServiceInterface
from acutis_api.exception.errors.bad_request import HttpBadRequestError

MSG_OFICIAL_CADASTRADO = 'Oficial cadastrado com sucesso.'


class CadastroPorCampanhaUseCase:
    def __init__(
        self,
        membro_repository: MembrosRepositoryInterface,
        s3_service: FileServiceInterface,
    ):
        self.__repository = membro_repository
        self.__validator = CamposAdicionaisValidators()
        self.__s3_service = s3_service

    def execute(  # noqa PLR0915
        self, request: CadastroPorCampanhaFormData, campanha_id: UUID
    ):
        foto_membro = (
            self.__s3_service.salvar_arquivo(request.foto)
            if request.foto
            else None
        )
        superior = request.superior
        campos_recebidos = request.campos_adicionais

        usuario_por_token = get_jwt_identity()

        campanha = self.__repository.buscar_campanha_por_id(campanha_id)
        self.__validator.verificar_campanha_valida(campanha)

        if campanha.superior_obrigatorio == 1 and not superior:
            raise HttpBadRequestError('É necessário informar o superior.')

        if campanha.campos_adicionais and not campos_recebidos:
            raise HttpBadRequestError(
                'É necessário informar os campos adicionais.'
            )

        if usuario_por_token:
            membro_logado = self.__repository.buscar_membro_por_lead_id(
                usuario_por_token
            )
            if campanha.objetivo == ObjetivosCampanhaEnum.oficiais:
                if campanha.campos_adicionais:
                    self._registrar_campos_adicionais(
                        usuario_por_token,
                        campos_recebidos,
                        campanha.campos_adicionais,
                    )

                if membro_logado:
                    if self.__repository.buscar_oficial_por_fk_membro_id(
                        membro_logado.id
                    ):
                        self.__repository.vincular_lead_a_campanha_registro(
                            usuario_por_token, campanha_id
                        )
                        self.__repository.salvar_alteracoes()
                        return ResponsePadraoSchema(
                            msg='Oficial vinculado a campanha com sucesso.'
                        )

                    self.__repository.vincular_lead_a_campanha_registro(
                        usuario_por_token, campanha_id
                    )

                    membro_oficial = RegistraMembroOficialSchema(
                        fk_membro_id=membro_logado.id,
                        fk_superior_id=superior,
                        fk_cargo_oficial_id=campanha.fk_cargo_oficial_id,
                    )
                    self.__repository.registrar_novo_membro_oficial(
                        membro_oficial
                    )
                    self.__repository.salvar_alteracoes()
                    return ResponsePadraoSchema(msg=MSG_OFICIAL_CADASTRADO)
                self.__repository.vincular_lead_a_campanha_registro(
                    usuario_por_token, campanha_id
                )
                membro_registrado = self._registrar_endereco_e_membro(
                    request,
                    usuario_por_token,
                    foto_membro,
                )
                self.__repository.salvar_alteracoes()
                membro_oficial = RegistraMembroOficialSchema(
                    fk_membro_id=membro_registrado.id,
                    fk_superior_id=superior,
                    fk_cargo_oficial_id=campanha.fk_cargo_oficial_id,
                )
                self.__repository.registrar_novo_membro_oficial(membro_oficial)
                self.__repository.salvar_alteracoes()
                return ResponsePadraoSchema(msg=MSG_OFICIAL_CADASTRADO)

            elif campanha.objetivo == ObjetivosCampanhaEnum.cadastro:
                if campanha.campos_adicionais:
                    self._registrar_campos_adicionais(
                        usuario_por_token,
                        campos_recebidos,
                        campanha.campos_adicionais,
                    )
                if membro_logado:
                    self.__repository.vincular_lead_a_campanha_registro(
                        usuario_por_token, campanha_id
                    )
                    self.__repository.salvar_alteracoes()
                    return ResponsePadraoSchema(
                        msg='Membro vinculado a campanha com sucesso.'
                    )

                self._registrar_endereco_e_membro(
                    request,
                    usuario_por_token,
                    foto_membro,
                )
                self.__repository.vincular_lead_a_campanha_registro(
                    usuario_por_token, campanha_id
                )
                self.__repository.salvar_alteracoes()
                return ResponsePadraoSchema(
                    msg='Membro cadastrado com sucesso.'
                )

            elif campanha.objetivo == ObjetivosCampanhaEnum.pre_cadastro:
                if campanha.campos_adicionais:
                    self._registrar_campos_adicionais(
                        usuario_por_token,
                        campos_recebidos,
                        campanha.campos_adicionais,
                    )
                self.__repository.vincular_lead_a_campanha_registro(
                    usuario_por_token, campanha_id
                )
                self.__repository.salvar_alteracoes()
                return ResponsePadraoSchema(
                    msg='Lead vinculado a campanha com sucesso.'
                )

        if self.__repository.buscar_lead_por_email(request.email):
            raise HttpBadRequestError('O e-mail informado já está cadastro.')

        if self.__repository.buscar_lead_por_telefone(request.telefone):
            raise HttpBadRequestError('O telefone informado já tem cadastro.')

        if campanha.objetivo == ObjetivosCampanhaEnum.oficiais:
            dados_lead = _dados_lead(request)
            lead = self.__repository.registrar_novo_lead(dados_lead)
            membro_registrado = self._registrar_endereco_e_membro(
                request,
                lead.id,
                foto_membro,
            )
            self.__repository.salvar_alteracoes()
            self.__repository.vincular_lead_a_campanha_registro(
                lead.id, campanha_id
            )

            membro_oficial = RegistraMembroOficialSchema(
                fk_membro_id=membro_registrado.id,
                fk_superior_id=superior,
                fk_cargo_oficial_id=campanha.fk_cargo_oficial_id,
            )
            self.__repository.registrar_novo_membro_oficial(membro_oficial)
            self.__repository.salvar_alteracoes()
            return ResponsePadraoSchema(msg=MSG_OFICIAL_CADASTRADO)

        elif campanha.objetivo == ObjetivosCampanhaEnum.cadastro:
            dados_lead = _dados_lead(request)
            lead = self.__repository.registrar_novo_lead(dados_lead)

            self._registrar_endereco_e_membro(
                request,
                lead.id,
                foto_membro,
            )
            self.__repository.vincular_lead_a_campanha_registro(
                lead.id, campanha_id
            )
            self.__repository.salvar_alteracoes()
            return ResponsePadraoSchema(msg='Membro cadastrado com sucesso.')

        elif campanha.objetivo == ObjetivosCampanhaEnum.pre_cadastro:
            dados_lead = _dados_lead(request)
            lead = self.__repository.registrar_novo_lead(dados_lead)
            self.__repository.vincular_lead_a_campanha_registro(
                lead.id, campanha_id
            )
            self.__repository.salvar_alteracoes()
            return ResponsePadraoSchema(msg='Lead cadastrado com sucesso.')

    def _registrar_campos_adicionais(
        self,
        lead_id: uuid.UUID,
        campos_recebidos: list[CampoAdicionalSchema],
        campos_campanha: list[CampoAdicional],
    ):
        self.__validator.validar_campos_adicionais(
            campos_recebidos, campos_campanha
        )

        for campo in campos_recebidos:
            if isinstance(campo.valor_campo, str) and (
                'data:' in campo.valor_campo
            ):
                arquivo, nome_arquivo = decodificar_base64_para_arquivo(
                    campo.valor_campo
                )
                campo.valor_campo = self.__s3_service.salvar_arquivo(
                    arquivo, nome_arquivo
                )
            self.__repository.registrar_campo_adicional_metadado_lead(
                lead_id, campo
            )

    def _registrar_endereco_e_membro(
        self,
        request: CadastroPorCampanhaFormData,
        lead_id: UUID,
        foto_membro: str | None = None,
    ):
        endereco_registrado = self.__repository.registrar_novo_endereco(
            request.endereco
        )
        dados_membro = RegistrarNovoMembroSchema(
            nome_social=request.nome_social,
            data_nascimento=request.data_nascimento,
            numero_documento=request.numero_documento,
            sexo=request.sexo,
            foto=foto_membro,
            endereco_id=endereco_registrado.id,
            lead_id=lead_id,
        )

        membro_registrado = self.__repository.registrar_novo_membro(
            dados_membro
        )

        return membro_registrado


def _dados_lead(request: CadastroPorCampanhaFormData):
    return RegistrarNovoLeadSchema(
        nome=request.nome,
        email=request.email,
        telefone=request.telefone,
        pais=request.pais,
        origem_cadastro=request.origem_cadastro,
        senha=request.senha,
        status=False,
    )
