import uuid

from acutis_api.application.utils.funcoes_auxiliares import (
    valida_cpf_cnpj,
    valida_email,
    valida_nome,
)
from acutis_api.communication.requests.agape import (
    EditarMembroAgapeFormData,
)
from acutis_api.domain.entities.membro_agape import MembroAgape
from acutis_api.domain.repositories.agape import AgapeRepositoryInterface
from acutis_api.domain.services.file_service import FileServiceInterface
from acutis_api.exception.errors.bad_request import HttpBadRequestError
from acutis_api.exception.errors.conflict import HttpConflictError
from acutis_api.exception.errors.not_found import HttpNotFoundError


class EditarMembroAgapeUseCase:
    """
    Caso de uso para editar um membro ágape existente.
    """

    def __init__(
        self,
        agape_repository: AgapeRepositoryInterface,
        file_service: FileServiceInterface,
    ):
        self.agape_repository = agape_repository
        self.file_service = file_service

    def execute(
        self,
        membro_agape_id: uuid.UUID,
        dados_edicao: EditarMembroAgapeFormData,
    ) -> None:
        self.__validate_data(
            dados_edicao,
        )

        membro_existente = self.agape_repository.buscar_membro_agape_por_id(
            membro_agape_id=membro_agape_id
        )

        if not membro_existente:
            raise HttpNotFoundError(
                f'Membro Ágape com ID {membro_agape_id} não encontrado.'
            )

        membro_existente.responsavel = dados_edicao.responsavel
        membro_existente.nome = dados_edicao.nome
        membro_existente.email = dados_edicao.email
        membro_existente.telefone = dados_edicao.telefone
        membro_existente.cpf = dados_edicao.cpf
        membro_existente.data_nascimento = dados_edicao.data_nascimento
        membro_existente.funcao_familiar = dados_edicao.funcao_familiar
        membro_existente.escolaridade = dados_edicao.escolaridade
        membro_existente.ocupacao = dados_edicao.ocupacao
        membro_existente.renda = dados_edicao.renda
        membro_existente.beneficiario_assistencial = (
            dados_edicao.beneficiario_assistencial
        )

        if dados_edicao.foto_documento:
            membro_existente.foto_documento = self.file_service.salvar_arquivo(
                dados_edicao.foto_documento
            )

        self.agape_repository.atualizar_membro_agape(
            membro_agape=membro_existente
        )

        self.agape_repository.salvar_alteracoes()

    def __validate_data(self, dados_para_atualizar: MembroAgape) -> None:
        if dados_para_atualizar.cpf:
            valida_cpf_cnpj(
                dados_para_atualizar.cpf,
                tipo_documento='cpf',
                gerar_excesao=True,
            )

            if self.agape_repository.buscar_membro_por_cpf(
                cpf=dados_para_atualizar.cpf
            ):
                raise HttpConflictError(
                    f'Ja existe um membro cadastrado com o CPF {dados_para_atualizar.cpf}.'  # noqa
                )
        if dados_para_atualizar.email:
            email_valido, msg = valida_email(
                email=dados_para_atualizar.email,
                verificar_entregabilidade=True,
                verificar_dominio=True,
            )
            if not email_valido:
                raise HttpBadRequestError(msg)

            if self.agape_repository.buscar_membro_por_email(
                email=dados_para_atualizar.email
            ):
                raise HttpConflictError(
                    f'Ja existe um membro cadastrado com o e-mail {dados_para_atualizar.email}'  # noqa
                )

        nome_valido, msg = valida_nome(nome=dados_para_atualizar.nome)

        if not nome_valido:
            raise HttpBadRequestError(msg)
