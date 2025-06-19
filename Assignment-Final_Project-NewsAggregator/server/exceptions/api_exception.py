class ApiException(Exception):
    def __init__(self, message, status_code=None):
        super().__init__(message)
        self.status_code = status_code


class NetworkError(ApiException):
    def __init__(self, message="Network connection failed"):
        super().__init__(message)


class APIKeyError(ApiException):
    def __init__(self, message="Invalid or missing API key"):
        super().__init__(message)
