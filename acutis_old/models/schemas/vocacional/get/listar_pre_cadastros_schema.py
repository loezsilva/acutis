from typing import List, Optional
from pydantic import BaseModel, Field
from pydantic import BaseModel, validator
from datetime import datetime

from models.schemas.vocacional.post.registrar_ficha_vocacional_request import EstadoCivilEnum
from models.vocacional.etapa_vocacional import VocationalStepsStatusEnum
from models.vocacional.usuario_vocacional import VocationalGendersEnum


class GetPreCadastroSchema(BaseModel):
    id: int
    nome: str
    email: str
    telefone: str
    created_at: str
    status: str
    pais: str
    responsavel: Optional[str]
    justificativa: Optional[str]

    @validator("created_at", pre=True)
    def parse_data_criacao(cls, value):
        if isinstance(value, datetime):
            return value.strftime("%d/%m/%Y %H:%M:%S")
        return value

    class Config:
        orm_mode = True

class ListarPreCadastrosResponse(BaseModel):
    pre_cadastros: list[GetPreCadastroSchema]
    pages: int
    total: int
    current_page: int

class ListarPreCadastrosQuery(BaseModel):
    pais: Optional[str] = Field(None, description="Pais")
    page: int = Field(None, description="Página atual")
    per_page: int = Field(None, description="Quantidade por página")
    nome: Optional[str] = Field(None, description="Nome do vocacional")
    telefone: Optional[str] = Field(None, description="Telefone do vocacional")
    email: Optional[str] = Field(None, description="Email do vocacional")
    status: Optional[str] = Field(None, description="Status do vocacional")
    data_final: Optional[str] = Field(None, description="Data final")
    data_inicial: Optional[str] = Field(None, description="Data inicial")
    created_at: Optional[str] = Field(
        None, description="Data de criação do pré cadastro"
    )
    genero: Optional[str] = Field(None, description="Gênero do vocacional")

    class Config:
        orm_mode = True

class CadastrosVocacionalResponse(BaseModel):
    id: int = Field(None, description="ID do cadastro vocacional")
    fk_usuario_vocacional_id: int = Field(None, description="ID usuário vocacional")
    nome: str = Field(None, description="Nome vocacional")
    documento_identidade: str = Field(None, description="Documento de identificação")
    created_at: str = Field(None, description="Data da criação do cadastro")
    email: str = Field(None, description="Email do vocacional")
    data_nascimento: str = Field(None, description="Data de nascimento")
    status: VocationalStepsStatusEnum = Field(None, description="Status do cadastro")
    genero: VocationalGendersEnum = Field(None, description="Gênero do vocacional")
    rua: str = Field(None, description="Rua")
    cidade: str = Field(None, description="Cidade onde reside")
    bairro: str = Field(None, description="Bairro onde reside")
    estado: str = Field(None, description="Estado onde reside")
    numero: str = Field(None, description="Número da residência")
    cep: str = Field(None, description="Cep")
    detalhe_estrangeiro: Optional[str] = Field(None, description="Detalhe estrangeiro")
    pais: str = Field(None, description="País onde reside")
    telefone: str = Field(None, description="Telefone do vocacional")
    responsavel: str = Field(None, description="Responsável por aprovar ou recusar vocacional")
    complemento: Optional[str] = Field(None, description="Complemento endereço")

class FichaVocacionalResponse(BaseModel):
    sacramentos: List[str] = Field(None, description="Sacramentos realizados")
    status: str = Field(None, description="Status da ficha")
    motivacao_instituto: str = Field(None, description="Motivação por escolher o instituto.")
    fk_usuario_vocacional_id: int = Field(None, description="ID usuário_vocacional")
    motivacao_admissao_vocacional: str = Field(None, description="Motivação pelo processo vocacional")
    referencia_conhecimento_instituto: str = Field(None, description="Como conheceu o instituto")
    identificacao_instituto: str = Field(None, description="Pontos de identificação com o instituto")
    seminario_realizado_em: str = Field(None, description="Data de realização do seminário")
    testemunho_conversao: str = Field(None, description="Testemunho de conversão")
    escolaridade: str = Field(None, description="Escolaridade")
    profissao: str = Field(None, description="Profissão")
    cursos: Optional[str] = Field(None, description="Cursos e formações")
    rotina_diaria: str = Field(None, description="Rotina diária")
    aceitacao_familiar: str = Field(None, description="Aceitação familiar")
    estado_civil: EstadoCivilEnum = Field(None, description="Estado civíl")
    motivo_divorcio: Optional[str] = Field(None, description="Motivo do divórcio")
    deixou_religiao_anterior_em: Optional[str] = Field(None, description="Data que deixou a última religião")
    remedio_controlado_inicio: Optional[str] = Field(None, description="Data que iniciou a tomar rémedio controlado")
    remedio_controlado_termino: Optional[str] = Field(None, description="Data que finalizou o uso de rémedio controlado")
    descricao_problema_saude: Optional[str] = Field(None, description="Problema de saúde")
    foto_vocacional: str = Field(None, description="Link para foto do vocacional")
    responsavel: Optional[str] = Field(None, description="Responsável por aprovar")
    justificativa: Optional[str] = Field(None, description="Motivo pelo qual recusou")

class PreCadastro(BaseModel):
    created_at: str = Field(None, description="Data e hora da criação do pré-cadastro")
    email: str = Field(None, description="Email do vocacional")
    id: int = Field(None, description="ID do pré-cadastro")
    justificativa: Optional[str] = Field(None, description="Justificativa do status")
    nome: str = Field(None, description="Nome do vocacional")
    pais: str = Field(None, description="País onde reside")
    responsavel: str = Field(None, description="Responsável pelo pré-cadastro")
    status: str = Field(None, description="Status do pré-cadastro")
    telefone: str = Field(None, description="Telefone do vocacional")

class DesistenciasVocacionaisSchema(BaseModel):
    pre_cadastro: PreCadastro
    cadastro_vocacional: Optional[CadastrosVocacionalResponse] = None
    ficha_do_vocacional: Optional[FichaVocacionalResponse] = None

class ListarPreVocacionaisResponse(BaseModel):
    pre_cadastros: List[DesistenciasVocacionaisSchema]
    total: int
    page: int
