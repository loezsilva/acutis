from functools import wraps
from flask import jsonify
from flask_jwt_extended import current_user
from utils.logs_access import log_access
from exceptions.error_types.http_unauthorized import UnauthorizedError
from exceptions.errors_handler import errors_handler

def permission_required(menu_name, action):
    def verify(f):
        @wraps(f)
        def decorate_verify(*args, **kwargs):
            try:
                if (
                    not current_user
                    or current_user.get("permissoes", {}).get(menu_name, {}).get(action, 0)
                    != 1
                ):

                    raise UnauthorizedError("Você não tem permissão para realizar esta ação.")
                    
                return f(*args, **kwargs)
            except Exception as e:
                response_error = errors_handler(e, save_logs=True)
                return response_error
            
        return decorate_verify

    return verify
