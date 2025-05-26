import uuid
from datetime import date, datetime

from pydantic import BaseModel, EmailStr, Field
from spectree import BaseFile

from acutis_api.domain.entities.instancia_acao_agape import StatusAcaoAgapeEnum
from acutis_api.domain.repositories.schemas.paginacao import PaginacaoQuery


class RegistrarNomeAcaoAgapeSchema(BaseModel):
    nome: str


class RegistrarCicloAcaoAgapeScheme(BaseModel):
    nome_acao_id: uuid.UUID
    abrangencia: str
    endereco_id: uuid.UUID


class NomeAcaoAgapeSchema(BaseModel):
    id: uuid.UUID
    nome: str


class ListarNomesAcoesAgapeFiltros(PaginacaoQuery):
    id: uuid.UUID
    nome: str


class EstoqueAgapeSchema(BaseModel):
    id: uuid.UUID
    item: str
    quantidade: int


class InstanciaItemAgapeSchema(BaseModel):
    id: uuid.UUID
    item: str
    quantidade: int


class ItemDoacaoCicloAgapeSchema(BaseModel):
    fk_item_instancia_agape_id: uuid.UUID
    item: str
    quantidade: int


class RegistrarItemEstoqueAgapeSchema(BaseModel):
    item: str
    quantidade: int


class ListarItensEstoqueAgapeFiltros(PaginacaoQuery):
    id: uuid.UUID
    item: str
    quantidade: int


# Esquema de doação em ciclo de ação Ágape
class DoacaoAgapeSchema(BaseModel):
    id: uuid.UUID
    item_id: uuid.UUID
    item: str
    quantidade: int


class ListarCicloAcoesAgapeFiltros(PaginacaoQuery):
    fk_acao_id: uuid.UUID | None = Field(None, description='ID da ação Ágape')
    data_inicial: datetime | None = Field(
        None, description='Data inicial de cadastro'
    )
    data_final: datetime | None = Field(
        None, description='Data final de cadastro'
    )
    filtros: str | None = Field(None, description='Filtros de busca')
    status: StatusAcaoAgapeEnum | None = Field(
        None, description='Status da ação Ágape'
    )


class ListarCiclosAcoesAgapeScheme(BaseModel):
    acao_id: uuid.UUID
    endereco_id: uuid.UUID
    data_cadastro_inicial: datetime
    data_cadastro_final: datetime
    status: StatusAcaoAgapeEnum


class CicloAcaoAgapeResponse(BaseModel):
    id: uuid.UUID
    nome: str
    data_cadastro: datetime
    ciclos_finalizados: int


class MembroFamiliaSchema(BaseModel):
    responsavel: bool = False
    nome: str
    familia_id: uuid.UUID
    data_nascimento: date
    email: EmailStr = Field(None, max_length=100)
    telefone: str = Field(None, max_length=20)
    cpf: str = Field(None, max_length=14)
    funcao_familiar: str = Field(None, min_length=3, max_length=50)
    escolaridade: str
    ocupacao: str | None = None
    renda: float | None = None
    beneficiario_assistencial: bool | None = False
    foto_documento: str | None = None


class RegistrarFamiliaAgapeSchema(BaseModel):
    nome_familia: str
    endereco_id: uuid.UUID
    observacao: str | None = None
    comprovante_residencia: BaseFile
    cadastrada_por: uuid.UUID


class EnderecoScheme(BaseModel):
    cep: str
    rua: str
    bairro: str
    cidade: str
    estado: str
    numero: str
    complemento: str


class FotoFamiliaAgapeSchema(BaseModel):
    foto: str
    familia_id: uuid.UUID

class ListarMembrosFamiliaAgapeFiltros(PaginacaoQuery): 
    familia_id: uuid.UUID

class NumeroMembrosFamiliaAgapeSchema(BaseModel):
    quantidade: int

class SomaRendaFamiliarAgapeSchema(BaseModel):
    total: float

class TotalItensRecebidosSchema(BaseModel):
    total_recebidas: int

class InformacoesAgregadasFamiliasSchema(BaseModel):
    total_cadastradas: int
    total_ativas: int
    total_inativas: int

class NumeroTotalMembrosSchema(BaseModel):
    quantidade_total_membros: int

class SomaTotalRendaSchema(BaseModel):
    soma_total_renda: float

class ContagemItensEstoqueSchema(BaseModel):
    em_estoque: int

class UltimaAcaoAgapeSchema(BaseModel):
    data: date | None # Making it optional as per potential None returns
    quantidade_itens_doados: int

class UltimaEntradaEstoqueSchema(BaseModel):
    data: date | None # Making it optional
    quantidade: int