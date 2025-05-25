from datetime import date, datetime, timezone, timedelta
import logging
from typing import List, Optional
from models.pedido import Pedido
from models.processamento_pedido import ProcessamentoPedido
from utils.enums.checkout import Status, TipoPagamento, TipoPagamentoMP
from pydantic import BaseModel, constr, SecretStr, EmailStr, Field
from builder import db
from utils.functions import get_current_time
from models import ListExceptionDonations


def register_order(
    campanha,
    clifor,
    reference_num,
    valor_doacao,
    forma_pagamento,
    periodo,
    id_pedido,
    id_transacao,
    fk_gateway_pagamento_id,
    vencimento_cartao=None,
    nosso_numero=None,
    status_processamento=0,
    create_transaction: bool = True,
):
    try:

        contabilizar_doacao = True

        clifor_in_list_exception_donations = (
            db.session.query(ListExceptionDonations)
            .filter(ListExceptionDonations.fk_clifor_id == clifor.id)
            .first()
        )

        if clifor_in_list_exception_donations is not None:
            contabilizar_doacao = False

        recorrencia_ativa = True if periodo == 2 else False
        with db.session.begin_nested():
            pedido = Pedido(
                fk_empresa_id=campanha.fk_empresa_id,
                fk_clifor_id=clifor.id,
                fk_campanha_id=campanha.id,
                fk_forma_pagamento_id=forma_pagamento,
                data_pedido=get_current_time(),
                periodicidade=periodo,
                status_pedido=1,
                valor_total_pedido=valor_doacao,
                order_id=id_pedido,
                recorrencia_ativa=recorrencia_ativa,
                vencimento_cartao=vencimento_cartao,
                fk_gateway_pagamento_id=fk_gateway_pagamento_id,
                usuario_criacao=clifor.fk_usuario_id,
                contabilizar_doacao=contabilizar_doacao,
            )

            db.session.add(pedido)

            if create_transaction:
                db.session.flush()

                processamento_pedido = ProcessamentoPedido(
                    fk_empresa_id=campanha.fk_empresa_id,
                    fk_pedido_id=pedido.id,
                    fk_clifor_id=clifor.id,
                    fk_forma_pagamento_id=forma_pagamento,
                    data_processamento=get_current_time(),
                    valor=valor_doacao,
                    status_processamento=status_processamento,
                    id_transacao_gateway=reference_num,
                    transaction_id=id_transacao,
                    nosso_numero=nosso_numero,
                    usuario_criacao=clifor.fk_usuario_id,
                )

                db.session.add(processamento_pedido)

            db.session.commit()
    except Exception as err:
        logging.error(f"{type(err)} - {err}")
        db.session.rollback()
        raise Exception(f"{type(err)} - {err}")


class CheckoutUserUpdateSchema(BaseModel):
    nome: str
    data_nascimento: Optional[date]
    sexo: Optional[str]
    telefone: Optional[str]
    tipo_clifor: constr(min_length=1, max_length=1)  # type: ignore
    cep: Optional[str]
    street: Optional[str]
    complemento: Optional[str]
    numero: Optional[str]
    neighborhood: Optional[str]
    city: Optional[str]
    state: Optional[str]
    cargo_id: Optional[int]
    usuario_superior_id: Optional[int]


class CheckoutUserCreateSchema(BaseModel):
    nome: str
    email: EmailStr
    cpf_cnpj: constr(min_length=5, max_length=24)  # type: ignore
    data_nascimento: Optional[date]
    telefone: str
    sexo: str
    password: SecretStr
    cep: Optional[str]
    rua: Optional[str]
    complemento: Optional[str]
    numero: Optional[str]
    bairro: Optional[str]
    estado: Optional[str]
    cidade: Optional[str]
    fk_empresa_id: int
    tipo_clifor: constr(min_length=1, max_length=1)  # type: ignore
    fk_campanha_id: Optional[int]
    fk_landpage_id: Optional[int]
    brasileiro: Optional[bool]
    fk_cargo_id: Optional[int]
    usuario_superior_id: Optional[int]
    campanha_origem: str
    detalhe_estrangeiro: Optional[str]
    country: str


class CheckoutUserResponseSchema(BaseModel):
    msg: str
    access_token: str
    refresh_token: str
    type_token: str


class CheckoutCreditCardSchema(BaseModel):
    numero_cartao: str
    validade_cartao_mes: constr(min_length=2, max_length=2)  # type: ignore
    validade_cartao_ano: constr(min_length=2, max_length=2)  # type: ignore
    codigo_seguranca_cartao: constr(min_length=3, max_length=4)  # type: ignore
    nome_titular_cartao: str
    cpf_cnpj_titular_cartao: str
    valor_doacao: float
    fk_campanha_id: int
    device_id: Optional[str]


class CheckoutDonationsQuerySchema(BaseModel):
    page: Optional[int]
    per_page: Optional[int]
    tipo_pagamento: Optional[TipoPagamento] = Field(
        description="```1``` - Cartão de crédito, ```2``` - Pix, ```3``` - Boleto"
    )
    pedido_por_campanha: Optional[int] = Field(
        description="ID da campanha para filtrar as doações por campanha"
    )
    status: Optional[Status] = Field(
        description="```0``` - Em processamento, ```1``` - Pago, ```2``` - Não Efetuado, ```3``` - Expirado"
    )
    data_inicial: Optional[datetime] = (
        datetime.now(timezone.utc) - timedelta(days=1)
    ).strftime("%Y-%m-%d %H:%M:%S")
    data_final: Optional[datetime] = datetime.now(timezone.utc).strftime(
        "%Y-%m-%d %H:%M:%S"
    )
    nome_cliente: Optional[str]
    recorrencia: Optional[str] = None
    listagem_completa: Optional[bool] = False
    fk_gateway_pagamento_id: Optional[int]
    area_admin: Optional[bool]


class CheckoutDonationsResponseSchema(BaseModel):
    valor_doacao: float
    nome: Optional[str]
    data_doacao: datetime
    forma_pagamento: str
    descricao_campanha: str
    recorrencia: bool
    status: str
    codigo_referencia: str
    order_id: Optional[str]
    transaction_id: Optional[str]
    fk_pedido_id: int
    titulo_campanha: str
    imagem_campanha: str
    anonimo: Optional[bool]
    recorrencia_ativa: Optional[bool]


class CheckoutDonationsResponseListSchema(BaseModel):
    page: int
    pages: int
    total: int
    doacoes: List[CheckoutDonationsResponseSchema]


class CheckoutCreditCardPaymentResponseSchema(BaseModel):
    id_pedido: Optional[str]
    id_transacao: Optional[str]
    response_code: int
    numero_referencia: str
    processor_message: Optional[str]
    msg: str


class CheckoutCreditCardPaymentErrorResponseSchema(BaseModel):
    id_pedido: Optional[str]
    id_transacao: Optional[str]
    response_code: int
    numero_referencia: Optional[str]
    processor_message: Optional[str]
    error: str


class CheckoutCreditCardCancelRecurrenceErrorSchema(BaseModel):
    error: str
    error_message: str


class CheckoutTransactionsSchema(BaseModel):
    data_transacao: str
    valor_transacao: str
    status_transacao: str
    tipo_pagamento: str
    id_transacao: str


class CheckoutTransactionResponseListSchema(BaseModel):
    __root__: List[CheckoutTransactionsSchema]


class PixCreateSchema(BaseModel):
    periodicidade: int = Field(description="```1``` - Único, ```2``` - Mensal")
    fk_campanha_id: int
    valor_doacao: float


class PixCalendarSchema(BaseModel):
    criacao: str
    dataDeVencimento: str
    validadeAposVencimento: int


class PixQRCodeSchema(BaseModel):
    imagem_base64: str
    pix_link: str
    emv: str


class PixReceiverSchema(BaseModel):
    cep: str
    cidade: str
    cnpj: str
    logradouro: str
    nome: str
    nomeFantasia: str
    uf: str


class PixTransactionResponseSchema(BaseModel):
    calendario: PixCalendarSchema
    pix_qrcode: PixQRCodeSchema
    recebedor: PixReceiverSchema
    status: str
    txid: str
    valor: str
    msg: str


class InvoiceTransactionSchema(BaseModel):
    valor_doacao: float
    fk_campanha_id: int
    periodicidade: int


class CheckoutPaymentMP(BaseModel):
    descricao_pagamento: Optional[str]
    periodicidade: int = Field(description="```1``` - Único, ```2``` - Mensal")
    tipo_pagamento: TipoPagamentoMP
    fk_campanha_id: int
    valor_doacao: float


class CheckoutCreditCardPaymentMP(BaseModel):
    numero_cartao: str
    validade_cartao_mes: constr(min_length=2, max_length=2)  # type: ignore
    validade_cartao_ano: constr(min_length=4, max_length=4)  # type: ignore
    codigo_seguranca_cartao: constr(min_length=3, max_length=4)  # type: ignore
    nome_titular_cartao: str
    cpf_cnpj_titular_cartao: str
    valor_doacao: float
    fk_campanha_id: int
