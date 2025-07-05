class RepositoryException(Exception):
    """Base exception for repository errors."""
    def __init__(self, message: str):
        super().__init__(message)
        self.error_type = self.__class__.__name__


class NotFoundException(RepositoryException):
    """Raised when an entity is not found in the repository."""
    def __init__(self, message: str = "Resource not found"):
        super().__init__(message)


class DuplicateEntityException(RepositoryException):
    """Raised when attempting to create a duplicate entity."""
    def __init__(self, message: str = "Entity already exists"):
        super().__init__(message)


class DisabledEntityException(RepositoryException):
    """Raised when an entity is disabled by admin."""
    def __init__(self, message: str = "Entity disabled by admin"):
        super().__init__(message)


class PermissionDeniedException(RepositoryException):
    """Raised when a user does not have permission for an action."""
    def __init__(self, message: str = "Permission denied"):
        super().__init__(message)


class DatabaseConnectionException(RepositoryException):
    """Raised when a database connection fails."""
    def __init__(self, message: str = "Database connection failed"):
        super().__init__(message)


class APINameNotFoundException(RepositoryException):
    """Raised when an API name is not found in the database."""
    def __init__(self, message: str = "API name not found."):
        super().__init__(message)
