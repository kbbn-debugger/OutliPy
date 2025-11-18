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

    def __init__(self, method: str = "mean", columns: Optional[List[str]] = None):
        self.method = method
        self.columns = columns
        self._validated = False

    def __repr__(self):
        return f"{self.__class__.__name__}(method = {self.method}, columns = {self.columns})"
    
    def __str__(self):
        cols = self.columns if self.columns else "All numeric columns"
        return f"{self.__class__.__name__} using strategy '{self.method}' on {cols}"

    def _validate_input(self, df: pd.DataFrame):
        """Validate input DataFrame and columns"""
        if not isinstance(df, pd.DataFrame): # type: ignore
            raise HandlingException("Input must be a pandas DataFrame.")
        
        if self.columns:
            missing = [col for col in self.columns if col not in df.columns]
            if missing:
                raise InvalidColumnException(f"The following columns are missing in DataFrame: {missing}")
            
        else:
            # Default to numeric columns only
            self.columns = df.select_dtypes(include=[np.number]).columns.tolist()
            if not self.columns:
                raise InvalidColumnException("No numeric columns found for handling.")

    def _validate_strategy(self, allowed_methods: Optional[List[str]] = None):
        """
        Validate that the chosen strategy is allowed.

        Args:
            allowed_methods (Optional[List[str]]): List of allowed strategy.
        """

        if allowed_methods is None:
            return # no restrictions
        
        if self.method not in allowed_methods:
            raise HandlingException(f"Method '{self.method}' is not allowed. Choose from {allowed_methods}")
        
        self._validated = True

    @abstractmethod
    def apply(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Apply outlier handling to the DataFrame.
        Must be implemented by subclasses.

        Returns:
            pd.DataFrame: DataFrame with outliers handled.
        """
        pass