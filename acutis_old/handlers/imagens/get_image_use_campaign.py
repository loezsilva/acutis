import base64
from flask import jsonify, request
from flask_jwt_extended import current_user
from exceptions.error_types.http_not_found import NotFoundError
from models.foto_campanha import FotoCampanha
from services.factories import file_service_factory

class GetImageUserCampaign:
    def __init__(self):
        self.__http_args = request.args
        self.__campanha_id = self.__http_args.get("campaign_id")
        self.__user_id = current_user["id"]    

    def execute(self):
        foto_campanha = self.__get_foto_campaign()
        return self.__get_image_bucket(foto_campanha)
        
    def __get_foto_campaign(self):
        
        if self.__campanha_id is not None:
            
            foto_campanha: FotoCampanha = FotoCampanha.query.filter_by(
                fk_usuario_id=self.__user_id, fk_campanha_id=self.__campanha_id
            ).first()
            
            if not foto_campanha:
                raise NotFoundError("Registro de foto do usuário não encontrada.")    
                
            return foto_campanha.foto
        
    def __get_image_bucket(self, filename):
        s3_client = file_service_factory()
        try:
            response = s3_client.get_object_by_filename(filename)
            image_data = response.read()
            image_url = base64.b64encode(image_data).decode("utf-8")
            return jsonify(f"data:image/png;base64,{image_url}")
        except Exception:
            return {"erros": "Imagem não encontrada"}, 200