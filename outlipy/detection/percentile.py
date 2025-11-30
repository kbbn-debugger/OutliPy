import pandas as pd
import numpy as np

from typing import Optional, List, Tuple, Union

from .base import OutlierDetectorBase
from ..exceptions import ConfigurationException, DetectionException

class Percentile(OutlierDetectorBase):
    """
    Percentile-based outlier detector.

    A data point is considered an outlier if it falls outside the range 
    defined by the lower and upper percentile bounds.
    """
    def __init__(
            self,
            *,
            threshold: Union[Tuple[float, float], float] = (0.05, 0.95),
            columns: Optional[List[str]] = None
    ):
        if not (isinstance(threshold, tuple) and len(threshold) == 2):
            raise ConfigurationException(
                error_code = "CON002",
                method = self.__class__.__name__,
                parameter_context = "Threshold must be a tuple (lower_percentile, upper_percentile).",
                suggestion = "Example: (0.05, 0.95) for 5th and 95th percentiles."
            )
        lower_q, upper_q = threshold
        if not (0 <= lower_q < upper_q <= 1):
            raise ConfigurationException(
                error_code = "CON002", 
                method = self.__class__.__name__,
                parameter_context = "Percentile values must be between 0 and 1, and lower < upper.",
                suggestion = "Ensure 0.0 <= lower_percentile < upper_percentile <= 1.0."
            )
        
        super().__init__(
            threshold = threshold,
            columns = columns
        )

    
    def _compute_scores(self, df: pd.DataFrame):
        """
        Compute the actual lower and upper bounds corresponding to the percentile thresholds.
        """

        # If suddenly self.columns becomes None.
        if self.columns is None:
            raise RuntimeError("Validation was done, but self.columns remains None")

        data_to_use = df[self.columns]

        self._scores = {} # Resets scores

        if not isinstance(self.threshold, tuple):
            raise ConfigurationException(
                error_code = "CON002",
                method = self.__class__.__name__,
                parameter_context = "Threshold must be a tuple (lower_percentile, upper_percentile).",
                suggestion = "Example: (0.05, 0.95) for 5th and 95th percentiles."
            )

        lower_q, upper_q = self.threshold

        for col in self.columns:
            series = data_to_use[col]

            lower_bound = series.quantile(lower_q)
            upper_bound = series.quantile(upper_q)

            if lower_bound == upper_bound:
                raise DetectionException(
                    error_code = "DET003",
                    method = self.__class__.__name__,
                    suggestion = "The percentile range resulted in zero variance. Remove constant/uninformative features."
                )
            
            self._scores[col] = {
                "lower_bound": lower_bound,
                "upper_bound": upper_bound
            }


    def detect(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Detect outliers based on the calculated percentile bounds.

        :param df: The DataFrame.
        :type df: pd.DataFrame
        :return: The mask where True marks an outlier.
        :rtype: DataFrame
        """

        # Auto fit if it was not fitted yet.
        if not self._fitted:
            self.fit(df)

        # if self.columns is unexpectedly become None.

        if self.columns is None:
            raise RuntimeError("Detector was fitted, but self.columns is unexpectedly None.")

        outlier_mask = pd.DataFrame(False, index = df.index, columns = self.columns)

        for col in self.columns:
            bounds = self._scores[col]
            lower_bound, upper_bound = bounds["lower_bound"], bounds["upper_bound"]
            series = df[col]

            outliers = (series < lower_bound) | (series > upper_bound)

            outlier_mask[col] = outliers

        return outlier_mask