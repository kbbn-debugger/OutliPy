class OutliPyException(Exception):
    """
    Base exception for all OutliPy errors.
    """
    pass


class DetectionException(OutliPyException):
    """
    Raised when outlier detection fails due to invalid input, computation errors,
    or misconfiguration of a detector.
    """
    pass


class HandlingException(OutliPyException):
    """
    Raised when outlier handling (removal, replacement, winsorization, etc.) fails
    due to invalid strategy, configuration, or data issues.
    """
    pass


class InvalidColumnException(OutliPyException):
    """
    Raised when columns specified by the user do not exist in the DataFrame,
    or if there are no valid numeric columns for detection/handling.
    """
    pass


class ConfigurationException(OutliPyException):
    """
    Raised when configuration parameters (like thresholds, strategy names, or
    column selections) are invalid, missing, or inconsistent.
    """
    pass


class MultivariateException(OutliPyException):
    """
    Raised when multivariate outlier detection (e.g., Mahalanobis distance) is
    used incorrectly, or when input data does not meet requirements.
    """
    pass
