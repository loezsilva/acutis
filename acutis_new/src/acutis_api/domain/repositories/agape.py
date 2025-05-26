from abc import ABC, abstractmethod
from uuid import UUID

from acutis_api.communication.requests.agape import (
    CoordenadaFormData,
    RegistrarItemCicloAcaoAgapeFormData,
)
from acutis_api.domain.entities.acao_agape import AcaoAgape
from acutis_api.domain.entities.coordenada import Coordenada
from acutis_api.domain.entities.endereco import Endereco
from acutis_api.domain.entities.estoque_agape import EstoqueAgape
from acutis_api.domain.entities.familia_agape import FamiliaAgape
from acutis_api.domain.entities.foto_familia_agape import FotoFamiliaAgape
from acutis_api.domain.entities.historico_movimentacao_agape import (
    HistoricoMovimentacaoAgape,
)
from datetime import datetime # Added
from acutis_api.domain.entities.instancia_acao_agape import InstanciaAcaoAgape
from acutis_api.domain.entities.item_instancia_agape import ItemInstanciaAgape
# MembroAgape is already imported below, ensuring it's available.
# FotoFamiliaAgape is already imported.
from acutis_api.domain.entities.membro_agape import MembroAgape
from acutis_api.domain.repositories.schemas.agape import (
    DoacaoAgapeSchema,
    EnderecoScheme,
    EstoqueAgapeSchema,
    FotoFamiliaAgapeSchema,
    ListarItensEstoqueAgapeFiltros,
    ListarNomesAcoesAgapeFiltros,
    MembroFamiliaSchema,
    NomeAcaoAgapeSchema,
    RegistrarCicloAcaoAgapeScheme,
    RegistrarFamiliaAgapeSchema,
    RegistrarItemEstoqueAgapeSchema,
    RegistrarNomeAcaoAgapeSchema,
)


class AgapeRepositoryInterface(ABC):
    @abstractmethod
    def salvar_alteracoes(self): ...

    @abstractmethod
    def verificar_nome_da_acao(self, nome_acao: str) -> tuple: ...

    @abstractmethod
    def buscar_acao_por_nome(self, nome_acao: str) -> AcaoAgape | None: ...

    @abstractmethod
    def buscar_nome_acao_por_id(
        self, nome_acao_id: UUID
    ) -> EstoqueAgape | None: ...

    @abstractmethod
    def buscar_ciclo_acao_agape_por_id(
        self, acao_agape_id: UUID
    ) -> InstanciaAcaoAgape | None: ...

    @abstractmethod
    def buscar_itens_ciclo_acao_agape(
        self, acao_agape_id: UUID
    ) -> list[DoacaoAgapeSchema]: ...

    @abstractmethod
    def buscar_endereco_ciclo_acao_agape(
        self, acao_agape_id: UUID
    ) -> Endereco | None: ...

    @abstractmethod
    def buscar_doacoes_ciclo_acao_agape(
        self, acao_agape_id: UUID
    ) -> list[DoacaoAgapeSchema]: ...

    @abstractmethod
    def deletar_item_ciclo_acao_agape(self, item_ciclo_id: UUID) -> None: ...

    @abstractmethod
    def retorna_item_estoque_ciclo_acao_agape(
        self, item_ciclo_id: UUID
    ) -> None: ...

    @abstractmethod
    def listar_itens_ciclo_acao_agape(
        self, acao_agape_id: UUID
    ) -> list[ItemInstanciaAgape]: ...

    @abstractmethod
    def registrar_nome_acao_agape(
        self, acao_agape: RegistrarNomeAcaoAgapeSchema
    ) -> AcaoAgape: ...

    @abstractmethod
    def registrar_endereco(self, dados: EnderecoScheme) -> Endereco: ...

    @abstractmethod
    def registrar_coordenada(
        self, endereco_id: UUID, dados: CoordenadaFormData
    ) -> Coordenada: ...

    @abstractmethod
    def listar_nomes_acoes_agape(
        self, filtros: ListarNomesAcoesAgapeFiltros
    ) -> tuple[list[NomeAcaoAgapeSchema], int]: ...

    @abstractmethod
    def verificar_item_estoque(self, item: str) -> tuple: ...

    @abstractmethod
    def registrar_item_estoque(
        self, dados: RegistrarItemEstoqueAgapeSchema
    ) -> EstoqueAgape: ...

    @abstractmethod
    def listar_itens_estoque_agape(
        self, filtros: ListarItensEstoqueAgapeFiltros
    ) -> tuple[list[EstoqueAgapeSchema], int]: ...

    @abstractmethod
    def buscar_item_estoque_por_id(
        self, item_id: UUID
    ) -> EstoqueAgape | None: ...

    @abstractmethod
    def registrar_ciclo_acao_agape(
        self, dados: RegistrarCicloAcaoAgapeScheme
    ) -> InstanciaAcaoAgape:
        """
        Registra um novo ciclo de ação Ágape completo:
        - Persiste o endereço
        - Cria a instância do ciclo
        - Processa doações: ajusta estoque, itens do ciclo e histórico
        Deve lançar exceção para controle de fluxo em caso de erro.
        """
        ...

    @abstractmethod
    def remover_item_estoque(self, item: EstoqueAgape) -> None: ...

    @abstractmethod
    def listar_ciclos_acao(
        self, filtros
    ) -> tuple[list[InstanciaAcaoAgape], int]:
        """
        Retorna lista paginada de instâncias de ciclo de ação Ágape,
        aplicando filtros de ação e status.
        """
        ...
        
    @abstractmethod
    def listar_familias(
        self, filtros
    ) -> tuple[list[FamiliaAgape], int]:
        """
            Retorna lista de famílias,
        """
        ...
        
    @abstractmethod
    def listar_membros_por_familia_id(
        self, familia_id: UUID
    ) -> list[MembroAgape]:
        """
            Retorna lista de membros de uma família,
        """
        ...

    @abstractmethod
    def iniciar_ciclo_acao_agape(self, ciclo_acao) -> InstanciaAcaoAgape: ...

    @abstractmethod
    def finalizar_ciclo_acao_agape(self, ciclo_acao) -> InstanciaAcaoAgape: ...

    @abstractmethod
    def deletar_ciclo_acao_agape(
        self, acao_agape_id
    ) -> InstanciaAcaoAgape: ...

    @abstractmethod
    def registrar_item_ciclo_acao_agape(
        self, ciclo_acao_id, dados: RegistrarItemCicloAcaoAgapeFormData
    ) -> None: ...

    @abstractmethod
    def registrar_familia(
        self, dados: RegistrarFamiliaAgapeSchema
    ) -> FamiliaAgape: ...

    @abstractmethod
    def registrar_membro_familia(
        self, dados: MembroFamiliaSchema
    ) -> MembroAgape: ...

    @abstractmethod
    def registrar_foto_familia(
        self, dados: FotoFamiliaAgapeSchema
    ) -> FotoFamiliaAgape: ...

    @abstractmethod
    def buscar_membro_familia_por_id(self, membro_id: UUID) -> MembroAgape: ...

    @abstractmethod
    def verificar_membro_familia_por_email(
        self, email: str
    ) -> MembroAgape: ...

    @abstractmethod
    def verificar_ciclo_acao_iniciado(
        self, ciclo_acao: InstanciaAcaoAgape
    ) -> InstanciaAcaoAgape: ...

    @abstractmethod
    def verificar_ciclo_acao_finalizado(
        self, ciclo_acao: InstanciaAcaoAgape
    ) -> InstanciaAcaoAgape: ...

    @abstractmethod
    def verficar_membro_familia_por_cpf(self, cpf: str) -> MembroAgape: ...

    @abstractmethod
    def movimentar_historico_ciclo_acao_agape(
        self,
        item_id,
        ciclo_acao_id,
        quantidade,
    ) -> HistoricoMovimentacaoAgape: ...

    @abstractmethod
    def adicionar_voluntario_agape(self, lead_id: UUID) -> None: ...

    @abstractmethod
    def buscar_familia_agape_por_id(self, familia_id: UUID) -> FamiliaAgape | None:
        '''Busca uma família ágape pelo seu ID.'''
        ...

    @abstractmethod
    def buscar_endereco_por_id(self, endereco_id: UUID) -> Endereco | None:
        '''Busca um endereço pelo seu ID.'''
        ...

    @abstractmethod
    def buscar_instancia_acao_agape_por_id(self, ciclo_acao_id: UUID) -> InstanciaAcaoAgape | None:
        '''Busca uma instância de ciclo de ação ágape pelo seu ID.'''
        ...

    @abstractmethod
    def buscar_ultima_instancia_por_nome_acao_id(self, nome_acao_id: UUID) -> InstanciaAcaoAgape | None:
        '''Busca a última instância de ciclo de ação ágape (mais recente) associada a um nome de ação específico.'''
        ...

    @abstractmethod
    def buscar_membro_por_cpf(self, cpf: str) -> MembroAgape | None:
        '''Busca um membro ágape pelo seu CPF.'''
        ...

    @abstractmethod
    def listar_fotos_por_familia_id(self, familia_id: UUID) -> list[FotoFamiliaAgape]:
        '''Lista todas as fotos de uma família ágape.'''
        ...

    @abstractmethod
    def buscar_data_ultimo_recebimento_familia_no_ciclo(self, familia_id: UUID, ciclo_acao_id: UUID) -> datetime | None:
        '''Busca a data da última doação recebida por uma família em um ciclo de ação específico.'''
        ...

    @abstractmethod
    def buscar_membro_agape_por_id(self, membro_agape_id: UUID) -> MembroAgape | None:
        '''Busca um membro ágape pelo seu ID.'''
        ...