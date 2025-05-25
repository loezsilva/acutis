from typing import List, Optional, Dict
from pydantic import BaseModel, Field

from models.schemas.vocacional.get.listar_cadastros_vocacionais_schema import (
    CadastroVocacionalResponse,
)
from models.schemas.vocacional.get.listar_pre_cadastros_schema import GetPreCadastroSchema
from models.schemas.vocacional.post.registrar_ficha_vocacional_request import (
    EstadoCivilEnum,
)
from models.vocacional.etapa_vocacional import VocationalStepsStatusEnum
from models.vocacional.usuario_vocacional import VocationalGendersEnum


class ListarFichasVocacionaisQuery(BaseModel):
    pais: Optional[str] = Field(None, description="Pais do vocacional")
    status: Optional[VocationalStepsStatusEnum] = Field(None, description="Status")
    genero: Optional[VocationalGendersEnum] = Field(
        None, description="Gênero masculino ou feminino"
    )
    email: Optional[str] = Field(None, description="Email do vocacional")
    nome: Optional[str] = Field(None, description="Nome do vocacionanal")
    documento_identidade: str = Field(None, description="Documento de idetidade")
    data_inicial: str = Field(None, description="Data filtro de inicio")
    data_final: str = Field(None, description="Data filtro final")
    fk_usuario_vocacional_id: int = Field(None, description="ID usuário vocacional")
    telefone: Optional[str] = Field(None, description="Telefone do vocacional")
    page: Optional[int] = Field(None, description="Page")
    per_page: Optional[int] = Field(None, description="Per page")
    fk_usuario_vocacional_id: Optional[int] = Field(None, description="ID vocacional")


class FichaVocacionalResponseSchema(BaseModel):
    sacramentos: list = Field(..., description="Sacramentos realizados")
    status: str = Field(..., description="Status da ficha")
    motivacao_instituto: str = Field(
        ..., description="Motivação por escolher o instituto."
    )
    fk_usuario_vocacional_id: int = Field(..., description="ID usuário_vocacional")
    motivacao_admissao_vocacional: str = Field(
        ..., description="Motivação pelo processo vocacional"
    )
    referencia_conhecimento_instituto: str = Field(
        ..., description="Como conheceu o instituto"
    )
    identificacao_instituto: str = Field(
        ..., description="Pontos de identificação com o instituto"
    )
    seminario_realizado_em: str = Field(
        ..., description="Data de realização do seminário"
    )
    testemunho_conversao: str = Field(..., description="Testemunho de conversão")
    escolaridade: str = Field(..., description="Escolaridade")
    profissao: str = Field(..., description="Profissão")
    cursos: Optional[str] = Field(None, description="Cursos e formações")
    rotina_diaria: str = Field(..., description="Rotina diária")
    aceitacao_familiar: str = Field(..., description="Aceitação familiar")
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
    foto_vocacional: str = Field(..., description="Link para foto do vocacional")
    responsavel: str = Field(None, description="Responsável por aprovar")
    justificativa: Optional[str] = Field(None, description="Motivo da recusa")
    

class SchemaFichaDoVocacional(BaseModel):
    cadastro_vocacional: CadastroVocacionalResponse
    ficha_do_vocacional: FichaVocacionalResponseSchema
    pre_cadastro: GetPreCadastroSchema


class ListarFichasVocacionaisResponse(BaseModel):
    fichas_vocacionais: List[SchemaFichaDoVocacional]
    total: int
    page: int
