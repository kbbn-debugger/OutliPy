import pandas as pd
from exceptions import DetectionException, ConfigurationException
from typing import Optional, List
from base import OutlierDetectorBase
from utils import select_numeric_columns

class IQRDetector(OutlierDetectorBase):
    """
    Interquartile Range (IQR) based outlier detector.

    threshold: multiplier for IQR to define the bounds.
               Typical default = 1.5 or 3.0 depending on desired sensitivity.
    """
    def __init__(
            self,
            threshold: float = 1.5,
            columns: Optional[List[str]] =None
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
        Compute Q1, Q3, IQR, and lower/upper bounds for each selected column.

        :param df: The DataFrame
        :type df: pd.DataFrame
        """

        numeric_df = select_numeric_columns(df, self.columns)

        self._scores = {}  # reset scores

        for col in numeric_df.columns:
            q1 = numeric_df[col].quantile(0.25)
            q3 = numeric_df[col].quantile(0.75)
            iqr = q3 - q1

            if iqr == 0:
                # Rase DET004 Zero Variance - cannot compute IQR-based outliers
                raise DetectionException(
                    error_code = "DET004",
                    method = self.__class__.__name__,
                    suggestion = "Remove Constant/Uninformative Features or verify Data Preprocessing"
                )
   
            lower = q1 - self.threshold * iqr
            upper = q3 + self.threshold * iqr

            self._scores[col] = {
                "q1": q1,
                "q3": q3,
                "iqr": iqr,
                "lower": lower,
                "upper": upper
            }

    def detect(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Return a DataFrame of booleans where True marks an outlier.

        :param df: The DataFrame.
        :type df: pd.DataFrame
        :return: The mask where True marks an outlier.
        :rtype: DataFrame
        """

        if not self._fitted:
            self.fit(df)

        numeric_df = select_numeric_columns(df)

        outlier_mask = pd.DataFrame(False, index = df.index, columns = numeric_df.columns)

        for col in numeric_df.columns:
            bounds = self._scores[col]
            lower, upper = bounds["lower"], bounds["upper"]
            series = numeric_df[col]

            outliers = (series < lower) | (series > upper)
            outlier_mask[col] = outliers

        return outlier_mask

