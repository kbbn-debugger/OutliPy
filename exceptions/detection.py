from base import OutliPyException
from typing import Optional
from error_code_registry import ErrorCodeRegistry


# ---------------------------------------------------------------
#               Detection Exceptions Error Codes
# ---------------------------------------------------------------

# DET001 - No data left after preprocessing.

ErrorCodeRegistry.register(
    "DET001",
    "[{method}] - {error_code}\n\n"
    "No data left after preprocessing\n"
    "{specific_message}\n\n"
    "Suggestion: {suggestion}"
)

# DET002 - No numeric data available for computation.

ErrorCodeRegistry.register(
    "DET002",
    "[{method}] - {error_code}\n\n"
    "No numeric data available for computation\n\n"
    "Suggestion: {suggestion}"
)

# DET003 - Zero Variance.

ErrorCodeRegistry.register(
    "DET003",
    "[{method}] - {error_code}\n\n"
    "Zero variance\n\n"
    "Suggestion: {suggestion}"
)

# DET004 - Zero IQR.

ErrorCodeRegistry.register(
    "DET004",
    "[{method}] - {error_code}\n\n"
    "Zero Inter-Quartile Range - IQR detector cannot compute bounds.\n\n"
    "Suggestion: {suggestion}"
)

# DET005 - Zero MAD.

ErrorCodeRegistry.register(
    "DET005",
    "[{method}] - {error_code}\n\n"
    "Zero Modified Absolute Deviation - Modified Z-score fails.\n\n"
    "Suggestion: {suggestion}"
)

# DET006 - Score computation resulted in NaN or inf.

ErrorCodeRegistry.register(
    "DET006",
    "[{method}] - {error_code}\n\n"
    "Normalization step failed\n\n"
    "Suggestion: {suggestion}"
)

# DET007 - Detection flagged zero rows unexpectedly.

ErrorCodeRegistry.register(
    "DET007",
    "[{method}] - {error_code}\n\n"
    "Detection flagged zero rows unexpectedly.\n\n"
    "Suggestion: {suggestion}"
)

# DET008 - Detection flagged all rows.

ErrorCodeRegistry.register(
    "DET008",
    "[{method}] - {error_code}\n\n"
    "Detection flagged all rows.\n\n"
    "Suggestion: {suggestion}"
)

# DET009 - Custom detector returned wrong shape or wrong dtype.

ErrorCodeRegistry.register(
    "DET009",
    "[{method}] - {error_code}\n\n"
    "Custom detector returned wrong shape or wrong dtype\n\n"
    "Suggestion: {suggestion}"
)

# ---------------------------------------------------------------
#               Multivariate Exceptions Error Codes
# ---------------------------------------------------------------

# MVT001 - Singular covariance matrix.

ErrorCodeRegistry.register(
    "MVT001",
    "[{method}] - {error_code}\n\n"
    "Singular Covariance Matrix - Cannot Invert\n\n"
    "Suggestion: {suggestion}"
)

# MVT002 - Too few samples for multivariate method.

ErrorCodeRegistry.register(
    "MVT002",
    "[{method}] - {error_code}\n\n"
    "Too few samples for multivarite method.\n\n"
    "Suggestion: {suggestion}"
)

# MVT003 - Non-Positive-Definite covariance matrix.

ErrorCodeRegistry.register(
    "MVT003",
    "[{method}] - {error_code}\n\n"
    "Non-Positive-Definite covariance matrix.\n\n"
    "Suggestion: {suggestion}"
)

# MVT004 - Mahalonobis distance computation failed.

ErrorCodeRegistry.register(
    "MVT004",
    "[{method}] - {error_code}\n\n"
    "Mahalonobis distance computation failed.\n\n"
    "Suggestion: {suggestion}"
)

# MVT005 - Corrupted or ill-conditioned matrix.

ErrorCodeRegistry.register(
    "MVT005",
    "[{method}] - {error_code}\n\n"
    "Corrupted matrix.\n\n"
    "Suggestion: {suggestion}"
)


# ----------------------------------------------------------------
#                        Detection Exception 
# ----------------------------------------------------------------



class DetectionException(OutliPyException):
    """
    Raised when outlier detection fails due to computation errors.
    """  
    def __init__(
            self,
            *,
            error_code: str,
            method: str,
            specific_message: Optional[str] = None,
            suggestion: Optional[str] = None
    ):
        
        context_data = {
            "specific_message": specific_message or ""
        }

        super().__init__(
            error_code = error_code,
            method = method,
            context = context_data,
            suggestion = suggestion or "Please check your DataFrame."
        )




# ----------------------------------------------------------------
#                       Multivariate Exception
# ----------------------------------------------------------------

class MultivariateException(OutliPyException): 
    """
    Raised when multivariate outlier detection (e.g., Mahalanobis distance) is
    used incorrectly, or when input data does not meet requirements.
    """
    def __init__(
            self,
            *,
            error_code: str,
            method: str,
            suggestion: Optional[str] = None
    ):
        
        context_data = {

        }

        super().__init__(
            error_code = error_code,
            method = method,
            suggestion = suggestion or "Please check your DataFrame"
        )