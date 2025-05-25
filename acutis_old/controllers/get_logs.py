from flask import Blueprint
from flask_jwt_extended import jwt_required
from exceptions import errors_handler
from handlers.logs.get_logs import LogsGetAll
from utils.response import response_handler
from utils.verify_permission import permission_required

log_controller = Blueprint("log_controller", __name__, url_prefix="/logs")


@log_controller.route("", methods=["GET"])
@jwt_required()
@permission_required("logs", "acessar")
def get_logs():
    """Retorna listagem de logs"""
    try:
        get_logs = LogsGetAll()
        response = response_handler(get_logs.execute())
        return response
    except Exception as err:
        response_error = errors_handler(err)
        return response_error
