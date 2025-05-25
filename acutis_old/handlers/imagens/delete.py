from exceptions.error_types.http_not_found import NotFoundError
from services.factories import file_service_factory

class DeleteImage:
    def __init__(self, filename: str):
        self.__filename = filename
        
    def execute(self):
        s3_client = file_service_factory()
        
        if s3_client.get_object_by_filename(self.__filename):
            s3_client.delete_object(self.__filename)
        else:
            raise NotFoundError("Imagem não localizada")
        
        return {"msg": "Imagem deletada com sucesso."}, 200