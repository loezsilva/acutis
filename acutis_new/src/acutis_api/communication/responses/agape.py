import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, model_validator

from acutis_api.communication.responses.padrao import PaginacaoResponse
from acutis_api.domain.entities.instancia_acao_agape import (
    AbrangenciaInstanciaAcaoAgapeEnum,
    StatusAcaoAgapeEnum,
)
from acutis_api.domain.entities.familia_agape import FamiliaAgape
from acutis_api.application.utils.funcoes_auxiliares import calcular_idade


class RegistrarAcaoAgapeResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    nome: str


class AcaoAgapeResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    nome: str


class ListarNomesAcoesAgapeResponsePaginada(PaginacaoResponse):
    resultados: list[AcaoAgapeResponse]


class EnderecoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    codigo_postal: str | None
    logradouro: str | None
    bairro: str | None
    cidade: str | None
    estado: str | None
    numero: str | None
    complemento: str | None
    ponto_referencia: str | None
    latitude: float | None
    longitude: float | None


# Estoque Ágape
class ItemEstoqueAgapeResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    item: str
    quantidade: int


class RegistrarItemEstoqueAgapeResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    item: str


class ListarItensEstoqueAgapeResponsePaginada(PaginacaoResponse):
    resultados: list[ItemEstoqueAgapeResponse]


# Resposta para detalhes de um ciclo de ação Ágape
class DoacaoAgapeResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    item_id: uuid.UUID
    item: str
    quantidade: int


class BuscarCicloAcaoAgapeResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    abrangencia: AbrangenciaInstanciaAcaoAgapeEnum
    endereco: EnderecoResponse
    doacoes: list[DoacaoAgapeResponse]


class BuscarItensCicloAcaoAgapeResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    resultados: list[DoacaoAgapeResponse]


# Resposta para instâncias de ciclo de ação Ágape
class InstanciaCicloAgapeResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
    )

    id: uuid.UUID
    endereco_id: uuid.UUID
    acao_id: uuid.UUID
    data_inicio: datetime | None
    data_termino: datetime | None
    status: StatusAcaoAgapeEnum
    abrangencia: AbrangenciaInstanciaAcaoAgapeEnum


# Resposta para listagem de instâncias de ciclo de ação Ágape
class ListarCiclosAcoesAgapeResponsePaginada(PaginacaoResponse):
    resultados: list[InstanciaCicloAgapeResponse]


# Resposta para listagem de ações ágape com contagem de ciclos
class AcaoAgapeCicloResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    nome: str
    data_cadastro: str
    ciclos_finalizados: int


class ListarCicloAcoesAgapeResponsePaginada(PaginacaoResponse):
    resultados: list[AcaoAgapeCicloResponse]

class MembroFamiliaAgapeResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: uuid.UUID
    cpf: str | None
    nome: str
    email: str | None
    telefone: str | None
    ocupacao: str
    renda: float | None
    responsavel: bool
    idade: int | None

class FamiliaAgapeResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
    )
    
    id: uuid.UUID
    nome_familia: str
    cadastrada_por: uuid.UUID
    endereco_id: uuid.UUID
    observacao: str | None
    criado_em: datetime | None
    membros: list[MembroFamiliaAgapeResponse]

class ListarFamiliasAgapeResponsePaginada(PaginacaoResponse):
    resultados: list[FamiliaAgapeResponse]
    
class ListarMembrosFamiliaAgapeResponsePaginada(PaginacaoResponse):
    resultados: list[MembroFamiliaAgapeResponse]


class EnderecoCicloAcaoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    # Campos do EnderecoResponse achatados
    id: uuid.UUID # ID do Endereço
    codigo_postal: str | None
    logradouro: str | None
    numero: str | None
    complemento: str | None
    bairro: str | None
    cidade: str | None
    estado: str | None
    ponto_referencia: str | None
    latitude: float | None
    longitude: float | None
    
    # Campo específico do ciclo de ação
    abrangencia: AbrangenciaInstanciaAcaoAgapeEnum


class UltimoCicloAcaoAgapeResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID  # ID da InstanciaAcaoAgape (o ciclo)
    abrangencia: AbrangenciaInstanciaAcaoAgapeEnum
    status: StatusAcaoAgapeEnum # Usando o Enum diretamente
    data_inicio: datetime | None
    data_termino: datetime | None
    endereco: EnderecoResponse | None
    itens_do_ciclo: list[DoacaoAgapeResponse]
    criado_em: datetime
    atualizado_em: datetime