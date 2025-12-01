import pandas as pd
import numpy as np

from typing import Optional, List

from ..exceptions import ConfigurationException, DetectionException

from .base import OutlierDetectorBase



class ZScoreDetector(OutlierDetectorBase):
    """
    Z-score based outlier detector.

    A data point is considered an outlier if its absolute Z-score is greater 
    than the defined threshold (typically 3.0).
    """
    def __init__(
            self,
            threshold: float = 3.0,
            columns: Optional[List[str]] = None
    ):
        if threshold <= 0:
            raise ConfigurationException(
                error_code = "CON002", 
                method = self.__class__.__name__,
                parameter_context = "threshold <= 0",
                suggestion = "Please input a value greater than 0."
            )
        
        super().__init__(
            threshold = threshold,
            columns = columns
        )
    
    def _compute_scores(self, df: pd.DataFrame):
        """
        Compute the mean and standard deviation for each selected column.

        :param df: The DataFrame
        :type df: pd.DataFrame
        """

        # If suddenly self.columns becomes None.
        if self.columns is None:
            raise RuntimeError("Validation was done, but self.columns remains None")

        data_to_use = df[self.columns]

        self._scores = {} # Resets scores

        for col in self.columns:
            series = data_to_use[col]

            mean = series.mean()
            std_dev = series.std(ddof = 0)

            if std_dev == 0:
                raise DetectionException(
                    error_code = "DET003",
                    method = self.__class__.__name__,
                    suggestion = "Remove Constant/Uninformative Features or verify Data Preprocessing (Standard deviation is zero)."
                )
            
            self._scores[col] = {
                "mean": mean,
                "std_dev": std_dev
            }


    def detect(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Detect outliers based on the Z-score threshold.

        :param df: The DataFrame
        :type df: pd.DataFrame
        """
        if not self._fitted:
            self.fit(df)

        if self.columns is None:
            raise RuntimeError("Detector was fitted, but self.columns is unexpectedly None.")
        
        outlier_mask = pd.DataFrame(False, index = df.index, columns = self.columns)

        for col in self.columns:
            stats = self._scores[col]
            mean, std_dev = stats['mean'], stats['std_dev']
            series = df[col]

            z_scores = np.abs((series - mean) / std_dev)

            outliers = z_scores > self.threshold

            outlier_mask[col] = outliers

        return outlier_mask