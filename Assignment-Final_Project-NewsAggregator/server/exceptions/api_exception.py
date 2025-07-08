class ApiException(Exception):
    def __init__(self, message: str, status_code=None):
        super().__init__(message)
        self.status_code = status_code
        self.error_type = self.__class__.__name__


class NetworkError(ApiException):
    def __init__(self, message: str = "Network connection failed"):
        super().__init__(message, status_code=503)


class APIKeyError(ApiException):
    def __init__(self, message: str = "Invalid or missing API key"):
        super().__init__(message, status_code=401)


class RateLimitError(ApiException):
    def __init__(self, message: str = "API rate limit exceeded"):
        super().__init__(message, status_code=429)


class InvalidResponseError(ApiException):
    def __init__(self, message: str = "Invalid API response format"):
        super().__init__(message, status_code=502)
