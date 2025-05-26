from uuid import UUID
from acutis_api.domain.repositories.agape import AgapeRepositoryInterface
from acutis_api.communication.responses.agape import UltimoCicloAcaoAgapeResponse, EnderecoResponse, DoacaoAgapeResponse
from acutis_api.exception.errors.not_found import HttpNotFoundError
# Importar AcaoAgape para verificar se o nome_acao_id é válido
from acutis_api.domain.entities.acao_agape import AcaoAgape

class BuscarUltimaAcaoAgapeUseCase:
    def __init__(self, agape_repository: AgapeRepositoryInterface):
        self._agape_repository = agape_repository

    def execute(self, nome_acao_id: UUID) -> UltimoCicloAcaoAgapeResponse:
        # 1. Verificar se o nome_acao_id (AcaoAgape) existe
        nome_acao_entity = self._agape_repository.buscar_nome_acao_por_id(nome_acao_id)
        if not nome_acao_entity:
            # O método buscar_nome_acao_por_id já levanta HttpNotFoundError se não encontrar
            # Esta verificação é redundante se o método do repo já levanta, mas não prejudica.
            raise HttpNotFoundError(f"Nome da ação com ID {nome_acao_id} não encontrado.")

        # 2. Buscar a última instância (ciclo) para este nome_acao_id
        ultima_instancia = self._agape_repository.buscar_ultima_instancia_por_nome_acao_id(nome_acao_id)
        if not ultima_instancia:
            raise HttpNotFoundError(f"Nenhum ciclo de ação encontrado para o nome da ação com ID {nome_acao_id}.")

        # 3. Buscar o endereço associado à última instância
        endereco_response_data = None
        if ultima_instancia.fk_endereco_id:
            endereco_entity = self._agape_repository.buscar_endereco_por_id(ultima_instancia.fk_endereco_id)
            if endereco_entity:
                # Usar EnderecoResponse para popular os dados do endereço
                endereco_response_data = EnderecoResponse.model_validate(endereco_entity)
        
        # 4. Buscar os itens/doações associados à última instância
        # O método buscar_doacoes_ciclo_acao_agape espera o ID da instância (ciclo_acao_id)
        itens_do_ciclo_schemas = self._agape_repository.buscar_doacoes_ciclo_acao_agape(ultima_instancia.id)
        
        itens_do_ciclo_responses = [
            DoacaoAgapeResponse.model_validate(item_schema) for item_schema in itens_do_ciclo_schemas
        ]

        # 5. Montar a resposta final
        return UltimoCicloAcaoAgapeResponse(
            id=ultima_instancia.id,
            abrangencia=ultima_instancia.abrangencia,
            status=ultima_instancia.status,
            data_inicio=ultima_instancia.data_inicio,
            data_termino=ultima_instancia.data_termino,
            endereco=endereco_response_data,
            itens_do_ciclo=itens_do_ciclo_responses,
            criado_em=ultima_instancia.criado_em,
            atualizado_em=ultima_instancia.atualizado_em
        )
