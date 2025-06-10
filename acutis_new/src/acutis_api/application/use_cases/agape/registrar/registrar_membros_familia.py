from uuid import UUID

from acutis_api.application.utils.funcoes_auxiliares import (
    decodificar_base64_para_arquivo,
    valida_cpf_cnpj,
    valida_email,
    valida_nome,
)
from acutis_api.application.utils.regex import format_string
from acutis_api.communication.requests.agape import (
    MembrosAgapeCadastroRequest,
)
from acutis_api.communication.responses.padrao import ResponsePadraoSchema
from acutis_api.domain.entities.membro_agape import MembroAgape
from acutis_api.domain.repositories.agape import AgapeRepositoryInterface
from acutis_api.domain.services.file_service import FileServiceInterface
from acutis_api.exception.errors.bad_request import HttpBadRequestError
from acutis_api.exception.errors.conflict import HttpConflictError
from acutis_api.exception.errors.not_found import HttpNotFoundError


class RegistrarMembrosFamiliaAgapeUseCase:
    def __init__(
        self,
        agape_repository: AgapeRepositoryInterface,
        file_service: FileServiceInterface,
    ):
        self._agape_repository = agape_repository
        self._file_service = file_service

    def execute(
        self,
        familia_agape_id: UUID,
        dados_requisicao: MembrosAgapeCadastroRequest,
    ) -> ResponsePadraoSchema:
        familia = self._agape_repository.buscar_familia_por_id(
            familia_agape_id
        )

        if not familia:
            raise HttpNotFoundError('Família não encontrada ou inativa.')

        if not dados_requisicao.membros:
            raise HttpBadRequestError('Nenhum membro fornecido para cadastro.')

        for membro in dados_requisicao.membros:
            self.__validate_data(dados_do_membro=membro)

            telefone_formatado = None
            if membro.telefone:
                telefone_formatado = format_string(
                    membro.telefone, only_digits=True
                )

            foto_documento_salva = None
            if membro.foto_documento:
                try:
                    arquivo_foto, nome_arquivo_foto = (
                        decodificar_base64_para_arquivo(membro.foto_documento)
                    )
                    foto_documento_salva = self._file_service.salvar_arquivo(
                        arquivo_foto,
                        nome_arquivo_foto,
                    )
                except Exception as e:
                    raise HttpBadRequestError(
                        f"Erro ao processar foto_documento \
                            para '{membro.nome}': {str(e)}"
                    )

            novo_membro = MembroAgape(
                fk_familia_agape_id=familia.id,
                responsavel=membro.responsavel,
                nome=membro.nome,
                email=membro.email,
                telefone=telefone_formatado,
                cpf=membro.cpf,
                data_nascimento=membro.data_nascimento,
                funcao_familiar=membro.funcao_familiar,
                escolaridade=membro.escolaridade,
                ocupacao=membro.ocupacao,
                renda=membro.renda,
                beneficiario_assistencial=membro.beneficiario_assistencial,
                foto_documento=foto_documento_salva,
            )

            self._agape_repository.registrar_membro_agape(novo_membro)

            self._agape_repository.salvar_alteracoes()

        return ResponsePadraoSchema(
            msg=rf'{len(dados_requisicao.membros)} \
                  membro(s) cadastrado(s) com sucesso na \
                    família {familia.nome_familia}.',
        ).model_dump()

    def __validate_data(self, dados_do_membro: MembroAgape) -> None:
        if dados_do_membro.cpf:
            valida_cpf_cnpj(
                dados_do_membro.cpf, tipo_documento='cpf', gerar_excesao=True
            )

            if self._agape_repository.buscar_membro_por_cpf(
                cpf=dados_do_membro.cpf
            ):
                raise HttpConflictError(
                    f'Ja existe um membro cadastrado com o CPF {dados_do_membro.cpf}.'  # noqa
                )
        if dados_do_membro.email:
            email_valido, msg = valida_email(
                email=dados_do_membro.email,
                verificar_entregabilidade=True,
                verificar_dominio=True,
            )
            if not email_valido:
                raise HttpBadRequestError(msg)

            if self._agape_repository.buscar_membro_por_email(
                email=dados_do_membro.email
            ):
                raise HttpConflictError(
                    f'Ja existe um membro cadastrado com o e-mail {dados_do_membro.email}'  # noqa
                )

        nome_valido, msg = valida_nome(nome=dados_do_membro.nome)

        if not nome_valido:
            raise HttpBadRequestError(msg)
