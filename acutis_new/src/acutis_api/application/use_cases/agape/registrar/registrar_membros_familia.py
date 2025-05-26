from uuid import UUID
from datetime import date # Para type hint de data_nascimento
from acutis_api.domain.repositories.agape import AgapeRepositoryInterface
from acutis_api.communication.requests.agape import (
    MembrosAgapeCadastroRequestSchema
)
from acutis_api.communication.responses.padrao import ResponsePadraoSchema
from acutis_api.exception.errors.not_found import HttpNotFoundError
from acutis_api.exception.errors.conflict import HttpConflictError
from acutis_api.exception.errors.bad_request import HttpBadRequestError
from acutis_api.domain.services.file_service import FileServiceInterface
from acutis_api.application.utils.funcoes_auxiliares import (
    decodificar_base64_para_arquivo, 
    valida_cpf_cnpj, 
    valida_email, 
    valida_nome
)
from acutis_api.application.utils.regex import format_string 
from acutis_api.domain.entities.membro_agape import (
    MembroAgape as MembroAgapeEntity # Entidade do domínio
)

class RegistrarMembrosFamiliaAgapeUseCase:
    def __init__(
        self, 
        agape_repository: AgapeRepositoryInterface, 
        file_service: FileServiceInterface
    ):
        self._agape_repository = agape_repository
        self._file_service = file_service

    def execute(
        self, 
        familia_agape_id: UUID, 
        request_data: MembrosAgapeCadastroRequestSchema
    ) -> ResponsePadraoSchema:
        familia = self._agape_repository.buscar_familia_por_id(
            familia_agape_id
            )
        if not familia:
            raise HttpNotFoundError("Família não encontrada ou inativa.")

        for membro in request_data.membros:
            # Validar nome
            nome_valido, msg_nome = valida_nome(membro.nome)
            if not nome_valido:
                raise HttpBadRequestError(
                    f"Nome inválido para '{membro.nome}': {msg_nome}"
                )
            nome_formatado = msg_nome

            # Validar CPF (se fornecido) e checar unicidade
            cpf_formatado = None
            if membro.cpf:
                cpf_formatado = valida_cpf_cnpj(
                    membro.cpf, 
                    tipo_documento='cpf', 
                    gerar_excesao=True
                ) # Levanta HttpBadRequestError
                if self._agape_repository.buscar_membro_por_cpf(cpf_formatado):
                    raise HttpConflictError(
                        f"CPF {cpf_formatado} já cadastrado para outro membro."
                    )
            
            if membro.responsavel and not cpf_formatado:
                 raise HttpBadRequestError(
                    f"""CPF é obrigatório para o 
                    membro responsável: {nome_formatado}.
                    """
                )

            # Validar Email (se fornecido) e checar unicidade
            email_formatado = None
            if membro.email:
                email_valido, msg_email = valida_email(
                    membro.email, 
                    verificar_entregabilidade=False, 
                    verificar_dominio=False
                )
                if not email_valido:
                    raise HttpBadRequestError(
                        f"Email inválido para '{nome_formatado}': {msg_email}"
                    )
                email_formatado = msg_email
                if self._agape_repository.buscar_membro_por_email(
                    email_formatado
                ):
                    raise HttpConflictError(
                        f"""
                        Email {email_formatado} já 
                        cadastrado para outro membro.
                        """
                    )
            
            telefone_formatado = None
            if membro.telefone:
                telefone_formatado = format_string(
                    membro.telefone, 
                    only_digits=True
                )

            foto_documento_salva = None
            if membro.foto_documento:
                try:
                    arquivo_foto, nome_arquivo_foto = (
                        decodificar_base64_para_arquivo(
                            membro.foto_documento
                        )
                    )
                    foto_documento_salva = self._file_service.salvar_arquivo(
                        arquivo_foto, 
                        nome_arquivo_foto, 'membros_agape/documentos'
                    )
                except Exception as e:
                    raise HttpBadRequestError(
                        f"""
                        Erro ao processar foto_documento 
                        para '{nome_formatado}': {str(e)}
                        """
                    )
            
            novo_membro = MembroAgapeEntity(
                fk_familia_agape_id=familia.id,
                responsavel=membro.responsavel,
                nome=nome_formatado,
                email=email_formatado,
                telefone=telefone_formatado,
                cpf=cpf_formatado,
                data_nascimento=membro.data_nascimento,
                funcao_familiar=membro.funcao_familiar,
                escolaridade=membro.escolaridade,
                ocupacao=membro.ocupacao,
                renda=membro.renda,
                beneficiario_assistencial=membro.beneficiario_assistencial,
                foto_documento=foto_documento_salva
            )
            self._agape_repository.registrar_membro_agape(novo_membro)

        self._agape_repository.salvar_alteracoes() # Commit no final

        return ResponsePadraoSchema(
            msg=f"""{len(request_data.membros)} membro(s) 
            cadastrado(s) com sucesso na família {familia.nome_familia}.
            """,
        )
