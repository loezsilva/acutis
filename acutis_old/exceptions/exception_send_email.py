class SendEmailException(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.name = "SendEmailException"
        self.status_code = 401
