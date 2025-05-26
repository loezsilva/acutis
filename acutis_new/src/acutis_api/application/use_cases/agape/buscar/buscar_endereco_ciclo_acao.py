from uuid import UUID
from acutis_api.domain.repositories.agape import AgapeRepositoryInterface
from acutis_api.communication.responses.agape import EnderecoCicloAcaoResponse
from acutis_api.exception.errors.not_found import HttpNotFoundError

class BuscarEnderecoCicloAcaoUseCase:
    def __init__(self, agape_repository: AgapeRepositoryInterface):
        self._agape_repository = agape_repository

    def execute(self, ciclo_acao_id: UUID) -> EnderecoCicloAcaoResponse:
        
        ciclo_acao = self._agape_repository.buscar_ciclo_acao_agape_por_id(ciclo_acao_id)
        # buscar_ciclo_acao_por_id já levanta HttpNotFoundError se não encontrado.

        if not ciclo_acao.fk_endereco_id:
            raise HttpNotFoundError(f"Ciclo de ação ágape {ciclo_acao_id} não possui endereço associado (fk_endereco_id está nulo).")

        endereco = self._agape_repository.buscar_endereco_por_id(ciclo_acao.fk_endereco_id)
        
        response_data = {
            "id": endereco.id, # ID do Endereço
            "codigo_postal": endereco.codigo_postal,
            "logradouro": endereco.logradouro,
            "numero": endereco.numero,
            "complemento": endereco.complemento,
            "bairro": endereco.bairro,
            "cidade": endereco.cidade,
            "estado": endereco.estado,
            "abrangencia": ciclo_acao.abrangencia
        }
        return EnderecoCicloAcaoResponse.model_validate(response_data)