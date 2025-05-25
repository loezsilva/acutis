import requests
import os
import logging

def send_data_to_memberkit(phone: str, full_name: str, email: str) -> None:
    
    if os.getenv("ENVIRONMENT") != "production": 
        return
    
    url_memberkit_api = os.getenv("URL_API_MEMBERKIT")
        
    data = {
        "email": email, 
        "full_name": full_name,
        "phone_local_code": phone[0:2],
        "phone_number": phone[2:],
    }
        
    response = requests.post(url_memberkit_api, json=data)
            
    if response.status_code != 201: 
        logging.error("Error ao enviar para o Memberkit")
    logging.info("Enviado para o Memberkit")
    
    return response