from datetime import date, datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field, validator
from spectree import BaseFile


class EstadoCivilEnum(str, Enum):
    CASADO = "Casado(a)"
    SOLTEIRO = "Solteiro(a)"
    DIVORCIADO = "Divorciado(a)"
    VIUVO = "Viúvo(a)"
    UNIAOESTAVEL = "União Estável"


class FormFichaVocacionalSchema(BaseModel):
    sacramentos: list = Field(..., description="Sacramentos realizados.")
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
    seminario_realizado_em: date = Field(
        ..., description="Data de realização do seminário"
    )
    testemunho_conversao: str = Field(..., description="Testemunho de conversão")
    escolaridade: str = Field(..., description="Escolaridade")
    profissao: str = Field(..., description="Profissão")
    cursos: Optional[str] = Field(None, description="Cursos e formações")
    rotina_diaria: str = Field(..., description="Rotina diária")
    aceitacao_familiar: str = Field(..., description="Aceitação familiar")
    estado_civil: Optional[EstadoCivilEnum] = Field(None, description="Estado civíl")
    motivo_divorcio: Optional[str] = Field(None, description="Motivo do divórcio")
    deixou_religiao_anterior_em: Optional[date] = Field(
        None, description="Data que deixou a última religião"
    )
    remedio_controlado_inicio: Optional[date] = Field(
        None, description="Data que iniciou a tomar rémedio controlado"
    )
    remedio_controlado_termino: Optional[date] = Field(
        None, description="Data que finalizou o uso de rémedio controlado"
    )
    descricao_problema_saude: Optional[str] = Field(
        None, description="Problema de saúde"
    )

    @validator(
        "seminario_realizado_em",
        "deixou_religiao_anterior_em",
        "remedio_controlado_inicio",
        "remedio_controlado_termino",
        pre=True,
    )
    def parse_dates(cls, value):
        if isinstance(value, str):
            return datetime.strptime(value, "%Y-%m-%d").date()
        return value


class RegistrarFichaVocacionalFormData(BaseModel):
    ficha_vocacional: str = Field(
        ...,
        description="""
            {
                "fk_usuario_vocacional_id": pre_cadastro.id,
                "motivacao_instituto": "Sestãoociedade.",
                "motivacao_admissao_vocacional": "De melhor através da minha vocação.",
                "referencia_conhecimento_instituto": "Conheci o instituto através de um amigo que já participou do processo vocacional.",
                "identificacao_instituto": "Me identifico com a forma como o instituto promove a justiça social e o desenvolvimento comunitário.",
                "testemunho_conversao": "Minha conversão começou após uma experiência profunda durante um retiro espiritual, onde senti um chamado pa",
                "escolaridade": "Ensino Superior Completo",
                "profissao": "Professor",
                "cursos": "Licenciatura em História, Pós-graduação em Educação Inclusiva",
                "rotina_diaria": "Acordo às 6h, vou para a escola onde leciono, à tarde estudo e à noite participo de grupos de oração",
                "aceitacao_familiar": "Minha família apoia minha decisão, embora tenham suas preocupações.",
                "estado_civil": "Solteiro(a)",
                "motivo_divorcio": None,
                "seminario_realizado_em": "2023-03-15",
                "deixou_religiao_anterior_em": "2020-05-20",
                "remedio_controlado_inicio": "2019-08-10",
                "remedio_controlado_termino": "2021-02-15",
                "sacramentos": ["eucaristia", "crisma", "teste"],
                "descricao_problema_saude": "Tive um período de depressão, mas atualmente estou bem e sem necessidade de medicação."
            }
        """,
    )
