from services.file_service import FileService
from services.s3_service import S3Service


def file_service_factory() -> FileService:
    return FileService(S3Service())
