import pandas as pd
from pandas.api.extensions import register_dataframe_accessor

from typing import Optional, List

from ..detection import IQRDetector, ZScoreDetector, MADDetector

@register_dataframe_accessor("Outli")
class OutlierAccessor:
    def __init__(self, pandas_obj):
        self._df = pandas_obj

    # ------------------------------------
    #            Direct methods
    # ------------------------------------

    def iqr(
            self, 
            *, 
            threshold: float = 1.5, 
            columns: Optional[List[str]] = None
    ) -> pd.DataFrame:
        """
        Detect outliers using the IQR method.
        
        :param threshold: The number of standard deviations from the mean used as the cutoff point. Any data point whose absolute Z-score exceeds this value is considered an outlier. (Default is 3.0).
        :type threshold: float
        :type threshold: float
        :param columns: Columns to evaluate. If None, detector should auto-detect numeric columns.
        :return: DataFrame of booleans: True = outlier, False = normal.
        :rtype: DataFrame
        """

        method = IQRDetector(threshold = threshold, columns = columns)
        mask = method.detect(df = self._df)
        return mask

    def zscore(
            self, 
            *, 
            threshold: float = 3.0, 
            columns: Optional[List[str]] = None
    ) -> pd.DataFrame:
        """
        Detect outliers using the Zscore method.
        
        :param threshold: The value used to determine outlier boundaries.
        :type threshold: float
        :param columns: Columns to evaluate. If None, detector should auto-detect numeric columns.
        :return: DataFrame of booleans: True = outlier, False = normal.
        :rtype: DataFrame
        """

        method = ZScoreDetector(threshold = threshold, columns = columns)
        mask = method.detect(df = self._df)
        return mask
    
    def mad(
            self,
            *,
            threshold: float = 3.0,
            columns: Optional[List[str]] = None
    ) -> pd.DataFrame:
        """
        
        """

        method = MADDetector(threshold = threshold, columns = columns)
        mask = method.detect(df = self._df)
        return mask
