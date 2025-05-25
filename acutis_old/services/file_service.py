from typing import Optional
import uuid
from exceptions.error_types.http_bad_request import BadRequestError
from services.file_service_interface import FileServiceInterface
from werkzeug.datastructures import FileStorage


class FileService:
    def __init__(self, file_service: FileServiceInterface):
        self.__service = file_service

    def upload_image(
        self,
        file: FileStorage,
        filename: Optional[str] = None,
        validate_file: bool = True,
    ):
        if filename is None:
            extension = file.filename.rsplit(".", 1)[1].lower()
            if validate_file:
                if file.filename == "":
                    raise BadRequestError("Nome do arquivo inválido.")

                allowed_extensions = {"png", "jpg", "jpeg", ".xlsx"}
                if extension not in allowed_extensions:
                    raise BadRequestError("Extensão do arquivo não permitida.")

            filename = f"{str(uuid.uuid4())}.{extension}"

        self.__service.upload_image(file, filename)

        return filename

    def get_public_url(self, object_name: str):
        return self.__service.get_public_url(object_name)

    def get_object_by_filename(self, filename: str):
        return self.__service.get_object_by_filename(filename)

    def upload_fileobj(
        self, file: FileStorage, filename: str, content_type: str
    ):
        return self.__service.upload_fileobj(file, filename, content_type)

    def delete_object(self, filename: str):
        return self.__service.delete_object(filename)
