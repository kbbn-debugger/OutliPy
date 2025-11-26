from abc import ABC, abstractmethod
from typing import Optional, List
import pandas as pd
from ..exceptions import HandlingException
from utils import validate_input

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
        """
        Check if dataframe is valid and columns exist.
        
        Args:
            df (pd.DataFrame): The DataFrame to be validated.
        """

        detector_name = self.__class__.__name__
        columns = self.columns

        validate_input(df, detector_name, columns)

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