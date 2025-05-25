from enum import Enum


class FormaPagamentoEnum(str, Enum):
    pix = 'pix'
    credito = 'credito'
    boleto = 'boleto'


class GatewayPagamentoEnum(str, Enum):
    maxipago = 'maxipago'
    mercado_pago = 'mercado_pago'
    itau = 'itau'


class StatusProcessamentoEnum(str, Enum):
    pendente = 'pendente'
    pago = 'pago'
    expirado = 'expirado'
    estornado = 'estornado'
    sem_filtro = None


class ListarDoacoesOrdenarPorEnum(str, Enum):
    benfeitor_id = 'benfeitor_id'
    benfeitor_nome = 'benfeitor_nome'
    lead_id = 'lead_id'
    membro_id = 'membro_id'
    campanha_id = 'campanha_id'
    campanha_nome = 'campanha_nome'
    doacao_id = 'doacao_id'
    doacao_criada_em = 'doacao_criada_em'
    doacao_cancelada_em = 'doacao_cancelada_em'
    pagamento_doacao_id = 'pagamento_doacao_id'
    valor_doacao = 'valor_doacao'
    recorrente = 'recorrente'
    forma_pagamento = 'forma_pagamento'
    codigo_ordem_pagamento = 'codigo_ordem_pagamento'
    anonimo = 'anonimo'
    gateway = 'gateway'
    ativo = 'ativo'
    processamento_doacao_id = 'processamento_doacao_id'
    processado_em = 'processado_em'
    codigo_referencia = 'codigo_referencia'
    codigo_transacao = 'codigo_transacao'
    codigo_comprovante = 'codigo_comprovante'
    nosso_numero = 'nosso_numero'
    status = 'status'
