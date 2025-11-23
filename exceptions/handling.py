from base import OutliPyException
from typing import Optional, List
from error_codes import ErrorCodeRegistry


class HandlingException(OutliPyException):
    """
    Raised when outlier handling (removal, replacement, winsorization, etc.) fails
    due to invalid strategy, configuration, or data issues.
    """
    default_error_code = "HE000"
    pass