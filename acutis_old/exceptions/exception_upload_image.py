class UploadImageException(Exception):
    def __init__(self, message: str, status_code: int, error_message: str) -> None:
        super().__init__(message)
        self.name = "UploadImageException"
        self.status_code = status_code
        self.msg = message
        self.error_message = error_message
