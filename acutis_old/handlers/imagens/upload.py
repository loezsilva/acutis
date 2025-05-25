import uuid
from flask import request
from flask_sqlalchemy import SQLAlchemy

from exceptions.error_types.http_bad_request import BadRequestError
from exceptions.errors_handler import errors_handler
from services.factories import file_service_factory


class ImageUpload:
    def __init__(self):
        self.__image = request.files["image"]
    
    def execute(self):  
        try:
            if "image" not in request.files:
                raise BadRequestError("O envio da imagem é obrigatório.")
            
            if self.__image.filename == "":
                raise BadRequestError("Nome de arquivo inválido")
            
            filename = str(uuid.uuid4())

            extension = self.__image.filename.rsplit(".", 1)[1].lower()

            allowed_extensions = {"png", "jpg", "jpeg"}
            if extension not in allowed_extensions:
                raise BadRequestError("Extensão de arquivo não permitida")
            
            filename = f"{filename}.{extension}"
            
            s3_client = file_service_factory()

            s3_client.upload_image(self.__image, filename)

            public_url = s3_client.get_public_url(filename)
            
            return {"filename": filename, "url": public_url}, 200
        
        except Exception as e:
            return errors_handler(e)