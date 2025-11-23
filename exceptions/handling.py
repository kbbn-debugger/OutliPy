from base import OutliPyException
from typing import Optional, List
from error_codes import ErrorCodeRegistry

ErrorCodeRegistry.register(
    "HEX000",
    "[OutliPy Handling] - {error_code}\n\n"
    "No outliers found for handling, but handling was forced\n\n"
    "Suggestion: {suggestion}"
)

ErrorCodeRegistry.register(
    "HEX001",
    "[OutliPy Handling] - {error_code}\n\n" \
    "{method} is unknown, invalid, or not allowed.\n\n"
    "These are the following allowed methods:\n{allowed_methods}\n\n"
    "Suggestion: {suggestion}"
)

ErrorCodeRegistry.register(
    "HEX002",
    "[OutliPy Handling] - {error_code}\n\n"
    "Replacement value {fill_value} is invalid or out of bounds.'n'n"
    "Suggestion: {suggestion}"
)

ErrorCodeRegistry.register(
    "HEX003",
    "[OutliPy Handling] - {error_code}\n\n"
    "Winsorization produced invalid results"
    "Suggestion: {suggestion}"
)

class HandlingException(OutliPyException):
    """
    Raised when outlier handling (removal, replacement, winsorization, etc.) fails
    due to invalid strategy, configuration, or data issues.
    """
    def __init__(self,
                 error_code: str,
                 *,
                 method: Optional[str] = None,
                 allowed_methods: Optional[List[str]] = None,
                 fill_value: Optional[float] = None
                 ):
        pass