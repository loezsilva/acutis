import json
from datetime import date
from typing import List, Optional
from uuid import UUID

from pydantic import (
    BaseModel,
    EmailStr,
    Field,
    model_validator,
    constr, # Added constr
)
from pydantic_core import PydanticCustomError
# Optional and List are already imported via 'from typing import List, Optional'
from spectree import BaseFile

from acutis_api.application.utils.funcoes_auxiliares import (
    valida_cpf_cnpj,
    valida_email,
    valida_nome,
)
from acutis_api.communication.requests.paginacao import PaginacaoQuery
from acutis_api.domain.entities.instancia_acao_agape import (
    AbrangenciaInstanciaAcaoAgapeEnum,
    StatusAcaoAgapeEnum,
)


class RegistrarNomeAcaoAgapeFormData(BaseModel):
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
class RegistrarOuEditarCicloAcaoAgapeFormData(BaseModel):
    nome_acao_id: UUID = Field(..., description='ID da ação Ágape')
    abrangencia: AbrangenciaInstanciaAcaoAgapeEnum
    endereco: EnderecoAgapeFormData
    doacoes: List[DoacaoAgapeRequestSchema]


class ListarNomesAcoesAgapeQueryPaginada(PaginacaoQuery):
    nome: Optional[str] = Field(None, description='Nome da ação')


# Filtros para listar ações com ciclos (rota listar-ciclo-acoes-agape)
class ListarCiclosAcoesAgapeQueryPaginada(PaginacaoQuery):
    acao_id: Optional[UUID] = Field(None, description='ID da ação Ágape')
    data_cadastro_inicial: Optional[date] = Field(
        None, description='Data inicial de cadastro'
    )
    data_cadastro_final: Optional[date] = Field(
        None, description='Data final de cadastro'
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


class RegistrarItemEstoqueAgapeFormData(BaseModel):
    item: str = Field(
        ..., description='Nome do item', min_length=3, max_length=100
    )
    quantidade: int = Field(..., description='Quantidade do item', example=1)

    @model_validator(mode='before')
    @classmethod
    def validar_formdata(cls, form_data: dict):
        return form_data


class ListarItensEstoqueAgapeQueryPaginada(PaginacaoQuery):
    item: Optional[str] = Field(None, description='Nome do item')


# Form data para abastecer item de estoque
class AbastecerItemEstoqueAgapeFormData(BaseModel):
    quantidade: int = Field(
        ..., description='Quantidade a acrescentar', example=1
    )

    @model_validator(mode='before')
    @classmethod
    def validar_formdata(cls, form_data: dict):
        if int(form_data['quantidade']) < 0:
            raise PydanticCustomError(
                'quantidade', 'A quantidade deve ser maior ou igual a 1.'
            )
        return form_data


# Form data para remover quantidade de item de estoque
class RemoverItemEstoqueAgapeFormData(BaseModel):
    quantidade: int = Field(
        ..., description='Quantidade a subtrair', example=1
    )

    @model_validator(mode='before')
    @classmethod
    def validar_formdata(cls, form_data: dict):
        if int(form_data['quantidade']) < 0:
            raise PydanticCustomError(
                'quantidade', 'A quantidade deve ser maior ou igual a 1.'
            )
        return form_data


class RegistrarItemCicloAcaoAgapeFormData(BaseModel):
    item_id: UUID = Field(..., description='ID da ação Ágape')
    quantidade: int = Field(..., description='Quantidade', example=1)

    @model_validator(mode='before')
    @classmethod
    def validar_formdata(cls, form_data: dict):
        if int(form_data['quantidade']) < 0:
            raise PydanticCustomError(
                'quantidade', 'A quantidade deve ser maior ou igual a 1.'
            )
        return form_data


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
    beneficiario_assistencial: Optional[float] = False
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
    comprovante_residencia: BaseFile = None
    fotos_familia: list[BaseFile] = None

    @model_validator(mode='before')
    @classmethod
    def validar_formdata(cls, form_data: dict):
        form_data = form_data.copy()

        if 'membros' in form_data and isinstance(form_data['membros'], str):
            try:
                if not form_data['membros'].startswith('['):
                    form_data['membros'] = f'[{form_data["membros"]}]'
                form_data['membros'] = json.loads(form_data['membros'])

                for membro in form_data['membros']:
                    nome_valido, erro = valida_nome(membro['nome'])
                    if not nome_valido:
                        raise PydanticCustomError('nome', erro)

                    email_valido, erro = valida_email(
                        email=membro['email'],
                        verificar_entregabilidade=True,
                        verificar_dominio=False,
                    )
                    if not email_valido:
                        raise PydanticCustomError('email', erro)

                    if not valida_cpf_cnpj(
                        membro['cpf'], 'cpf', gerar_excesao=False
                    ):
                        raise PydanticCustomError(
                            'cpf', f'O cpf {membro["cpf"]} é inválido.'
                        )

            except json.JSONDecodeError:
                raise PydanticCustomError(
                    'value_error', "'membros' deve ser um JSON valido."
                )

        if 'endereco' in form_data and isinstance(form_data['endereco'], str):
            try:
                form_data['endereco'] = json.loads(form_data['endereco'])
            except json.JSONDecodeError:
                raise PydanticCustomError(
                    'value_error', "'endereco' deve ser um JSON valido."
                )

        return form_data

class ListarFamiliasAgapeQueryPaginada(PaginacaoQuery):
    pass

class ListarMembrosFamiliaAgapeQueryPaginada(PaginacaoQuery):
    pass

class AdicionarVoluntarioAgapeFormData(BaseModel):
    lead_id: UUID = Field(
        ..., description='ID do Lead'
    )

# Schemas para cadastrar membros em uma família ágape
class MembroAgapeCadastroItemSchema(BaseModel):
    responsavel: bool = False
    nome: constr(min_length=3, max_length=100, strip_whitespace=True) # type: ignore
    email: EmailStr | None = None 
    telefone: str | None = None 
    cpf: str | None = None 
    data_nascimento: date
    funcao_familiar: constr(min_length=1, max_length=50, strip_whitespace=True) # type: ignore
    escolaridade: constr(min_length=1, max_length=50, strip_whitespace=True) # type: ignore
    ocupacao: constr(min_length=1, max_length=100, strip_whitespace=True) # type: ignore
    renda: float | None = Field(default=None, ge=0)
    beneficiario_assistencial: bool = False
    foto_documento: str | None = None # Esperado como string base64

class MembrosAgapeCadastroRequestSchema(BaseModel):
    membros: list[MembroAgapeCadastroItemSchema]