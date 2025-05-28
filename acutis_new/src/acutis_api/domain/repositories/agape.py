from abc import ABC, abstractmethod
from uuid import UUID
from typing import Optional, Any
from datetime import datetime

from acutis_api.communication.requests.agape import (
    CoordenadaFormData,
    RegistrarItemCicloAcaoAgapeFormData,
    EditarEnderecoFamiliaAgapeRequest,
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
from acutis_api.domain.repositories.schemas.paginacao import PaginacaoQuery
from acutis_api.domain.entities.instancia_acao_agape import InstanciaAcaoAgape
from acutis_api.domain.entities.item_instancia_agape import ItemInstanciaAgape
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
    NumeroMembrosFamiliaAgapeSchema,
    SomaRendaFamiliarAgapeSchema,
    TotalItensRecebidosSchema,
    InformacoesAgregadasFamiliasSchema,
    NumeroTotalMembrosSchema,
    SomaTotalRendaSchema,
    ContagemItensEstoqueSchema,
    UltimaAcaoAgapeSchema,
    UltimaEntradaEstoqueSchema,
    CoordenadasSchema,
    PaginacaoSchema,
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
    def buscar_endereco_por_id(self, endereco_id: UUID) -> Endereco | None:
        '''Busca um endereço pelo seu ID.'''
        ...

    @abstractmethod
    def buscar_ultimo_ciclo_acao_por_nome_acao_id(
        self, nome_acao_id: UUID
    ) -> InstanciaAcaoAgape | None:
        '''
        Busca a última instância de ciclo de ação ágape 
        (mais recente) associada a um nome de ação específico.
        '''
        ...
    
    @abstractmethod
    def buscar_membro_por_cpf(self, cpf: str) -> MembroAgape | None:
        '''Busca um membro ágape pelo seu CPF.'''
        ...

    @abstractmethod
    def listar_fotos_por_familia_id(
        self, familia_id: UUID
    ) -> list[FotoFamiliaAgape]:
        '''Lista todas as fotos de uma família ágape.'''
        ...

    @abstractmethod
    def buscar_data_ultimo_recebimento_familia_no_ciclo(
        self, familia_id: UUID, ciclo_acao_id: UUID
    ) -> datetime | None:
        '''Busca a data da última doação recebida 
        por uma família em um ciclo de ação específico.
        '''
        ...

    @abstractmethod
    def buscar_membro_agape_por_id(
        self, membro_agape_id: UUID
    ) -> MembroAgape | None:
        '''Busca um membro ágape pelo seu ID.'''
        ...
    
    @abstractmethod
    def registrar_membro_agape(self, membro: MembroAgape) -> MembroAgape:
        '''Registra um novo membro ágape na sessão do banco de dados.
        '''
        ...
    
    @abstractmethod
    def buscar_familia_por_id(
        self, familia_id: UUID
    ) -> Optional[FamiliaAgape]:
        pass

    @abstractmethod
    def numero_membros_familia_agape(
        self, familia_id: UUID
    ) -> NumeroMembrosFamiliaAgapeSchema:
        pass

    @abstractmethod
    def soma_renda_familiar_agape(
        self, familia: FamiliaAgape
    ) -> SomaRendaFamiliarAgapeSchema:
        pass

    @abstractmethod
    def total_itens_recebidos_por_familia(
        self, familia: FamiliaAgape
    ) -> TotalItensRecebidosSchema:
        pass

    @abstractmethod
    def informacoes_agregadas_familias(
        self
    ) -> InformacoesAgregadasFamiliasSchema:
        pass

    @abstractmethod
    def numero_total_membros_agape(self) -> NumeroTotalMembrosSchema:
        pass

    @abstractmethod
    def soma_total_renda_familiar_agape(self) -> SomaTotalRendaSchema:
        pass

    @abstractmethod
    def contagem_itens_estoque(self) -> ContagemItensEstoqueSchema:
        pass

    @abstractmethod
    def ultima_acao_agape_com_itens(
        self
    ) -> Optional[UltimaAcaoAgapeSchema]:
        pass

    @abstractmethod
    def ultima_entrada_estoque(
        self
    ) -> Optional[UltimaEntradaEstoqueSchema]:
        pass

    abstractmethod
    def deletar_familia_e_membros(self, familia: FamiliaAgape) -> None:
        # Este método irá deletar (hard delete) os membros da família
        # e depois marcar a família como deletada (soft delete).
        pass

    @abstractmethod
    def deletar_membro(self, membro_id: UUID) -> None:
        # Deleta (hard delete) um membro ágape.
        pass
    
    @abstractmethod
    def atualizar_endereco_familia(
        self, 
        familia: FamiliaAgape, 
        dados_endereco: EditarEnderecoFamiliaAgapeRequest, 
        coordenadas: Optional[CoordenadasSchema]
    ) -> FamiliaAgape:
        # Atualiza o endereço associado à família.
        # A instância 'familia' já foi buscada e validada pelo Caso de Uso.
        pass

    @abstractmethod
    def atualizar_membro_agape(
        self, membro: MembroAgape
    ) -> MembroAgape:
        # Atualiza os dados de um membro ágape.
        # A instância 'membro' já foi buscada e validada pelo Caso de Uso.
        pass

    @abstractmethod
    def listar_familias_beneficiadas_por_ciclo_acao_id(
        self, ciclo_acao_id: UUID
    ) -> list[FamiliaAgape]:
        # Lista as famílias beneficiadas por um ciclo de ação específico.
        pass

    def listar_historico_movimentacoes_paginado(
        self, pagina: int, por_pagina: int
    ) -> tuple[list[tuple[Any, str]], int]:
        """
        Lista o histórico de movimentações do estoque ágape de forma paginada.
        Retorna uma tupla contendo a lista de resultados e o número total de itens.
        Cada resultado na lista é uma tupla (entidade_historico, nome_do_item).
        """
        ...

    def listar_itens_por_doacao_agape_id(self, doacao_id: UUID) -> list[Any]:
        """
        Lista os itens de uma doação ágape específica, incluindo detalhes do item.
        Espera-se que o retorno seja uma lista de objetos ou tuplas nomeadas
        contendo: item_id, nome_item, quantidade_doada, item_doacao_agape_id, item_instancia_agape_id.
        """
        ...

    def listar_itens_recebidos_por_ciclo_e_doacao_id(
        self, ciclo_acao_id: UUID, doacao_id: UUID
    ) -> list[Any]:
        """
        Lista os itens de uma doação ágape específica, validando contra o ciclo de ação.
        Espera-se que o retorno seja uma lista de objetos ou tuplas nomeadas
        contendo: item_id, nome_item, quantidade_doada, item_doacao_agape_id, item_instancia_agape_id.
        """
        ...
    
    @abstractmethod
    def listar_voluntarios_agape(
        self, filtros: PaginacaoSchema
    ) -> tuple[list[MembroAgape], int]:
        """
        Retorna uma lista paginada de membros ágape considerados voluntários,
        baseado em filtros (ex: perfil).
        """
        ...