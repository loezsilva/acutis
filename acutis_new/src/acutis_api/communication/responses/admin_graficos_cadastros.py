from pydantic import BaseModel, RootModel


class QuantidadeLeadsMesAtualResponse(BaseModel):
    quantidade_leads_mes_atual: int
    porcentagem: float


class QuantidadeCadastrosMesAtualResponse(BaseModel):
    quantidade_cadastro_mes_atual: int
    porcentagem: float


class QuantidadeCadastrosDiaAtualResponse(BaseModel):
    quantidade_cadastro_dia_atual: int
    porcentagem: float


class LeadsMediaMensalResponse(BaseModel):
    leads_media_mensal: int


class MembrosMediaMensalResponse(BaseModel):
    membros_media_mensal: int


class MembrosMediaDiariaResponse(BaseModel):
    membros_media_diaria: int


class ResumoQuantidadeRegistrosResponse(BaseModel):
    leads: int
    membros: int
    benfeitores: int


class GeneroSchema(BaseModel):
    quantidade: int
    porcentagem: float


class MembrosPorGeneroResponse(BaseModel):
    masculino: GeneroSchema
    feminino: GeneroSchema
    outros: GeneroSchema


class LeadsPorHoraSchema(BaseModel):
    hora: str
    quantidade: int


class QuantidadeLeadsPorHoraResponse(RootModel):
    root: list[LeadsPorHoraSchema]


class MembrosPorMesSchema(BaseModel):
    dia: str
    quantidade: int


class QuantidadeMembrosPorDiaMesAtualResponse(RootModel):
    root: list[MembrosPorMesSchema]


class LeadsPorDiaMesAtualResponse(BaseModel):
    dia: int


class LeadsPorDiaSchema(BaseModel):
    dia: str
    quantidade: int


class MembrosPorHoraSchema(BaseModel):
    hora: str
    quantidade: int


class MembrosPorHoraDiaAtualResponse(RootModel):
    root: list[MembrosPorHoraSchema]


class QuantidadeLeadsPorOrigemSchema(BaseModel):
    origem: str
    quantidade: int
    porcentagem: float


class QuantidadeLeadsPorOrigemResponse(RootModel):
    root: list[QuantidadeLeadsPorOrigemSchema]


class LeadsPorDiaSemanaSchema(BaseModel):
    dia_semana: str
    quantidade: int


class LeadsPorDiaSemanaResponse(RootModel):
    root: list[LeadsPorDiaSemanaSchema]


class LeadsPorOrigemSchema(BaseModel):
    quantidade: int
    dia: str
    campanha: str


class LeadsPorCampanhaMesAtualResponse(RootModel):
    root: list[LeadsPorOrigemSchema]


class CadastroPormesSchema(BaseModel):
    mes: str
    quantidade: int


class CadastrosPorMesResponse(RootModel):
    root: list[CadastroPormesSchema]


class MembrosPorIdadeSchema(BaseModel):
    faixa_etaria: str
    masculino: int
    feminino: int
    nao_informado: int


class CadastrosPorIdadeResponse(RootModel):
    root: list[MembrosPorIdadeSchema]


class LeadsPorEvolucaoMensalSchema(BaseModel):
    ano_mes: str
    montante_acumulado: int


class LeadsPorEvolucaoMensalResponse(RootModel):
    root: list[LeadsPorEvolucaoMensalSchema]
