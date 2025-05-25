from typing import Optional
from pydantic import BaseModel, Field

from models.schemas.vocacional.get.listar_cadastros_vocacionais_schema import (
    CadastroVocacionalResponse,
)
from models.schemas.vocacional.get.listar_fichas_vocacionais_schema import (
    FichaVocacionalResponseSchema,
)
from models.schemas.vocacional.get.listar_pre_cadastros_schema import (
    GetPreCadastroSchema,
)
from models.schemas.vocacional.post.registrar_ficha_vocacional_request import (
    EstadoCivilEnum,
)
from models.vocacional.etapa_vocacional import VocationalStepsStatusEnum
from models.vocacional.usuario_vocacional import VocationalGendersEnum


class CadastrosRecusadosResponse(BaseModel):
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
    detalhe_estrangeiro: str = Field(None, description="Detalhe estrangeiro")
    pais: str = Field(None, description="País onde reside")
    telefone: str = Field(None, description="Telefone do vocacional")
    responsavel: str = Field(
        None, description="Responsável por aprovar ou recusar vocacional"
    )
    complemento: str = Field(None, description="Complemento endereço")


class FichaVocacionalRecusadosResponse(BaseModel):
    sacramentos: list = Field(None, description="Sacramentos realizados")
    status: str = Field(None, description="Status da ficha")
    motivacao_instituto: str = Field(
        None, description="Motivação por escolher o instituto."
    )
    fk_usuario_vocacional_id: int = Field(None, description="ID usuário_vocacional")
    motivacao_admissao_vocacional: str = Field(
        None, description="Motivação pelo processo vocacional"
    )
    referencia_conhecimento_instituto: str = Field(
        None, description="Como conheceu o instituto"
    )
    identificacao_instituto: str = Field(
        None, description="Pontos de identificação com o instituto"
    )
    seminario_realizado_em: str = Field(
        None, description="Data de realização do seminário"
    )
    testemunho_conversao: str = Field(None, description="Testemunho de conversão")
    escolaridade: str = Field(None, description="Escolaridade")
    profissao: str = Field(None, description="Profissão")
    cursos: Optional[str] = Field(None, description="Cursos e formações")
    rotina_diaria: str = Field(None, description="Rotina diária")
    aceitacao_familiar: str = Field(None, description="Aceitação familiar")
    estado_civil: EstadoCivilEnum = Field(None, description="Estado civíl")
    motivo_divorcio: Optional[str] = Field(None, description="Motivo do divórcio")
    deixou_religiao_anterior_em: Optional[str] = Field(
        None, description="Data que deixou a última religião"
    )
    remedio_controlado_inicio: Optional[str] = Field(
        None, description="Data que iniciou a tomar rémedio controlado"
    )
    remedio_controlado_termino: Optional[str] = Field(
        None, description="Data que finalizou o uso de rémedio controlado"
    )
    descricao_problema_saude: Optional[str] = Field(
        None, description="Problema de saúde"
    )
    foto_vocacional: str = Field(None, description="Link para foto do vocacional")
    responsavel: str = Field(None, description="Responsável por aprovar")
    justificativa: str = Field(None, description="Motivo pelo qual recusou")


class VocacionaisRecusadosQuery(BaseModel):
    data_inicial: str = Field(None, description="Data inicial")
    data_final: str = Field(None, description="Data final")
    nome: str = Field(None, description="Nome do vocacional")
    email: str = Field(None, description="Email do vocacional")
    desistencia_em: str = Field(None, description="Data da desistência")
    etapa: str = Field(None, description="Etapa a qual desistiu")
    pais: str = Field(None, description="País onde reside")
    page: int = Field(None, description="Page")
    per_page: int = Field(None, description="Per Page")
    pais: str = Field(None, description="Pais")
    telefone: str = Field(None, description="Telefone vocacional")
    genero: str = Field(None, description="Gênero vocacional")
    status: str = Field(None, description="Status vocacional")
    documento_identidade: str = Field(None, description="Documento de identidade")
    justificativa: str = Field(None, description="Motivo pelo qual recusou")

class InformacoesDaReprovacao(BaseModel):
    recusado_em: str
    recusado_por: str
    justificativa: Optional[str]

class VocacionaisRecusadosSchema(BaseModel):
    pre_cadastro: GetPreCadastroSchema
    cadastro_vocacional: Optional[CadastrosRecusadosResponse] = None
    ficha_do_vocacional: Optional[FichaVocacionalRecusadosResponse] = None
    informacoes_da_reprovacao: InformacoesDaReprovacao


class VocacionaisRecusadosResponse(BaseModel):
    recusados: list[VocacionaisRecusadosSchema]
    total: int
    page: int
 