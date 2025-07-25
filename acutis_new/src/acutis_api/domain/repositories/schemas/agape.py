import uuid
from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field
from spectree import BaseFile

from acutis_api.domain.entities.instancia_acao_agape import StatusAcaoAgapeEnum
from acutis_api.domain.repositories.schemas.paginacao import PaginacaoQuery


class RegistrarCicloAcaoAgapeScheme(BaseModel):
    nome_acao_id: uuid.UUID
    abrangencia: str
    endereco_id: uuid.UUID


class NomeAcaoAgapeSchema(BaseModel):
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


class FamiliaBeneficiariaSchema(BaseModel):
    doacao_id: uuid.UUID
    nome_familia: str
    data_hora_doacao: Optional[str]
    recibos: list[str]


class GeoLocalizadoresFamiliaSchema(BaseModel):
    nome_familia: uuid.UUID
    latitude: float
    longitude: float


class FotoFamiliaAgapeSchema(BaseModel):
    foto: str
    familia_id: uuid.UUID


class SomaRendaFamiliarAgapeSchema(BaseModel):
    total: float


class InformacoesAgregadasFamiliasSchema(BaseModel):
    total_cadastradas: int
    total_ativas: int
    total_inativas: int


class UltimaAcaoAgapeSchema(BaseModel):
    data: date | None  # Making it optional as per potential None returns
    quantidade_itens_doados: int


class UltimaEntradaEstoqueSchema(BaseModel):
    data: date | None  # Making it optional
    quantidade: int


class CoordenadasSchema(BaseModel):
    latitude: float
    longitude: float
    latitude_ne: Optional[float] = None
    longitude_ne: Optional[float] = None
    latitude_so: Optional[float] = None
    longitude_so: Optional[float] = None


class PaginacaoSchema(PaginacaoQuery):
    pass


class DadosCompletosDoacaoSchema(BaseModel):
    ciclo_acao_id: Optional[uuid.UUID] = None
    ciclo_acao_nome: Optional[str] = None
    ciclo_acao_data_inicio: Optional[datetime] = None
    ciclo_acao_data_termino: Optional[datetime] = None
    familia_id: Optional[uuid.UUID] = None
    familia_nome: Optional[str] = None
    familia_observacao: Optional[str] = None
    responsavel_familia_nome: Optional[str] = None
    responsavel_familia_cpf: Optional[str] = None
    responsavel_familia_telefone: Optional[str] = None
    doacao_id: Optional[uuid.UUID] = None
    doacao_data: Optional[datetime] = None
    item_doado_nome: Optional[str] = None
    item_doado_quantidade: Optional[int] = None

    class Config:
        from_attributes = True


class DadosExportacaoFamiliaSchema(BaseModel):
    familia_id: uuid.UUID
    familia_nome: str
    familia_data_cadastro: Optional[datetime] = None
    familia_status: Optional[str] = None  # Ex: "Ativa", "Inativa"
    familia_observacao: Optional[str] = None
    endereco_logradouro: Optional[str] = None
    endereco_numero: Optional[str] = None
    endereco_complemento: Optional[str] = None
    endereco_bairro: Optional[str] = None
    endereco_cidade: Optional[str] = None
    endereco_estado: Optional[str] = None
    endereco_cep: Optional[str] = None
    responsavel_nome: Optional[str] = None
    responsavel_cpf: Optional[str] = None
    responsavel_telefone: Optional[str] = None
    responsavel_email: Optional[str] = None
    responsavel_data_nascimento: Optional[date] = None
    responsavel_funcao_familiar: Optional[str] = None
    responsavel_escolaridade: Optional[str] = None
    responsavel_ocupacao: Optional[str] = None
    numero_total_membros: Optional[int] = None
    renda_familiar_total_estimada: Optional[float] = None
    comprovante_residencia_url: Optional[str] = None
    cadastrada_por_usuario_id: Optional[uuid.UUID] = None

    class Config:
        from_attributes = True


class DoacaoRecebidaItemDetalheSchema(BaseModel):
    nome_item: str
    quantidade: int


class DoacaoRecebidaDetalheSchema(BaseModel):
    id: uuid.UUID
    data_doacao: datetime
    itens: list[DoacaoRecebidaItemDetalheSchema]
