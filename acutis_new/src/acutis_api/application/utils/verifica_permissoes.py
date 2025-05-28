from functools import wraps
from flask_jwt_extended import current_user
from acutis_api.exception.errors.unauthorized import HttpUnauthorizedError
from acutis_api.exception.errors_handler import errors_handler

def permissao_requerida(menu_name, action):
    def verify(f):
        @wraps(f)
        def decorate_verify(*args, **kwargs):
            try:
                if (
                    not current_user
                    or current_user.get("permissoes", {}).get(menu_name, {}).get(action, 0)
                    != 1
                ):

                    raise HttpUnauthorizedError("Você não tem permissão para realizar esta ação.")
                    
                return f(*args, **kwargs)
            except Exception as e:
                response_error = errors_handler(e)
                return response_error
            
        return decorate_verify

    return verify