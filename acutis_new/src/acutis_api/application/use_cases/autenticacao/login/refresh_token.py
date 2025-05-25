from flask_jwt_extended import create_access_token, get_jwt_identity

from acutis_api.communication.responses.autenticacao import (
    RefreshTokenResponse,
)


class RefreshTokenUseCase:
    @staticmethod
    def execute():
        identity = get_jwt_identity()

        response = RefreshTokenResponse(
            access_token=create_access_token(identity=identity)
        ).model_dump()

        return response
