from uuid import UUID
from acutis_api.domain.repositories.agape import AgapeRepositoryInterface
from acutis_api.communication.responses.agape import EnderecoCicloAcaoResponse
from acutis_api.exception.errors.not_found import HttpNotFoundError

class BuscarEnderecoCicloAcaoUseCase:
    def __init__(self, agape_repository: AgapeRepositoryInterface):
        self._agape_repository = agape_repository

    def execute(self, ciclo_acao_id: UUID) -> EnderecoCicloAcaoResponse:
        instancia_acao_agape = self._agape_repository.buscar_instancia_acao_agape_por_id(ciclo_acao_id)
        # buscar_instancia_acao_agape_por_id já levanta HttpNotFoundError se não encontrado.

        if not instancia_acao_agape.fk_endereco_id:
            raise HttpNotFoundError(f"Ciclo de ação ágape {ciclo_acao_id} não possui endereço associado (fk_endereco_id está nulo).")

        endereco_entity = self._agape_repository.buscar_endereco_por_id(instancia_acao_agape.fk_endereco_id)
        # buscar_endereco_por_id já levanta HttpNotFoundError se não encontrado.

        # Montar a resposta usando EnderecoCicloAcaoResponse
        # Os campos de endereço virão de endereco_entity
        # O campo 'abrangencia' virá de instancia_acao_agape.abrangencia
        
        response_data = {
            "id": endereco_entity.id, # ID do Endereço
            "codigo_postal": endereco_entity.codigo_postal,
            "logradouro": endereco_entity.logradouro,
            "numero": endereco_entity.numero,
            "complemento": endereco_entity.complemento,
            "bairro": endereco_entity.bairro,
            "cidade": endereco_entity.cidade,
            "estado": endereco_entity.estado,
            "ponto_referencia": endereco_entity.ponto_referencia,
            "latitude": endereco_entity.latitude,
            "longitude": endereco_entity.longitude,
            "abrangencia": instancia_acao_agape.abrangencia
        }
        return EnderecoCicloAcaoResponse.model_validate(response_data)
