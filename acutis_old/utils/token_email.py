from itsdangerous import BadSignature, URLSafeTimedSerializer, SignatureExpired

from config import SECRET_KEY
from exceptions.error_types.http_unauthorized import UnauthorizedError


def generate_token(obj, salt) -> str:
    serializer = URLSafeTimedSerializer(SECRET_KEY)

    token = serializer.dumps(obj, salt=salt)

    return token


def verify_token(token, salt, max_age=24 * 60 * 60):
    try:
        serializer = URLSafeTimedSerializer(SECRET_KEY)

        obj = serializer.loads(token, salt=salt, max_age=max_age)

        return obj
    except SignatureExpired:
        raise UnauthorizedError("Token expirado.")
    except BadSignature:
        raise UnauthorizedError("Token inválido.")
