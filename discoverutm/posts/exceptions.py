class InvalidFilterParameterError(Exception):
    def __init__(self, message, status=400):
        super().__init__(message)
        self.error_message = message
        self.status = status


class FailedToUploadImageError(Exception):
    def __init__(self, message):
        super().__init__(message)
