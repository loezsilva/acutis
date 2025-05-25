from datetime import datetime
from flask import current_app, request
import json

import pytz


def log_access(response, user_id, username, cargo, sc=None):
    app = current_app._get_current_object()
    timestamp = datetime.now(pytz.timezone("America/Fortaleza")).strftime(
        "%Y-%m-%d %H:%M:%S"
    )
    route = request.path
    method = request.method
    ip_address = request.headers.get("X-Forwarded-For", request.remote_addr)
    request_data = request.get_json() if request.is_json else {}
    response_data = response
    status_code = sc

    if sc is None and isinstance(response, tuple) and len(response) > 1:
        status_code = response[1]

    log_entry = {
        "status_code": status_code,
        "timestamp": timestamp,
        "username": username,
        "cargo": cargo,
        "user_id": user_id,
        "route": route,
        "method": method,
        "request_data": request_data,
        "response_data": response_data,
        "ip_address": ip_address,
    }

    with app.app_context():
        with open("access_log.txt", "a") as log_file:
            log_file.write(json.dumps(log_entry, indent=None) + "\n")

    return response
