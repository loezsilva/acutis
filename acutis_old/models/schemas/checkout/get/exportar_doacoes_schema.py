from pydantic import BaseModel, Field

class ExportarDoacoesResponse(BaseModel):
    url: str    
    
class ExportarRecorrenciasAtivasRequest(BaseModel):
    nome: str = Field(None, description="Nome do doador")
    campanha_id: int = Field(None, description="Id da campanha")
    data_inicio: str = Field(None, description="FIltrar a partir de")
    data_fim: str = Field(None, description="FIltrar aterior há")
    forma_pagamento: int = Field(None, description="ID da forma de pagamento")
    