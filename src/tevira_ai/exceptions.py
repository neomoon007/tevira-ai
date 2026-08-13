class DomainException(Exception):
    def __init__(self, message: str, error_code: str, status_code: int):
        super().__init__(message)
        self.message = message
        self.error_code = error_code
        self.status_code = status_code


class ResourceNotFoundError(DomainException):
    def __init__(self, resource_type: str, resource_id: str):
        super().__init__(
            message=f"{resource_type} with ID {resource_id} was not found.",
            error_code="RESOURCE_NOT_FOUND",
            status_code=404,
        )


class ResourceInUseError(DomainException):
    def __init__(self, resource_type: str, resource_id: str):
        super().__init__(
            message=f"{resource_type} with ID {resource_id} is in use by another resource.",
            error_code="RESOURCE_IN_USE",
            status_code=409,
        )
