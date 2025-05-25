from pydantic import BaseModel


class GetAgapeFamiliesInfoSchema(BaseModel):
    cadastradas: int
    ativas: int
    inativas: int


class GetNumberRegisteredAgapeMembersSchema(BaseModel):
    quantidade: int


class GetSumAgapeFamiliesIncomeSchema(BaseModel):
    total: float


class GetNumberStockItemsSchema(BaseModel):
    em_estoque: int


class GetLastAgapeActionSchema(BaseModel):
    data: str
    quantidade_itens_doados: int


class GetLastStockSupplySchema(BaseModel):
    data: str
    quantidade: int


class GetTotalDonationsReceiptsSchema(BaseModel):
    total_recebidas: int
