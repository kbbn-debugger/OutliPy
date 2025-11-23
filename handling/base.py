from abc import ABC, abstractmethod
from typing import Optional, List
import pandas as pd
import numpy as np
from ..exceptions import HandlingException, InvalidColumnException

class OutlierHandlerBase(ABC):
    """
    Abstract base class for all Outlier Handling in OutliPy

    attributes:
        methods (str): The method used for handling outliers (e.g., "mean", "median", "winsorization").
        columns (Optional[List[str]]): Columns to apply handling on.
    """

    def __init__(self, *, method: Optional[str] = None, columns: Optional[List[str]] = None):
        self.method = method or self.__class__.__name__
        self.columns = columns
        self._validated = False

    def __repr__(self):
        return f"{self.__class__.__name__}(method = {self.method}, columns = {self.columns})"
    
    def __str__(self):
        cols = self.columns if self.columns else "All numeric columns"
        return f"{self.__class__.__name__} using strategy '{self.method}' on {cols}"

    def _validate_input(self, df: pd.DataFrame):
        """Check if dataframe is valid and columns exist."""
        detector_name = self.__class__.__name__

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

        # Auto-select columns if None provided
        if self.columns is None:
            self.columns = df.select_dtypes(include=[np.number]).columns.tolist()
            
            # If still empty, it means no numeric data exists in the whole DF
            if not self.columns:
                raise InvalidColumnException(
                    method = detector_name,
                    no_numeric = True                 # Flags the no_numeric into True, raises ICE002
                )
        else:
            # Flags if user input an empty list. Default is None
            if not self.columns:
                raise InvalidColumnException(
                    method = detector_name,
                    error_code = "ICE000",
                    suggestion = "You provided an empty list of columns. Please specify columns."
                )
            
            # Flags if user input duplicate column names. Example ["age", "age"]
            if len(self.columns) != len(set(self.columns)):
                seen = set()
                dupes = [x for x in self.columns if x in seen or seen.add(x)]
                raise InvalidColumnException(
                    error_code = "ICE005",
                    method = detector_name,
                    duplicated = dupes,
                    suggestion = "Remove duplicate column names from your configuration list."
                )               

        # Validate specific columns
        missing_cols = []
        invalid_cols = []
        nan_cols = []

        for col in self.columns:
            # Check if column/s are missing
            if col not in df.columns:
                missing_cols.append(col)
            # Check if existing column is actually numeric
            elif not pd.api.types.is_numeric_dtype(df[col]):
                invalid_cols.append(col)
            # Check if NaNs exist in rows and empty columns
            elif df[col].isna().any() or np.isinf(df[col]).any():
                nan_cols.append(col)

        # Raise Exception if ANY more issues found
        if missing_cols or invalid_cols or nan_cols:
            raise InvalidColumnException(
                method = detector_name,
                missing = missing_cols,
                invalid = invalid_cols,
                nan_cols = nan_cols
            )

    def _validate_strategy(self, allowed_methods: Optional[List[str]] = None):
        """
        Validate that the chosen strategy is allowed.

        Args:
            allowed_methods (Optional[List[str]]): List of allowed strategy.
        """

        if allowed_methods is None:
            return # no restrictions
        
        if self.method not in allowed_methods:
            raise HandlingException(
                error_code = "HEX000",
                method = self.method,
                typed_method = self.method,
                allowed_methods = allowed_methods
            )
        
        self._validated = True

    @abstractmethod
    def apply(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Apply outlier handling to the DataFrame.

        Returns:
            pd.DataFrame: DataFrame with outliers handled.
        """
        pass