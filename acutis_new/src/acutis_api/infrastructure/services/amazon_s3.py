from types import NoneType

import boto3
from werkzeug.datastructures import FileStorage

from acutis_api.domain.services.file_service import FileServiceInterface
from acutis_api.infrastructure.settings import settings


class S3Service(FileServiceInterface):
    def __init__(self):
        self._client = boto3.client(
            's3',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_REGION,
        )
        self._bucket_name = settings.AWS_BUCKET_NAME

    def buscar_url_arquivo(self, nome_arquivo: str) -> str:
        response = self._client.generate_presigned_url(
            'get_object',
            Params={'Bucket': self._bucket_name, 'Key': nome_arquivo},
            ExpiresIn=3600,
        )

        return response

    def salvar_arquivo(
        self,
        arquivo: FileStorage,
        nome_arquivo: str,
        extra_args: dict | None = None,
    ):
        if not isinstance(extra_args, (dict, NoneType)):
            raise ValueError('O argumento "extra_args" deve ser do tipo DICT.')

        self._client.upload_fileobj(
            Fileobj=arquivo,
            Key=nome_arquivo,
            Bucket=self._bucket_name,
            ExtraArgs=extra_args,
        )
