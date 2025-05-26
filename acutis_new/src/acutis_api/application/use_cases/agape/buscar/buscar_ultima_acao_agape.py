from uuid import UUID
from acutis_api.domain.repositories.agape import AgapeRepositoryInterface
from acutis_api.communication.responses.agape import UltimoCicloAcaoAgapeResponse, EnderecoResponse, DoacaoAgapeResponse
from acutis_api.exception.errors.not_found import HttpNotFoundError

class BuscarUltimaAcaoAgapeUseCase:
    def __init__(self, agape_repository: AgapeRepositoryInterface):
        self._agape_repository = agape_repository

    def execute(self, nome_acao_id: UUID) -> UltimoCicloAcaoAgapeResponse:
        # 1. Verificar se o nome_acao_id (AcaoAgape) existe
        nome_acao = self._agape_repository.buscar_nome_acao_por_id(nome_acao_id)
        if not nome_acao:
            # O método buscar_nome_acao_por_id já levanta HttpNotFoundError se não encontrar
            # Esta verificação é redundante se o método do repo já levanta, mas não prejudica.
            raise HttpNotFoundError(f"Nome da ação com ID {nome_acao_id} não encontrado.")

        # 2. Buscar a última instância (ciclo) para este nome_acao_id
        ultimo_ciclo_acao = self._agape_repository.buscar_ultimo_ciclo_acao_por_nome_acao_id(nome_acao_id)
        if not ultimo_ciclo_acao:
            raise HttpNotFoundError(f"Nenhum ciclo de ação encontrado para o nome da ação com ID {nome_acao_id}.")

        # 3. Buscar o endereço associado à última instância
        endereco_response_data = None
        if ultimo_ciclo_acao.fk_endereco_id:
            endereco = self._agape_repository.buscar_endereco_por_id(ultimo_ciclo_acao.fk_endereco_id)
            if endereco:
                # Usar EnderecoResponse para popular os dados do endereço
                endereco_response_data = EnderecoResponse.model_validate(endereco)
        
        # 4. Buscar os itens/doações associados à última instância
        # O método buscar_doacoes_ciclo_acao_agape espera o ID da instância (ciclo_acao_id)
        itens_do_ciclo_schemas = self._agape_repository.buscar_doacoes_ciclo_acao_agape(ultimo_ciclo_acao.id)
        
        itens_do_ciclo_responses = [
            DoacaoAgapeResponse.model_validate(item_schema) for item_schema in itens_do_ciclo_schemas
        ]

        # 5. Montar a resposta final
        return UltimoCicloAcaoAgapeResponse(
            id=ultimo_ciclo_acao.id,
            abrangencia=ultimo_ciclo_acao.abrangencia,
            status=ultimo_ciclo_acao.status,
            data_inicio=ultimo_ciclo_acao.data_inicio,
            data_termino=ultimo_ciclo_acao.data_termino,
            endereco=endereco_response_data,
            itens_do_ciclo=itens_do_ciclo_responses,
            criado_em=ultimo_ciclo_acao.criado_em,
            atualizado_em=ultimo_ciclo_acao.atualizado_em
        )
