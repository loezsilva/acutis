import os
import uuid
from flask import request

from exceptions.error_types.http_bad_request import BadRequestError
from services.factories import file_service_factory


class UpdateImagem:
    def __init__(self, filename: str):
        self.__image = request.files["image"]
        self.__filename = filename
    
    def execute(self):
        self.__verify_image() 
        
        extension = self.__image.filename.rsplit(".", 1)[1].lower()

        allowed_extensions = {"png", "jpg", "jpeg"}
        if extension not in allowed_extensions:
            raise BadRequestError("Extensão de arquivo não permitida")

        s3_client = file_service_factory()

        s3_client.upload_image(self.__image, self.__filename)

        public_url = s3_client.get_public_url(self.__filename)
        return {"filename": self.__filename, "url": public_url}, 201
            
    def __verify_image(self):
        if "image" not in request.files:
            return {"error": "O envio da imagem é obrigatório."}, 400

        if self.__image.filename == "":
            raise BadRequestError("Nome de arquivo inválido")        
        