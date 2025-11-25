from base import OutliPyException
from typing import Optional, List, Union
from error_code_registry import ErrorCodeRegistry


# CON001 – Missing required configuration parameter

ErrorCodeRegistry.register(
    "CON001",
    "[{method}] - {error_code}\n\n"
    "Missing required configuration parameter - {parameter}\n\n"
    "Suggestion: {suggestion}"
)

# CON002 – Invalid parameter value (e.g., threshold ≤ 0)

ErrorCodeRegistry.register(
    "CON002",
    "[{method}] - {error_code}\n\n"
    "Invalid parameter value: {parameter_context}\n\n"
    "Suggestion: {suggestion}"
)

# CON003 – Unsupported detection method

ErrorCodeRegistry.register(
    "CON003",
    "[{method}] - {error_code}\n\n"
    "The current {typed_method} is currently not unsupported\n\n"
    "Suggestion: {suggestion}"
)

# CON004 – Parameter type mismatch

ErrorCodeRegistry.register(
    "CON004",
    "[{method}] - {error_code}\n\n"
    "Inconsistent parameter type passed on {parameter}\n\n"
    "Suggestion: {suggestion}"
)

# CON005 – Too few rows to use chosen method

ErrorCodeRegistry.register(
    "CON005",
    "[{method}] - {error_code}\n\n"
    "Too few rows passed\n\n"
    "Suggestion: {suggestion}"
)


class ConfigurationException(OutliPyException):
    """
    Raised when configuration parameters are invalid, missing, or inconsistent.
    """
    def __init__(
            self,
            *,
            error_code: str,
            method: str,
            parameter: Optional[Union[str, List[str]]] = None,
            parameter_context: Optional[Union[str, List[str]]] = None,
            typed_method: Optional[str] = None,
            suggestion: Optional[str] = None
    ):
        
        context_data = {
            "parameter": parameter,
            "typed_method": typed_method,
            "parameter_context": parameter_context
        }
        
        super().__init__(
            error_code = error_code,
            method = method,
            context = context_data,
            suggestion = suggestion or "Please check your parameters or DataFrame."
        )