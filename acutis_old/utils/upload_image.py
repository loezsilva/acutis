import base64
import io
import os
from PIL import Image
from exceptions.exception_upload_image import UploadImageException

from services.file_service import FileService


class UploadImage:
    def __init__(self, file_service: FileService) -> None:
        self.__file_service = file_service

    def upload_image_base64(self, image_name: str, base64_image: str):
        try:
            if base64_image.startswith("data:image/jpeg"):
                image_format = "jpeg"
            elif base64_image.startswith("data:image/png"):
                image_format = "png"
            else:
                raise UploadImageException(
                    message="Formato de imagem não suportado. Somente JPEG e PNG são aceitos.",
                    status_code=400,
                    error_message="Formato inválido",
                )

            image_data = base64_image.split(",")[1]
            image_bytes = base64.b64decode(image_data)
            image = Image.open(io.BytesIO(image_bytes))

            if image.mode == "RGBA":
                image = image.convert("RGB")

            compressed_image_io = io.BytesIO()
            quality = 15 if image_format == "jpeg" else 85

            image.save(
                compressed_image_io, format=image_format.upper(), quality=quality
            )
            compressed_image_io.seek(0)

            compressed_image_filename = os.path.join("storage/images/", image_name)
            os.makedirs(os.path.dirname(compressed_image_filename), exist_ok=True)
            with open(compressed_image_filename, "wb") as f:
                f.write(compressed_image_io.read())

            self.__file_service.upload_image(compressed_image_filename, image_name)

        except Exception as err:
            raise UploadImageException(
                message=f"Ocorreu um erro ao realizar o upload da imagem -> {err}",
                status_code=500,
                error_message=str(err),
            )
