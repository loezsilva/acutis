import uuid
from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict

from acutis_api.application.utils.funcoes_auxiliares import (
    transforma_string_para_data,
)
from acutis_api.communication.responses.padrao import PaginacaoResponse
from acutis_api.domain.entities.historico_movimentacao_agape import (
    TipoMovimentacaoEnum,
)
from acutis_api.domain.entities.instancia_acao_agape import (
    AbrangenciaInstanciaAcaoAgapeEnum,
    StatusAcaoAgapeEnum,
)


def format_datetime(value):
    return value.strftime('%d/%m/%Y %H:%M')


def format_date(value):
    return value.strftime('%d/%m/%Y')


def parse_value(value):
    if isinstance(value, datetime):
        return format_datetime(value)
    if isinstance(value, date):
        return format_date(value)
    if isinstance(value, str):
        parsed = transforma_string_para_data(value)
        return format_datetime(parsed) if parsed else value
    if isinstance(value, (list, dict)):
        return parse_datas_padrao_brasileiro(value)
    return value


def parse_datas_padrao_brasileiro(obj):
    if isinstance(obj, list):
        return [parse_datas_padrao_brasileiro(item) for item in obj]
    if isinstance(obj, dict):
        return {key: parse_value(value) for key, value in obj.items()}
    return obj


class AcaoAgapeResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    nome: str


class ListarNomesAcoesAgapeResponsePaginada(BaseModel):
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


class EnderecoComCoordenadasResponse(EnderecoResponse):
    latitude: float | None = None
    longitude: float | None = None


# Estoque Ágape
class ItemEstoqueAgapeResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    item: str
    quantidade: int


class ListarItensEstoqueAgapeResponsePaginada(BaseModel):
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
    nome_acao_id: uuid.UUID
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
    nome_acao_id: uuid.UUID
    status: StatusAcaoAgapeEnum


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
    comprovante_residencia: str | None


class ListarFamiliasAgapeResponsePaginada(PaginacaoResponse):
    resultados: list[FamiliaAgapeResponse]


class ListarMembrosFamiliaAgapeResponsePaginada(PaginacaoResponse):
    resultados: list[MembroFamiliaAgapeResponse]


class EnderecoCicloAcaoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    # Campos do EnderecoResponse achatados
    id: uuid.UUID  # ID do Endereço
    codigo_postal: str | None
    logradouro: str | None
    numero: str | None
    complemento: str | None
    bairro: str | None
    cidade: str | None
    estado: str | None

    # Campo específico do ciclo de ação
    abrangencia: AbrangenciaInstanciaAcaoAgapeEnum


class NomeAcaoAgapeResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID  # ID da InstanciaAcaoAgape (o ciclo)
    abrangencia: AbrangenciaInstanciaAcaoAgapeEnum
    endereco: EnderecoResponse | None
    doacoes: list[DoacaoAgapeResponse]


class FamiliaAgapePorCpf(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    nome_familia: str
    observacao: str | None
    comprovante_residencia_url: str | None
    criado_em: datetime
    ativo: bool
    ultimo_recebimento: datetime | None


class FamiliaAgapeDetalhesPorCpfResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    familia: FamiliaAgapePorCpf
    endereco: EnderecoResponse | None
    fotos_familia_urls: list[str]


class MembroAgapeDetalhesResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    nome: str
    email: str | None
    telefone: str | None
    cpf: str | None
    data_nascimento: date
    responsavel: bool
    funcao_familiar: str
    escolaridade: str
    ocupacao: str
    renda: float | None
    foto_documento_url: str | None
    beneficiario_assistencial: bool


class CardRendaFamiliarAgapeResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    renda_familiar: str
    renda_per_capta: str


class CardTotalRecebimentosAgapeResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    total_itens_recebidos: str


class CardsEstatisticasFamiliasAgapeResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    familias_cadastradas: str
    renda_media: str
    membros_por_familia: str
    familias_ativas: str
    familias_inativas: str


class CardsEstatisticasItensEstoqueResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    itens_em_estoque: str
    ultima_acao: str
    ultima_entrada: str


class FamiliaBeneficiariaResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    doacao_id: uuid.UUID
    nome_familia: str
    data_hora_doacao: Optional[str] = None
    recibos: list[str] = []


class ListarBeneficiariosAgapeResponse(PaginacaoResponse):
    resultados: list[FamiliaBeneficiariaResponse]


class EnderecoFamiliaAgapeResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    familia_id: uuid.UUID
    nome_familia: str
    # Campos do EnderecoResponse original
    endereco_id: uuid.UUID  # ID do Endereço em si
    codigo_postal: Optional[str] = None
    logradouro: Optional[str] = None
    bairro: Optional[str] = None
    cidade: Optional[str] = None
    estado: Optional[str] = None
    numero: Optional[str] = None
    complemento: Optional[str] = None


class ListarEnderecosFamiliasAgapeResponse(BaseModel):
    resultados: list[EnderecoComCoordenadasResponse]


class GeolocalizacaoBeneficiarioResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    nome_familia: str
    latitude: float
    longitude: float


class ListarGeolocalizacoesBeneficiariosResponse(BaseModel):
    ciclo_acao_id: uuid.UUID
    resultados: list[GeolocalizacaoBeneficiarioResponse]

    class Config:
        from_attributes = True
        json_schema_extra = {
            'example': [
                {
                    'nome_familia': 'Família Silva',
                    'latitude': -23.550520,
                    'longitude': -46.633308,
                    'endereco_id': 'e1f2a3b4-c5d6-e7f8-a9b0-c1d2e3f4a5b6',
                },
                {
                    'nome_familia': 'Família Santos',
                    'latitude': -22.906847,
                    'longitude': -43.172896,
                },
            ]
        }


class HistoricoMovimentacaoItemAgapeResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    item_id: uuid.UUID
    quantidade: int
    tipo_movimentacao: TipoMovimentacaoEnum
    data_movimentacao: datetime


class ListarHistoricoMovimentacoesAgapeResponsePaginada(PaginacaoResponse):
    resultados: list[HistoricoMovimentacaoItemAgapeResponse]

    class Config:
        from_attributes = True
        json_schema_extra = {
            'example': {
                'pagina': 1,
                'paginas': 5,
                'total': 50,
                'resultados': [
                    {
                        'id': 'd1e2f3a4...',
                        'item_id': 'a1b2c3d4...',
                        'nome_item': 'Arroz Tipo 1',
                        'quantidade': 100,
                        'tipo_movimentacao': 'entrada',
                        'data_movimentacao': '2023-10-26T10:00:00Z',
                    },
                    {
                        'id': 'e2f3a4b5...',
                        'item_id': 'b2c3d4e5...',
                        'nome_item': 'Feijão Carioca',
                        'quantidade': 50,
                        'tipo_movimentacao': 'saida',
                        'data_movimentacao': '2023-10-27T14:30:00Z',
                    },
                ],
            }
        }


# Schemas para Itens Doados a um Beneficiário em um Ciclo de Ação
class ItemDoadoBeneficiarioResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    nome_item: str
    quantidade: int


class ListarItensDoadosBeneficiarioResponse(BaseModel):
    resultados: list[ItemDoadoBeneficiarioResponse]

    class Config:
        from_attributes = True
        json_schema_extra = {
            'example': [
                {
                    'nome_item': 'Arroz Parboilizado - 5kg',
                    'quantidade': 2,
                },
                {
                    'nome_item': 'Feijão Preto - 1kg',
                    'quantidade': 3,
                },
            ]
        }


class VoluntarioAgapeResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    nome: str
    email: str | None
    telefone: str | None
    perfil: str | None


class ListarVoluntariosAgapeResponse(PaginacaoResponse):
    resultados: list[VoluntarioAgapeResponse]


class RegistrarDoacaoAgapeResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    msg: str
    doacao_id: uuid.UUID


class AtualizacaoPermissaoStatus(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    lead_id: uuid.UUID
    status: str
    perfis_concedidos: Optional[list[str]] = None


# Schemas para Registrar Recibos de Doação Ágape (Response)
class ReciboAgapeResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    fk_doacao_agape_id: uuid.UUID
    recibo: str
    criado_em: datetime


class RegistrarRecibosResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    recibos_criados: list[ReciboAgapeResponse]


class ListarStatusPermissaoVoluntariosResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    acessar: bool
    criar: bool
    editar: bool
    deletar: bool


class DoacaoRecebidaItemDetalheSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    nome_item: str
    quantidade: int


class DoacaoRecebidaDetalheSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    nome_acao: str
    doacao_id: uuid.UUID
    ciclo_acao_id: uuid.UUID
    dia_horario: datetime
    recibos: list[str] | str


class ListarDoacoesRecebidasFamiliaResponse(PaginacaoResponse):
    resultados: list[DoacaoRecebidaDetalheSchema]
