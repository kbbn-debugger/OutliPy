import pandas as pd
import numpy as np

from typing import Optional, List

from .base import OutlierDetectorBase
from ..exceptions import ConfigurationException, DetectionException

class MADDetector(OutlierDetectorBase):
    """
    
    """
    def __init__(
            self,
            *,
            threshold: float = 3.5,
            columns: Optional[List[str]] = None
    ):
        if threshold < 0:
            raise ConfigurationException(
                error_code = "CON002", 
                method = self.__class__.__name__,
                parameter_context = "threshold < 0",
                suggestion = "Please input a value greater than 0."
            )
        
        super().__init__(
            threshold = threshold,
            columns = columns
        )

    
    def _compute_scores(self, df: pd.DataFrame):
        """
        Compute the median and Median Absolute Deviation (MAD) for each column.
        """

        # If suddenly self.columns becomes None.
        if self.columns is None:
            raise RuntimeError("Validation was done, but self.columns remains None")

        data_to_use = df[self.columns]

        self._scores = {} # Resets scores

        self.scaling_factor = 0.67449

        for col in self.columns:
            series = data_to_use[col]

            median = series.median()

            mad = (series - median).abs().median()

            if median == 0:
                raise DetectionException(
                    error_code = "DET005",
                    method = self.__class__.__name__,
                    suggestion = "Zero Modified Absolute Deviation (MAD = 0). Remove constant/uninformative features."
                )
            
            self._scores[col] = {
                "median": median,
                "mad": mad
            }

    def detect(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Return a DataFrame of booleans where True marks an outlier.

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
            stats = self._scores[col]
            median, mad = stats["median"], stats["mad"]
            series = df[col]

            modified_zscores = self.scaling_factor * np.abs(series - median) / mad

            outliers = modified_zscores > self.threshold

            outlier_mask[col] = outliers

        return outlier_mask