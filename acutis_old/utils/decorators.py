from flask import request
from utils.send_email import send_email


def limit_ip_address_maxpago(func):
    def wrapper(*args, **kwargs):
        client_ip = request.remote_addr
        valid_ips = ['52.207.83.230', '54.237.160.163', '127.0.0.1']
        if client_ip not in valid_ips:
            send_email('Webhook MaxPago Recorrência: Permissão Negada',
                       'neville.guimaraes@headers.com.br',
                       f"<html>Tentativa de acesso do ip: {client_ip} mas o ip não consta na lista de ips válidos: {valid_ips}</html>")
            return {"error": f"Permissão negada."}, 403
        return func(*args, **kwargs)
    wrapper.__name__ = func.__name__
    return wrapper
