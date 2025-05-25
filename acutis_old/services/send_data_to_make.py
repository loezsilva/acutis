import requests
import os
import logging

def send_data_to_make(telefone: str, nome: str) -> None:
    
    if os.getenv("ENVIRONMENT") != "production": 
        return
        
    url_webhook_make = os.getenv("URL_API_MAKE")
        
    data = {
        "telefone": telefone,
        "nome": nome
    }
        
    response = requests.post(url_webhook_make, json=data)
    
    if response.status_code != 201: 
        logging.error("Error ao enviar para o Memberkit")
    logging.info("Enviado para o Memberkit")
    
    
    return response