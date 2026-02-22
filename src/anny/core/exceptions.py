class AnnyError(Exception):
    """Base exception for all Anny errors."""

    def __init__(self, message: str = "An error occurred"):
        self.message = message
        super().__init__(self.message)


class AuthError(AnnyError):
    """Raised when authentication fails (missing key, invalid credentials)."""

    def __init__(self, message: str = "Authentication failed"):
        super().__init__(message)


class ValidationError(AnnyError):
    """Raised when user input fails validation (bad dates, empty metrics, etc.)."""

    def __init__(self, message: str = "Invalid input"):
        super().__init__(message)


class APIError(AnnyError):
    """Raised when a Google API call fails."""

    def __init__(self, message: str = "API call failed", service: str = ""):
        self.service = service
        super().__init__(message)
