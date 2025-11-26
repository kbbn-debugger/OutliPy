import pandas as pd
import numpy as np
from typing import Optional, List
from exceptions import InvalidColumnException



def validate_input(df: pd.DataFrame, detector_name: str, columns: Optional[List[str]]):
    """
    Check if dataframe is valid and columns exist.
    
    Args:
        df (pd.DataFrame): The DataFrame to be validated.
        detector_name (str): The name of the detector.
        columns (Optional[List[str]]): A list of strings passed for checking.
    """

    # Basic Type Check
    if not isinstance(df, pd.DataFrame):
        raise TypeError(f"[{detector_name}] Input must be a pandas DataFrame, got {type(df).__name__}")

    # Check if DataFrame is empty
    if df.empty:
        raise InvalidColumnException(
            method = detector_name,
            error_code = "ICE007",
            suggestion = "Please input a non-empty DataFrame"
        )

    # Check for duplicated columns
    if df.columns.duplicated().any():
        dup_list = df.columns[df.columns.duplicated()].unique().to_list()
        raise InvalidColumnException(
            method = detector_name,
            duplicated = dup_list
        )


    cols_to_check: List[str] = []

    # Auto-select columns if None provided
    if columns is None:
        cols_to_check = df.select_dtypes(include=[np.number]).columns.tolist()
        
        # If still empty, it means no numeric data exists in the whole DF
        if not cols_to_check:
            raise InvalidColumnException(
                method = detector_name,
                no_numeric = True                 # Flags the no_numeric into True, raises ICE002
            )
    else:
        # Flags if user input an empty list. Default is None
        if not cols_to_check:
            raise InvalidColumnException(
                method = detector_name,
                error_code = "ICE000",
                suggestion = "You provided an empty list of columns. Please specify columns."
            )
        
        # Flags if user input duplicate column names. Example ["age", "age"]
        if len(cols_to_check) != len(set(cols_to_check)):
            seen = set()
            dupes = [x for x in cols_to_check if x in seen or seen.add(x)]
            raise InvalidColumnException(
                error_code = "ICE005",
                method = detector_name,
                duplicated = dupes,
                suggestion = "Remove duplicate column names from your configuration list."
            )               

    # Validate specific columns
    missing_cols = []
    invalid_cols = []
    nan_inf_cols = []

    for col in cols_to_check:
        # Check if column/s are missing
        if col not in df.columns:
            missing_cols.append(col)
        # Check if existing column is actually numeric
        elif not pd.api.types.is_numeric_dtype(df[col]):
            invalid_cols.append(col)
        # Check if NaNs exist in rows and empty columns
        elif df[col].isna().any() or np.isinf(df[col]).any():
            nan_inf_cols.append(col)

    # Raise Exception if ANY more issues found
    if missing_cols or invalid_cols or nan_inf_cols:
        raise InvalidColumnException(
            method = detector_name,
            missing = missing_cols,
            invalid = invalid_cols,
            nan_cols = nan_inf_cols
        )