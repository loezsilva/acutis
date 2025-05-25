class SendGridException(Exception):
    def __init__(self, message: str, status_code) -> None:
        super().__init__(message)
        self.name = 'SendGridException'
        self.status_code = status_code
        self.error_message = message
