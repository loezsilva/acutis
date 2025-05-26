from uuid import UUID
from datetime import date # Para type hint de data_nascimento
from acutis_api.domain.repositories.agape import AgapeRepositoryInterface
from acutis_api.communication.requests.agape import MembrosAgapeCadastroRequestSchema, MembroAgapeCadastroItemSchema # Schemas de requisição
from acutis_api.communication.responses.padrao import ResponsePadraoSchema # Schema de resposta padrão
from acutis_api.exception.errors.not_found import HttpNotFoundError
from acutis_api.exception.errors.conflict import HttpConflictError
from acutis_api.exception.errors.bad_request import HttpBadRequestError
from acutis_api.domain.services.file_service import FileServiceInterface
from acutis_api.application.utils.funcoes_auxiliares import decodificar_base64_para_arquivo, valida_cpf_cnpj, valida_email, valida_nome
from acutis_api.application.utils.regex import format_string # Para formatar telefone
from acutis_api.domain.entities.membro_agape import MembroAgape as MembroAgapeEntity # Entidade do domínio

class CadastrarMembrosFamiliaAgapeUseCase:
    def __init__(self, agape_repository: AgapeRepositoryInterface, file_service: FileServiceInterface):
        self._agape_repository = agape_repository
        self._file_service = file_service

    def execute(self, familia_agape_id: UUID, request_data: MembrosAgapeCadastroRequestSchema) -> ResponsePadraoSchema:
        familia = self._agape_repository.buscar_familia_agape_por_id(familia_agape_id)
        if not familia: # Repositório já levanta HttpNotFoundError se não encontrar e não estiver deletada
            # Esta checagem é uma dupla garantia ou pode ser removida se o repo sempre levanta.
            raise HttpNotFoundError("Família não encontrada ou inativa.")

        novos_membros_criados = [] # Para uma possível resposta com os membros criados

        for membro_data in request_data.membros:
            # Validar nome
            nome_valido, msg_nome = valida_nome(membro_data.nome)
            if not nome_valido:
                raise HttpBadRequestError(f"Nome inválido para '{membro_data.nome}': {msg_nome}")
            nome_formatado = msg_nome # valida_nome retorna o nome formatado se válido

            # Validar CPF (se fornecido) e checar unicidade
            cpf_formatado = None
            if membro_data.cpf:
                cpf_formatado = valida_cpf_cnpj(membro_data.cpf, tipo_documento='cpf', gerar_excesao=True) # Levanta HttpBadRequestError
                if self._agape_repository.buscar_membro_por_cpf(cpf_formatado):
                    raise HttpConflictError(f"CPF {cpf_formatado} já cadastrado para outro membro.")
            
            if membro_data.responsavel and not cpf_formatado:
                 raise HttpBadRequestError(f"CPF é obrigatório para o membro responsável: {nome_formatado}.")

            # Validar Email (se fornecido) e checar unicidade
            email_formatado = None
            if membro_data.email:
                email_valido, msg_email = valida_email(membro_data.email, verificar_entregabilidade=False, verificar_dominio=False)
                if not email_valido:
                    raise HttpBadRequestError(f"Email inválido para '{nome_formatado}': {msg_email}")
                email_formatado = msg_email # valida_email retorna o email normalizado
                if self._agape_repository.buscar_membro_por_email(email_formatado):
                    raise HttpConflictError(f"Email {email_formatado} já cadastrado para outro membro.")
            
            telefone_formatado = None
            if membro_data.telefone:
                telefone_formatado = format_string(membro_data.telefone, only_digits=True)

            # Processar foto_documento (base64)
            foto_documento_salva = None
            if membro_data.foto_documento:
                try:
                    arquivo_foto, nome_arquivo_foto = decodificar_base64_para_arquivo(membro_data.foto_documento)
                    # O FileService em acutis_new pode ter um método diferente de 'upload_image'
                    # Assumindo 'salvar_arquivo' como método genérico do FileServiceInterface
                    foto_documento_salva = self._file_service.salvar_arquivo(arquivo_foto, nome_arquivo_foto, 'membros_agape/documentos')
                except Exception as e:
                    raise HttpBadRequestError(f"Erro ao processar foto_documento para '{nome_formatado}': {str(e)}")
            
            novo_membro = MembroAgapeEntity(
                fk_familia_agape_id=familia.id,
                responsavel=membro_data.responsavel,
                nome=nome_formatado,
                email=email_formatado,
                telefone=telefone_formatado,
                cpf=cpf_formatado,
                data_nascimento=membro_data.data_nascimento,
                funcao_familiar=membro_data.funcao_familiar,
                escolaridade=membro_data.escolaridade,
                ocupacao=membro_data.ocupacao,
                renda=membro_data.renda,
                beneficiario_assistencial=membro_data.beneficiario_assistencial,
                foto_documento=foto_documento_salva
                # id, criado_em, atualizado_em são gerados automaticamente
            )
            self._agape_repository.registrar_membro_agape(novo_membro)
            # Se quisesse retornar detalhes dos membros:
            # novos_membros_criados.append(MembroAgapeDetalhesResponse.model_validate(novo_membro))


        self._agape_repository.salvar_alteracoes() # Commit no final

        return ResponsePadraoSchema(sucesso=True, detalhe=f"{len(request_data.membros)} membro(s) cadastrado(s) com sucesso na família {familia.nome_familia}.")
