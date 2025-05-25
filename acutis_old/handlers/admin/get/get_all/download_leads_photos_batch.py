from concurrent.futures import ThreadPoolExecutor, as_completed
from io import BytesIO
import zipfile
from flask_jwt_extended import current_user
from flask_sqlalchemy import SQLAlchemy

from models.foto_leads import FotoLeads
from models.users_imports import UsersImports
from services.file_service import FileService
from utils.functions import get_current_time


class DownloadLeadsPhotosBatch:
    def __init__(self, database: SQLAlchemy, file_service: FileService) -> None:
        self.__database = database
        self.__file_service = file_service

    def execute(self):
        zip_path = BytesIO()

        query_files = (
            self.__database.session.query(
                FotoLeads.foto,
                UsersImports.nome,
                UsersImports.id,
                FotoLeads.data_download,
                FotoLeads.user_download,
                UsersImports.intencao,
            )
            .join(UsersImports, FotoLeads.fk_user_import_id == UsersImports.id)
            .filter(FotoLeads.data_download == None)
        )

        quant_fotos = query_files.count()
        files = query_files.all()

        txt_content = "\n".join(f"{file[1]}: \n {file[5]} \n" for file in files)

        def download_and_add_to_zip(file_tuple):
            file_name = file_tuple[0]
            user_name = file_tuple[1]
            user_id = file_tuple[2]

            zip_file_name = f"{user_name}_{user_id}_{file_name}"
            response = self.__file_service.get_object_by_filename(file_name)

            if response is not None:
                return zip_file_name, response.read()
            return zip_file_name, None

        with zipfile.ZipFile(zip_path, "w") as zip_file:
            zip_file.writestr("intencoes.txt", txt_content)

            with ThreadPoolExecutor(max_workers=10) as executor:
                future_to_file = {
                    executor.submit(download_and_add_to_zip, file_tuple): file_tuple
                    for file_tuple in files
                }
                for future in as_completed(future_to_file):
                    zip_file_name, content = future.result()
                    if content:
                        zip_file.writestr(zip_file_name, content)

        zip_path.seek(0)

        zip_file_name = f'fotos_leads_{get_current_time().strftime("%Y%m%d%H%M%S")}.zip'

        code = self.__file_service.upload_fileobj(
            filename=zip_file_name,
            file=zip_path,
            content_type="application/zip",
        )

        if code == 200:
            zip_download = self.__file_service.get_public_url(zip_file_name)

            ids_leads = [file[2] for file in files]
            self.__database.session.query(FotoLeads).filter(
                FotoLeads.fk_user_import_id.in_(ids_leads)
            ).update(
                {
                    "user_download": current_user["id"],
                    "data_download": get_current_time(),
                },
                synchronize_session=False,
            )
            try:
                self.__database.session.commit()
            except Exception as exception:
                self.__database.session.rollback()
                raise exception

        response = {
            "msg": f"Download de {quant_fotos} fotos realizado com sucesso!",
            "zip_download": zip_download,
        }

        return response, 200
