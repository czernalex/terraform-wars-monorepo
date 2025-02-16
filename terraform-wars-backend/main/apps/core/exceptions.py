from typing import Any, Dict, List


class NotFoundError(Exception):
    """Exception raised when a resource is not found."""

    def __init__(self, message: str):
        super().__init__(message)


class ValidationError(Exception):
    """Exception raised when a request data does not validate."""

    def __init__(self, errors: List[Dict[str, Any]]):
        self.errors = errors
        super().__init__(self.errors)
