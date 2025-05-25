import logging
import os
import requests
from models.schemas.users.post.create_register_in_app_acutis import CreateRegisterAppAcutis

class SendDataToAppAcutis:
    def __init__(self, data: CreateRegisterAppAcutis) -> None:
        self.__data = data
        
    def execute(self) -> None:
        try:
            
            if os.getenv("ENVIRONMENT") != "production":
                return
            
            token = os.getenv("TOKEN_REGISTER_USER_APP_ACUTIS")
            url_to_send = os.getenv("URL_TO_SEND_REGISTER_USER_APP_ACUTIS")
            
            data_to_send = CreateRegisterAppAcutis.parse_obj(self.__data)
            
            headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            }
            
            payload = [{
                "email": data_to_send.email,
                "cpf": data_to_send.cpf,
                "patent": data_to_send.patent,
                "name": data_to_send.name
            }]
            
            response = requests.post(
                url=url_to_send,
                json=payload,   
                headers=headers
            )
            
            if response.status_code != 200:
                logging.error(f"ERROR AO ENVIAR REGISTRO PARA O APP ACUTIS - {response.text} - {response.status_code}")
            
        except Exception as err: 
            logging.error(f"{str(type(err))} - {str(err)}")
            raise err