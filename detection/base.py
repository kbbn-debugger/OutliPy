from abc import ABC, abstractmethod
from typing import Optional, List
import pandas as pd
from utils import validate_input

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
        """
        Check if dataframe is valid and columns exist.
        
        Args:
            df (pd.DataFrame): The DataFrame to be validated.
        """

        detector_name = self.__class__.__name__
        columns = self.columns

        validate_input(df, detector_name, columns)


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