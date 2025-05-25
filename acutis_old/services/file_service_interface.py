from werkzeug.datastructures import FileStorage

from abc import ABC, abstractmethod


class FileServiceInterface(ABC):

    @abstractmethod
    def upload_image(
        self,
        file: FileStorage,
        filename: str | None = None,
        validate_file: bool = True,
    ):
        pass

    @abstractmethod
    def get_public_url(self, object_name: str) -> tuple:
        pass

    @abstractmethod
    def get_object_by_filename(self, filename: str) -> FileStorage:
        pass

    @abstractmethod
    def upload_fileobj(
        self, file: FileStorage, filename: str, content_type: str
    ) -> int:
        pass

    @abstractmethod
    def delete_object(self, filename: str) -> None:
        pass
