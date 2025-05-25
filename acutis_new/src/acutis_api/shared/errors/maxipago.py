from http import HTTPStatus

ERROS_MAXIPAGO = {
    '1': 'Transação não autorizada, revise suas informações de pagamento.',
    '2': 'Transação recusada por suspeita de fraude ou duplicidade.',
    '5': 'Transação em análise manual de fraude.',
    '1022': 'Erro na operadora do cartão.',
    '1023': 'Transação rejeitada pelo parceiro.',
    '1024': 'Erro nos parâmetros enviados.',
    '1025': 'Erro nas credenciais de acesso.',
    '2048': 'Erro interno na MaxiPago.',
    '4097': 'Tempo de resposta esgotado com a adquirente.',
}


class ErroPagamento(Exception):
    def __init__(self, message: str):
        self.name = 'Erro no Pagamento'
        self.status_code = HTTPStatus.BAD_REQUEST
        self.message = message


class ErroRecorrenciaNaoEncontrada(Exception):
    def __init__(self, message: str):
        self.name = 'Recorrência não encontrada'
        self.status_code = HTTPStatus.NOT_FOUND
        self.message = message
