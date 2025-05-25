from services.factories import file_service_factory

class GetImage:
    def __init__(self, filename: str):
        self.__filename = filename
        
    def execute(self):
        s3_client = file_service_factory()
         
        try:
            imagem_url = s3_client.get_public_url(self.__filename)
        except Exception:
            return {"erros": "Imagem não encontrada"}
        
        return imagem_url