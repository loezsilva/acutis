from http import HTTPStatus
import os
import boto3
from botocore.exceptions import ClientError
from werkzeug.datastructures import FileStorage
from exceptions.errors_handler import errors_handler
from services.file_service_interface import FileServiceInterface


class S3Service(FileServiceInterface):
    def __init__(self):
        self.__client = boto3.client(
            "s3",
            aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
            region_name=os.environ.get("AWS_REGION"),
        )
        self.__bucket_name = os.environ.get("AWS_BUCKET_NAME")

    def upload_image(self, file: FileStorage, filename: str) -> None:
        self.__client.upload_fileobj(file, self.__bucket_name, filename)

    def get_public_url(self, object_name: str) -> str:
        try:
            response = self.__client.generate_presigned_url(
                "get_object",
                Params={"Bucket": self.__bucket_name, "Key": object_name},
                ExpiresIn=3600,
            )

            return response
        except ClientError as e:
            return errors_handler(e)

    def get_object_by_filename(self, filename: str) -> FileStorage:
        response = self.__client.get_object(
            Bucket=self.__bucket_name, Key=filename
        )

        return response["Body"]

    def upload_fileobj(
        self, file: FileStorage, filename: str, content_type: str
    ) -> HTTPStatus.OK:
        self.__client.upload_fileobj(
            Fileobj=file,
            Bucket=self.__bucket_name,
            Key=filename,
            ExtraArgs={"ContentType": content_type},
        )

        return HTTPStatus.OK

    def delete_object(self, filename: str) -> None:
        self.__client.delete_object(Bucket=self.__bucket_name, Key=filename)
