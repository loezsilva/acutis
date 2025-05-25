# from concurrent.futures import ThreadPoolExecutor, as_completed
# from fileinput import filename
# from io import BytesIO
# from os import error
# from flask_sqlalchemy import SQLAlchemy
# import zipfile
# from exceptions.error_types.http_not_found import NotFoundError
# from exceptions.errors_handler import errors_handler
# from models.generais import Generais
# from services.s3_service import S3Service
# from utils.functions import get_current_time

# class ExportFotosGenerais:
#     def __init__(self, conn: SQLAlchemy, s3_client: S3Service):
#         self.__conn = conn
#         self.__s3_client = s3_client()     
    
#     def execute(self):
#         fotos, quantidade_fotos = self.__get_fotos_generais()
#         zip_download = self.__generate_zip_files(fotos)
#         return self.__format_response(zip_download, quantidade_fotos)
    
#     def __get_fotos_generais(self):
#         query_files = (
#             self.__conn.session.query(Generais.print_grupo)
#             .filter(Generais.deleted_at == None, Generais.print_grupo != None)
#             .all()
#         )
        
#         if query_files is None:
#             raise NotFoundError("Nenhuma foto disponível para exportar.")
        
#         files = [file_tuple for file_tuple in query_files]
        
#         quant_fotos = len(files)
#         return files, quant_fotos
    
    
#     def __generate_zip_files(self, files: list):
#         zip_file_name = f'fotos_generais_{get_current_time().strftime("%Y%m%d%H%M%S")}.zip'
#         zip_path = BytesIO()
        
#         with zipfile.ZipFile(zip_path, "w") as zip_file:

#             def download_and_add_to_zip(file_name):
#                 try:
#                     response = self.__s3_client.get_object_by_filename(file_name)
#                     if response is not None:
#                         return file_name, response.read()
#                 except Exception as e:
#                     errors_handler(e)
#                 return file_name, None

#             with ThreadPoolExecutor(max_workers=10) as executor:
#                 future_to_file = {
#                     executor.submit(download_and_add_to_zip, file_name[0]): file_name[0]
#                     for file_name in files
#                 }
#                 for future in as_completed(future_to_file):
#                     file_name, content = future.result()
#                     if content:
#                         zip_file.writestr(file_name, content)

#         zip_path.seek(0)
#         self.__s3_client.upload_fileobj(
#             file=zip_path,
#             filename=zip_file_name,
#             content_type="application/zip",
#         )
#         zip_download = self.__s3_client.get_public_url(zip_file_name)
            
#         return zip_download
        
#     def __format_response(self, zip_download: tuple, quant_fotos: int) -> tuple:
#         response = {
#             "msg": f"Download de {quant_fotos} fotos realizado com sucesso!",
#             "zip_download": zip_download,
#         }
        
#         return response, 200