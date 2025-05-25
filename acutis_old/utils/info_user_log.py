# Pega dados do usuário se estiver logado.

from flask_jwt_extended import current_user, get_jwt_identity
from utils.logs_access import log_access

def log_user_access(response, status_code):
    current_user_id = get_jwt_identity()   
    if current_user_id:
        current_user_info = {
            "id": current_user_id,
            "nome": current_user['nome'],
            "fk_perfil_id": current_user['fk_perfil_id']
        }
        log_access(response, current_user_info['id'], current_user_info['nome'], current_user_info['fk_perfil_id'], status_code)
