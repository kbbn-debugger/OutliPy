from base import OutliPyException
from typing import Optional, List
from exceptions.error_code_registry import ErrorCodeRegistry




# ----------------------------------------------------------------
#                Invalid Column Exception Error Codes
# ----------------------------------------------------------------

# ICE000 - Empty list of columns.

ErrorCodeRegistry.register(
    "ICE000",
    "[{method}] - {error_code}\n\n"
    "Empty list of columns.\n\n"
    "Suggestion: {suggestion}"
)

# ICE001 - Missing columns.

ErrorCodeRegistry.register(
    "ICE001",
    "[{method}] - {error_code}\n\n"
    "The following columns are missing:\n{missing}\n\n"
    "Suggestion: {suggestion}"
)

# ICE002 - No numeric columns for detection.

ErrorCodeRegistry.register(
    "ICE002",
    "[{method}] - {error_code}\n\n"
    "No numeric columns found for detection\n\n"
    "Suggestion: {suggestion}"
)


# ICE003 - Invalid or non-numeric columns.

ErrorCodeRegistry.register(
    "ICE003",
    "[{method}] - {error_code}\n\n"
    "The following columns are invalid or non-numeric:\n{invalid}\n\n"\
    "Suggestion: {suggestion}"
)

# ICE004 - Invalid and missing columns.

ErrorCodeRegistry.register(
    "ICE004",
    "[{method}] - {error_code}\n\n"\
    "The following columns are invalid and missing.\nInvalid: {invalid}\nMissing: {missing}\n\n"\
    "Suggestion: {suggestion}"
)

# ICE005 - Duplicated columns

ErrorCodeRegistry.register(
    "ICE005",
    "[{method}] - {error_code}\n\n"\
    "The following columns are duplicated:\n{duplicated}\n\n"
    "Suggestion: {suggestion}"
)

# ICE006 - Column contains NaN

ErrorCodeRegistry.register(
    "ICE006",
    "[{method}] - {error_code}\n\n"
    "The following columns contains NaN or an empty column:\n{nan_cols}\n\n"
    "Suggestion: {suggestion}"
)

# ICE007 - Empty DataFrame.

ErrorCodeRegistry.register(
    "ICE007",
    "[{method}] - {error_code}\n\n"
    "The DataFrame is empty\n\n"
    "Suggestion: {suggestion}"
)




# ----------------------------------------------------------------
#                     Invalid Column Exception
# ----------------------------------------------------------------

class InvalidColumnException(OutliPyException):
    """
    Raised when columns specified by the user do not exist in the DataFrame,
    or if there are no valid numeric columns for detection/handling.
    """
    def __init__(self, *,
                 method: str,
                 error_code: Optional[str] = None,
                 invalid: Optional[List[str]] = None, 
                 missing: Optional[List[str]] = None,
                 duplicated: Optional[List[str]] = None,
                 nan_cols: Optional[List[str]] = None,
                 suggestion: Optional[str] = None,
                 no_numeric: bool = False):

        # Inputs
        invalid = invalid or []
        missing = missing or []
        nan_cols = nan_cols or []
        duplicated = duplicated or []

        # Final Code
        code = error_code or ""

        # The logic determining the error code.
        if error_code is None:
            # Structural Errors
            if duplicated:
                code = "ICE005"
                suggestion = suggestion or "Remove the duplicate column from the DataFrame"
            elif no_numeric:
                code = "ICE002"
                suggestion = suggestion or "Ensure data has numeric columns."
            # Mixed errors
            elif (invalid and missing):
                code = "ICE004"
                suggestion = suggestion or "Check column names."
            # Specific Errors
            elif invalid:
                code = "ICE003"
                suggestion = suggestion or "Remove invalid columns."
            elif nan_cols:
                code = "ICE006"
                suggestion = suggestion or "Remove NaN columns, rows, or empty columns from the DataFrame"
            else:
                code = "ICE001"
                suggestion = suggestion or "Add missing columns."

        # Wraps the invalid and missing into context.
        context_data = {
            "invalid": invalid,
            "missing": missing,
            "duplicated": duplicated,
            "nan_cols": nan_cols
        }

        # Pass it back to the base.
        super().__init__(
            error_code = code,
            method = method,
            suggestion = suggestion,
            context = context_data
        )