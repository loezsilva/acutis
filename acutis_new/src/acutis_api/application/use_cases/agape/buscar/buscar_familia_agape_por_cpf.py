from uuid import UUID
from acutis_api.domain.repositories.agape import AgapeRepositoryInterface
from acutis_api.communication.responses.agape import FamiliaAgapeDetalhesPorCpfResponse, EnderecoResponse
from acutis_api.exception.errors.not_found import HttpNotFoundError
# from acutis_api.application.utils.regex import validar_cpf # Omitido pois não existe no local esperado
from acutis_api.domain.services.file_service import FileServiceInterface 

class BuscarFamiliaAgapePorCpfUseCase:
    def __init__(self, agape_repository: AgapeRepositoryInterface, file_service: FileServiceInterface):
        self._agape_repository = agape_repository
        self._file_service = file_service # Para gerar URLs

    def execute(self, cpf: str, ciclo_acao_id: UUID) -> FamiliaAgapeDetalhesPorCpfResponse:
        # 1. Validar CPF (remover formatação se necessário antes de passar para o repo)
        # cpf_validado = validar_cpf(cpf) # Omitido - o utilitário não foi encontrado
        cpf_a_buscar = cpf # Usar o CPF diretamente
            
        # 2. Buscar Membro pelo CPF
        membro = self._agape_repository.buscar_membro_por_cpf(cpf_a_buscar)
        if not membro:
            raise HttpNotFoundError(f"Nenhum membro encontrado com o CPF fornecido.")
        if not membro.fk_familia_agape_id:
            raise HttpNotFoundError(f"Membro com CPF {cpf_a_buscar} não está associado a nenhuma família.")

        # 3. Buscar Família pelo ID do membro
        familia = self._agape_repository.buscar_familia_por_id(membro.fk_familia_agape_id)
        if not familia: 
            raise HttpNotFoundError(f"Família com ID {membro.fk_familia_agape_id} não encontrada ou está inativa.")

        # 4. Buscar Endereço da Família
        endereco_response_data = None
        if familia.fk_endereco_id:
            endereco_entity = self._agape_repository.buscar_endereco_por_id(familia.fk_endereco_id)
            if endereco_entity:
                endereco_response_data = EnderecoResponse.model_validate(endereco_entity)
        
        # 5. Buscar Fotos da Família e gerar URLs
        fotos_entities = self._agape_repository.listar_fotos_por_familia_id(familia.id)
        fotos_urls = [self._file_service.get_public_url(foto.foto) for foto in fotos_entities if foto.foto]

        # 6. Buscar data do último recebimento da família no ciclo especificado
        ultimo_recebimento_data = self._agape_repository.buscar_data_ultimo_recebimento_familia_no_ciclo(
            familia_id=familia.id,
            ciclo_acao_id=ciclo_acao_id
        )

        # 7. Gerar URL para comprovante de residência
        comprovante_url = None
        if familia.comprovante_residencia:
            comprovante_url = self._file_service.get_public_url(familia.comprovante_residencia)

        # 8. Montar a resposta final
        return FamiliaAgapeDetalhesPorCpfResponse(
            id=familia.id,
            nome_familia=familia.nome_familia,
            observacao=familia.observacao,
            comprovante_residencia_url=comprovante_url,
            criado_em=familia.criado_em,
            ativo=familia.deletado_em is None, # Lógica para 'ativo'
            ultimo_recebimento=ultimo_recebimento_data,
            endereco=endereco_response_data,
            fotos_familia_urls=fotos_urls
        )
