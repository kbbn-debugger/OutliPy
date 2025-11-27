import pandas as pd
from pandas.api.extensions import register_dataframe_accessor
from typing import Optional, List
from detection import IQRDetector

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
        
        :param threshold: The IQR multiplier used to determine outlier boundaries.
        :type threshold: float
        :param columns: Columns to evaluate. If None, detector should auto-detect numeric columns.
        :return: DataFrame of booleans: True = outlier, False = normal.
        :rtype: DataFrame
        """

        method = IQRDetector(threshold = threshold, columns = columns)
        mask = method.detect(df = self._df)
        return mask


