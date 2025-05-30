from typing import Dict, Any


class PaymentCreditCardUseCase:

    __STATUS_MESSAGES = {
        'approved': {
            'accredited': "Pronto, seu pagamento foi aprovado!"
        },
        'in_process': {
            'pending_contingency': "Estamos processando o pagamento. Não se preocupe, em menos de 2 dias úteis informaremos por e-mail se foi creditado.",
            'pending_review_manual': "Estamos processando seu pagamento. Não se preocupe, em menos de 2 dias úteis informaremos por e-mail se foi creditado ou se necessitamos de mais informação."
        },
        'rejected': {
            'cc_rejected_bad_filled_card_number': "Revise o número do cartão.",
            'cc_rejected_bad_filled_date': 'Revise a data de vencimento do cartão.',
            'cc_rejected_bad_filled_expiration_date': "Revise a data de vencimento do cartão.",
            'cc_rejected_bad_filled_other': "Revise os dados do cartão.",
            'cc_rejected_bad_filled_security_code': "Revise o código de segurança do cartão.",
            'cc_rejected_blacklist': "Não pudemos processar seu pagamento.",
            'cc_rejected_call_for_authorize': "Você deve autorizar ao {payment_method_id} o pagamento do valor ao Mercado Pago",
            'cc_rejected_card_disabled': "Ligue para o {payment_method_id} para ativar seu cartão. O telefone está no verso do seu cartão.",
            'cc_rejected_card_error': "Não conseguimos processar seu pagamento.",
            'cc_rejected_duplicated_payment': "Você já efetuou um pagamento com esse valor. Caso precise pagar novamente, utilize outro cartão ou outra forma de pagamento.",
            'cc_rejected_high_risk': "Escolha outra forma de pagamento. Recomendamos meios de pagamento em dinheiro.",
            'cc_rejected_insufficient_amount': "O cartão possui saldo insuficiente.",
            'cc_rejected_invalid_installments': "{payment_method_id} não processa pagamentos em {installments} parcelas.",
            'cc_rejected_max_attempts': "Você atingiu o limite de tentativas permitido. Escolha outro cartão ou outra forma de pagamento.",
            'cc_rejected_other_reason': "{payment_method_id} não processa o pagamento.",
            'cc_rejected_card_type_not_allowed': "O pagamento foi rejeitado porque o usuário não tem a função crédito habilitada em seu cartão multiplo (débito e crédito)."
        }
    }

    def format_response(self, response: Dict[str, Any]) -> Dict[str, str]:
        status = response['status']
        status_detail = response['status_detail']
        message = self.__STATUS_MESSAGES.get(status, {}).get(status_detail, '')
        return {'status': status, 'message': message.format(**response)}
