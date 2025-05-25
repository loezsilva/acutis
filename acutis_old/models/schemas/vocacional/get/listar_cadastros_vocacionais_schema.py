from typing import List, Optional
from pydantic import BaseModel, Field

from models.schemas.vocacional.get.listar_pre_cadastros_schema import FichaVocacionalResponse, PreCadastro
from models.vocacional.etapa_vocacional import VocationalStepsStatusEnum
from models.vocacional.usuario_vocacional import VocationalGendersEnum

class CadastroVocacionalResponse(BaseModel):
    id: int = Field(..., description="ID do cadastro vocacional")
    fk_usuario_vocacional_id: int = Field(..., description="ID usuário vocacional")
    nome: str = Field(..., description="Nome vocacional")
    documento_identidade: str = Field(..., description="Documento de identificação")
    created_at: str = Field(..., description="Data da criação do cadastro")
    email: str = Field(..., description="Email do vocacional")
    data_nascimento: str = Field(..., description="Data de nascimento")
    status: VocationalStepsStatusEnum = Field(..., description="Status do cadastro")
    genero: VocationalGendersEnum = Field(..., description="Gênero do vocacional")
    rua: str = Field(None, description="Rua")
    cidade: str = Field(None, description="Cidade onde reside")
    bairro: str = Field(None, description="Bairro onde reside")
    estado: str = Field(None, description="Estado onde reside")
    numero: str = Field(None, description="Número da residência")
    cep: str = Field(None, description="Cep")
    detalhe_estrangeiro: str = Field(None, description="Detalhe estrangeiro")
    pais: str = Field(..., description="País onde reside")
    telefone: str = Field(..., description="Telefone do vocacional")
    responsavel: str = Field(
        None, description="Responsável por aprovar ou recusar vocacional"
    )
    complemento: str = Field(None, description="Complemento endereço")
    justificativa: Optional[str] = Field(None, description="Motivo da recusa")

class ListarCadastrosVocacionaisQuery(BaseModel):
    page: int = Field(None, description="Página atual")
    per_page: int = Field(None, description="Quantidade por página")
    documento_identidade: Optional[str] = Field(None, description="Número de documento")
    email: Optional[str] = Field(None, description="Email do vocacional")
    created_at: Optional[str] = Field(
        None, description="Data de preenchimento do cadastro"
    )
    nome: Optional[str] = Field(None, description="Nome do vocacional")
    status: Optional[VocationalStepsStatusEnum] = Field(
        None, description="Status do cadastro vocacional"
    )
    genero: Optional[VocationalGendersEnum] = Field(
        None, description="Gênero masculino ou feminino"
    )
    pais: Optional[str] = Field(None, description="Pais")
    telefone: Optional[str] = Field(None, description="Telefone do vocacioal")
    data_inicial: Optional[str] = Field(None, description="Data inicial")
    data_final: Optional[str] = Field(None, description="Data final")
    telefone: Optional[str] = Field(None, description="Telefone do vocacioal")


class DesistenciasVocacionaisSchema(BaseModel):
    pre_cadastro: PreCadastro
    cadastro_vocacional: Optional[CadastroVocacionalResponse] = None
    ficha_do_vocacional: Optional[FichaVocacionalResponse] = None

class ListarCadastrosVocacionaisResponse(BaseModel):
    cadastros_vocacionais: List[DesistenciasVocacionaisSchema]
    total: int
    page: int
