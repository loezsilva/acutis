from acutis_api.infrastructure.services.amazon_s3 import S3Service
from acutis_api.infrastructure.services.strategy.file_service import (
    FileService,
)


def file_service_factory() -> FileService:
    return FileService(S3Service())
