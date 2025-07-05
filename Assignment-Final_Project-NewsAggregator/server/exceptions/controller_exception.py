class ControllerException(Exception):
    def __init__(self, message: str, status_code=None):
        super().__init__(message)
        self.status_code = status_code
        self.error_type = self.__class__.__name__


class UnauthorizedException(ControllerException):
    def __init__(self, message: str = "Unauthorized access"):
        super().__init__(message, status_code=401)


class ForbiddenException(ControllerException):
    def __init__(self, message: str = "Forbidden"):
        super().__init__(message, status_code=403)


class BadRequestException(ControllerException):
    def __init__(self, message: str = "Bad request"):
        super().__init__(message, status_code=400)


class NotFoundException(ControllerException):
    def __init__(self, message: str = "Resource not found"):
        super().__init__(message, status_code=404)


class InternalServerErrorException(ControllerException):
    def __init__(self, message: str = "Internal server error"):
        super().__init__(message, status_code=500)
