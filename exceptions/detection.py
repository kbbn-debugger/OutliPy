from base import OutliPyException
from typing import Optional, List

class DetectionException(OutliPyException):
    """
    Raised when outlier detection fails due to invalid input, computation errors,
    or misconfiguration of a detector.
    """  
    def __init__(self):
        pass

class MultivariateException(OutliPyException):
    """
    Raised when multivariate outlier detection (e.g., Mahalanobis distance) is
    used incorrectly, or when input data does not meet requirements.
    """
    pass