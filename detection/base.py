from abc import ABC, abstractmethod
from typing import Optional, List
import pandas as pd
import numpy as np
from ..exceptions import DetectionException, InvalidColumnException

class OutlierDetectorBase(ABC):
    """
    Abstract base class for all Outlier Detectors in OutliPy.

    Attributes:
        threshold (float): Threshold for detecting outliers.
        columns (Optional[List[str]]): Columns to analyze. If None, all numeric columns are used.
    """

    def __init__(self, threshold: float = 3.0, columns: Optional[List[str]] = None):
        self.threshold = threshold
        self.columns = columns
        self._fitted = False
        self._scores = {}  # Stores computed outlier scores per column

    def __repr__(self):
        return f"{self.__class__.__name__}(threshold={self.threshold}, columns={self.columns})"

    def __str__(self):
        cols = self.columns if self.columns else "All numeric columns"
        return f"{self.__class__.__name__} using threshold {self.threshold} on {cols}"

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


    def fit(self, df: pd.DataFrame):
        """
        Fit detector to the dataframe. Computes any statistics required for detection.

        Args:
            df (pd.DataFrame): Input DataFrame.
        """
        self._validate_input(df)
        self._compute_scores(df)
        self._fitted = True
        return self

    @abstractmethod
    def _compute_scores(self, df: pd.DataFrame):
        """
        Compute outlier scores for the dataframe columns.
        To be implemented by each specific detector.
        """
        pass

    @abstractmethod
    def detect(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Detect outliers and return a boolean DataFrame indicating outliers.

        Args:
            df (pd.DataFrame): Input DataFrame

        Returns:
            pd.DataFrame: Boolean mask where True indicates an outlier.
        """
        pass