import json
from datetime import date
from enum import Enum
from typing import Any, List, Optional
from uuid import UUID

from pydantic import (
    BaseModel,
    EmailStr,
    Field,
    model_validator,
)
from pydantic_core import PydanticCustomError
from spectree import BaseFile

from acutis_api.application.utils.funcoes_auxiliares import (
    now,
    valida_cpf_cnpj,
    valida_email,
    valida_nome,
)
from acutis_api.communication.requests.paginacao import PaginacaoQuery
from acutis_api.domain.entities.historico_movimentacao_agape import (
    TipoMovimentacaoEnum,
)
from acutis_api.domain.entities.instancia_acao_agape import (
    AbrangenciaInstanciaAcaoAgapeEnum,
    StatusAcaoAgapeEnum,
)


class RegistrarNomeAcaoAgapeRequest(BaseModel):
    nome: str = Field(..., min_length=3, max_length=100)

    @model_validator(mode='before')
    @classmethod
    def validar_formdata(cls, form_data: dict):
        return form_data


class EnderecoAgapeFormData(BaseModel):
    cep: str = Field(..., min_length=8, max_length=9)
    rua: str = Field(..., min_length=3, max_length=100)
    bairro: str = Field(..., min_length=3, max_length=80)
    cidade: str = Field(..., min_length=3, max_length=32)
    estado: str = Field(..., max_length=2)
    numero: str | None = Field(None, description='Número', max_length=8)
    complemento: str | None = Field(
        None, description='Complemento', max_length=60
    )

    @model_validator(mode='before')
    @classmethod
    def validar_formdata(cls, form_data: dict):
        if not str(form_data['cep']).isdigit():
            raise PydanticCustomError('cep', 'CEP aceita apenas números.')

        return form_data


class CoordenadaFormData(BaseModel):
    latitude: float
    longitude: float
    latitude_ne: float
    longitude_ne: float
    latitude_so: float
    longitude_so: float


class DoacaoAgapeRequestSchema(BaseModel):
    item_id: UUID
    quantidade: int = Field(
        ..., description='Quantidade do item no ciclo', example=1
    )


# Schema para cadastrar ciclo de ação Ágape
class RegistrarOuEditarCicloAcaoAgapeRequest(BaseModel):
    nome_acao_id: Optional[UUID] = None
    abrangencia: AbrangenciaInstanciaAcaoAgapeEnum
    endereco: EnderecoAgapeFormData
    doacoes: List[DoacaoAgapeRequestSchema]


# Filtros para listar ações com ciclos (rota listar-ciclo-acoes-agape)
class ListarCiclosAcoesAgapeQueryPaginada(PaginacaoQuery):
    nome_acao_id: Optional[UUID] = Field(
        None, description='ID do nome da ação Ágape'
    )
    status: Optional[StatusAcaoAgapeEnum] = Field(
        None,
        description=(
            'Status da ação Ágape.\n\n'
            '- `nao_iniciado`: Não iniciado\n'
            '- `em_andamento`: Em andamento\n'
            '- `finalizado`: Finalizado'
        ),
    )


class RegistrarItemEstoqueAgapeRequest(BaseModel):
    item: str = Field(
        ..., description='Nome do item', min_length=3, max_length=100
    )

    @model_validator(mode='before')
    @classmethod
    def validar_formdata(cls, form_data: dict):
        return form_data


class ListarItensEstoqueAgapeQueryPaginada(PaginacaoQuery):
    item: Optional[str] = Field(None, description='Nome do item')


class ItemQuantityValidation:
    @model_validator(mode='before')
    @classmethod
    def validar_formdata(cls, form_data: dict):
        if int(form_data['quantidade']) < 0:
            raise PydanticCustomError(
                'quantidade', 'A quantidade deve ser maior ou igual a 1.'
            )
        return form_data


# Form data para abastecer item de estoque
class AbastecerItemEstoqueAgapeRequest(BaseModel, ItemQuantityValidation):
    quantidade: int = Field(
        ..., gt=0, description='Quantidade a acrescentar', example=1
    )


# Form data para remover quantidade de item de estoque
class RemoverItemEstoqueAgapeRequest(BaseModel, ItemQuantityValidation):
    quantidade: int = Field(
        ..., description='Quantidade a subtrair', example=1
    )


class RegistrarItemCicloAcaoAgapeFormData(BaseModel, ItemQuantityValidation):
    item_id: UUID = Field(..., description='ID do item')
    quantidade: int = Field(..., description='Quantidade', example=1)


class MembroFamiliaAgapeFormData(BaseModel):
    responsavel: bool
    nome: str = Field(..., min_length=3, max_length=100)
    email: EmailStr = Field(..., max_length=100)
    telefone: str = Field(..., min_length=9, max_length=20)
    cpf: str = Field(..., min_length=11, max_length=14)
    data_nascimento: date
    funcao_familiar: str = Field(..., min_length=3, max_length=50)
    escolaridade: str = Field(..., min_length=3, max_length=50)
    ocupacao: str = Field(..., min_length=3, max_length=100)
    renda: Optional[float] = None
    beneficiario_assistencial: Optional[bool] = False
    foto_documento: Optional[str] = None

    @model_validator(mode='before')
    @classmethod
    def validar_formdata(cls, form_data: dict):
        if not str(form_data['cpf']).isdigit():
            raise PydanticCustomError('cpf', 'CPF aceita apenas números.')

        if not str(form_data['telefone']).isdigit():
            raise PydanticCustomError(
                'telefone', 'Telefone aceita apenas números.'
            )

        return form_data


class RegistrarOuEditarFamiliaAgapeFormData(BaseModel):
    endereco: EnderecoAgapeFormData
    membros: list[MembroFamiliaAgapeFormData]
    observacao: Optional[str] = Field('', max_length=255)
    comprovante_residencia: BaseFile | None = None
    fotos_familia: list[BaseFile] = []

    @model_validator(mode='before')
    @classmethod
    def validar_formdata(cls, form_data: dict[str, Any]) -> dict[str, Any]:
        form_data = dict(form_data)

        membros_key = 'membros'
        endereco_key = 'endereco'

        if membros_key in form_data:
            membros_data = form_data[membros_key]

            if isinstance(membros_data, str):
                membros_data = [membros_data]

            if isinstance(membros_data, list):
                try:
                    membros = [
                        json.loads(m) if isinstance(m, str) else m
                        for m in membros_data
                    ]
                except json.JSONDecodeError:
                    raise PydanticCustomError(
                        'value_error', "'membros' deve conter JSONs válidos."
                    )

                for membro in membros:
                    nome_valido, erro = valida_nome(membro.get('nome', ''))
                    if not nome_valido:
                        raise PydanticCustomError('nome', erro)

                    email_valido, erro = valida_email(
                        email=membro.get('email', ''),
                        verificar_entregabilidade=True,
                        verificar_dominio=False,
                    )
                    if not email_valido:
                        raise PydanticCustomError('email', erro)

                    cpf = membro.get('cpf', '')
                    if not valida_cpf_cnpj(cpf, 'cpf', gerar_excesao=False):
                        raise PydanticCustomError(
                            'cpf', f'O cpf {cpf} é inválido.'
                        )

                form_data[membros_key] = membros

        if endereco_key in form_data and isinstance(
            form_data[endereco_key], str
        ):
            try:
                form_data[endereco_key] = json.loads(form_data[endereco_key])
            except json.JSONDecodeError:
                raise PydanticCustomError(
                    'value_error', "'endereco' deve ser um JSON válido."
                )

        return form_data


class ListarMembrosFamiliaAgapeQueryPaginada(PaginacaoQuery):
    pass


# Schemas para cadastrar membros em uma família ágape
class MembroAgapeCadastroItemSchema(BaseModel):
    responsavel: Optional[bool] = Field(
        ..., description='Indica se o membro é o responsável pela família'
    )
    nome: str = Field(
        ...,
        description='Nome completo do membro',
        min_length=3,
        max_length=100,
    )
    email: Optional[EmailStr] = Field(
        None,
        description='Email do membro',
        min_length=3,
        max_length=100,
    )
    telefone: Optional[str] = Field(
        None,
        description='Telefone do membro',
        max_length=20,
    )
    cpf: Optional[str] = Field(
        None,
        description='CPF do membro',
        pattern=r'^\d{3}\.\d{3}\.\d{3}-\d{2}$',
        max_length=14,
    )
    data_nascimento: date = Field(
        ..., description='Data de nascimento do membro (YYYY-MM-DD)'
    )
    funcao_familiar: str = Field(
        None,
        description='Função do membro na família (ex: Pai, Mãe, Filho)',
        min_length=3,
        max_length=50,
    )
    escolaridade: str = Field(
        None,
        description='Nível de escolaridade do membro',
        min_length=5,
        max_length=50,
    )
    ocupacao: Optional[str] = Field(
        None,
        description='Ocupação atual do membro',
        min_length=3,
        max_length=50,
    )
    renda: Optional[float] = Field(
        None, description='Renda mensal do membro', ge=0
    )
    beneficiario_assistencial: bool = Field(
        None,
        description='Indica se o membro é beneficiário de \
            algum programa assistencial',
    )
    foto_documento: BaseFile = Field(
        None, description='Foto do documento do membro'
    )


class MembrosAgapeCadastroRequest(BaseModel):
    membros: list[MembroAgapeCadastroItemSchema]

    class Config:
        from_attributes = True
        json_schema_extra = {
            'example': [
                {
                    'responsavel': True,
                    'nome': 'Fulano de Tal Atualizado',
                    'email': 'fulano.atualizado@example.com',
                    'telefone': '11987654321',
                    'cpf': '12345678900',
                    'data_nascimento': '1990-01-15',
                    'funcao_familiar': 'Pai',
                    'escolaridade': 'Ensino Superior Completo',
                    'ocupacao': 'Engenheiro de Software',
                    'renda': 5000.00,
                    'foto_documento': '(Foto do documento em base64)',
                    'beneficiario_assistencial': False,
                }
            ]
        }


class EditarEnderecoFamiliaAgapeRequest(BaseModel):
    model_config = {'extra': 'forbid'}  # Pydantic v2 style for ConfigDict

    cep: str = Field(
        ..., min_length=8, max_length=9, description='CEP (somente números)'
    )
    rua: str = Field(
        ..., min_length=3, max_length=100, description='Logradouro/Rua'
    )
    numero: str = Field(
        ..., max_length=10, description='Número'
    )  # Max length assumption
    complemento: Optional[str] = Field(
        None, max_length=100, description='Complemento'
    )  # Max length assumption
    ponto_referencia: Optional[str] = Field(
        None, max_length=255, description='Ponto de referência'
    )  # Max length assumption
    bairro: str = Field(..., min_length=3, max_length=80, description='Bairro')
    cidade: str = Field(..., min_length=3, max_length=32, description='Cidade')
    estado: str = Field(
        ..., min_length=2, max_length=2, description='Estado (UF, ex: SP)'
    )


class EditarMembroAgapeFormData(BaseModel):
    responsavel: Optional[bool] = Field(
        ..., description='Indica se o membro é o responsável pela família'
    )
    nome: str = Field(
        ...,
        description='Nome completo do membro',
        min_length=3,
        max_length=100,
    )
    email: Optional[EmailStr] = Field(
        None,
        description='Email do membro',
        min_length=3,
        max_length=100,
    )
    telefone: Optional[str] = Field(
        None,
        description='Telefone do membro',
        max_length=20,
    )
    cpf: Optional[str] = Field(
        None,
        description='CPF do membro',
        pattern=r'^\d{3}\.\d{3}\.\d{3}-\d{2}$',
        max_length=14,
    )
    data_nascimento: date = Field(
        ..., description='Data de nascimento do membro (YYYY-MM-DD)'
    )
    funcao_familiar: str = Field(
        None,
        description='Função do membro na família (ex: Pai, Mãe, Filho)',
        min_length=3,
        max_length=50,
    )
    escolaridade: str = Field(
        None,
        description='Nível de escolaridade do membro',
        min_length=5,
        max_length=50,
    )
    ocupacao: Optional[str] = Field(
        None,
        description='Ocupação atual do membro',
        min_length=3,
        max_length=50,
    )
    renda: Optional[float] = Field(
        None, description='Renda mensal do membro', ge=0
    )
    beneficiario_assistencial: bool = Field(
        None,
        description='Indica se o membro é beneficiário de \
            algum programa assistencial',
    )
    foto_documento: BaseFile = Field(
        None, description='Foto do documento do membro'
    )

    class Config:
        from_attributes = True
        json_schema_extra = {
            'example': {
                'responsavel': True,
                'nome': 'Fulano de Tal Atualizado',
                'email': 'fulano.atualizado@example.com',
                'telefone': '11987654321',
                'cpf': '12345678900',
                'data_nascimento': '1990-01-15',
                'funcao_familiar': 'Pai',
                'escolaridade': 'Ensino Superior Completo',
                'ocupacao': 'Engenheiro de Software',
                'renda': 5000.00,
                'foto_documento': '',
                'beneficiario_assistencial': False,
            }
        }


class ListarHistoricoMovimentacoesAgapeQueryPaginada(PaginacaoQuery):
    item_id: Optional[UUID] = None
    tipo_movimentacao: Optional[TipoMovimentacaoEnum] = None
    data_movimentacao_inicial: Optional[date] = None
    data_movimentacao_final: Optional[date] = now().date()


class ItemDoacaoInputSchema(BaseModel):
    item_instancia_id: UUID
    quantidade: int = Field(
        ..., gt=0, description='Quantidade do item a ser doado'
    )


class RegistrarDoacaoAgapeRequestSchema(BaseModel):
    familia_id: UUID
    ciclo_acao_id: UUID
    doacoes: List[ItemDoacaoInputSchema]

    @model_validator(mode='before')
    @classmethod
    def check_itens_not_empty(cls, values):
        doacoes = values.get('doacoes')
        if not doacoes:
            raise ValueError('A lista de doações não pode estar vazia.')
        return values


class InfoPermissaoVoluntarioSchema(BaseModel):
    lead_id: UUID
    perfis_agape: List[str]


class RegistrarRecibosRequestSchema(BaseModel):
    recibo: str = Field(..., description='URL ou identificador do recibo')


class RegistrarRecibosRequestFormData(BaseModel):
    recibos: List[BaseFile] = Field(..., min_items=1, max_items=2)


class ReceiptsEnum(str, Enum):
    com_recibo = 'com_recibo'
    sem_recibo = 'sem_recibo'


class BeneficiariosCicloAcaoQuery(PaginacaoQuery):
    cpf: Optional[str] = Field(None, max_length=14)
    data_inicial: Optional[date] = Field(None)
    data_final: Optional[date] = Field(now().date())
    recibos: Optional[ReceiptsEnum] = Field(None)
