from abc import ABC, abstractmethod
from enum import Enum

from httpx import Response


class AssuntosEmailEnum(str, Enum):
    verificacao = 'Instituto HeSed - Verificação de Email'
    membro_oficial = 'Instituto HeSed - Membro Oficial'
    agradecimento_doacao = 'Instituto HeSed - Agradecemos Sua Doação'
    recuperar_senha = 'Instituto HeSed - Confirmação de redefinição de senha'


class EnviarNotificacaoInterface(ABC):
    @abstractmethod
    def enviar_email(
        self, destinatario: str, assunto: str, conteudo: str
    ) -> Response: ...
