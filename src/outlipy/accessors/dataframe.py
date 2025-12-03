import pandas as pd
from pandas.api.extensions import register_dataframe_accessor

from typing import Optional, List, Union, Tuple

from ..detection import IQRDetector, ZScoreDetector, MADDetector, Percentile
from ..handling import (MeanHandler, MedianHandler, WinsorizationHandler, 
                        RemoveHandler, ConstantHandler, InterpolateHandler,
                        GroupedHandler)
@register_dataframe_accessor("outli")
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

    def percentile(
            self,
            *,
            threshold: Union[Tuple[float, float], float] = (0.05, 0.95),
            columns: Optional[List[str]] = None
    ) -> pd.DataFrame:
        
        method = Percentile(threshold = threshold, columns = columns)
        mask = method.detect(df = self._df)
        return mask
    
    # ------------------------------------------------------
    #                   Handling
    # ------------------------------------------------------

    def mean(
            self,
            *,
            outlier_mask: pd.DataFrame,
            columns: Optional[List[str]] = None
    ) -> pd.DataFrame:
        
        handler = MeanHandler(columns = columns)
        cleaned = handler.apply(self._df, outlier_mask = outlier_mask)
        return cleaned
    
    def median(
            self,
            *,
            outlier_mask: pd.DataFrame,
            columns: Optional[List[str]] = None
    ) -> pd.DataFrame:
        
        handler = MedianHandler(columns = columns)
        cleaned = handler.apply(self._df, outlier_mask = outlier_mask)
        return cleaned
    
    def winsor(
            self,
            *,
            limits: Tuple[float, float] = (0.05, 0.95),
            columns: Optional[List[str]] = None
    ) -> pd.DataFrame:
        
        handler = WinsorizationHandler(limits = limits, columns = columns)
        cleaned = handler.apply(self._df)
        return cleaned
    
    def remove(
            self,
            *,
            outlier_mask: pd.DataFrame,
            columns: Optional[List[str]] = None
    ) -> pd.DataFrame:
        
        handler = RemoveHandler(columns = columns)
        cleaned = handler.apply(df = self._df, outlier_mask = outlier_mask)
        return cleaned
    
    def conrep(
            self,
            *,
            fill_value: float,
            outlier_mask: pd.DataFrame,
            columns: Optional[List[str]] = None
    ) -> pd.DataFrame:
        
        handler = ConstantHandler(fill_value = fill_value, columns = columns)
        cleaned = handler.apply(df = self._df, outlier_mask = outlier_mask)
        return cleaned
    
    def interpolate(
            self,
            *,
            method: str = 'linear',
            outlier_mask: pd.DataFrame,
            columns: Optional[List[str]] = None
    ) -> pd.DataFrame:
        
        handler = InterpolateHandler(method = method, columns = columns)
        cleaned = handler.apply(df = self._df, outlier_mask = outlier_mask)
        return cleaned
    
    def group(
            self,
            *,
            group_by: List[str],
            agg_func: str = "median",
            outlier_mask: pd.DataFrame,
            columns: Optional[List[str]] = None
    ) -> pd.DataFrame:
        
        handler = GroupedHandler(group_by = group_by, agg_func = agg_func, columns = columns)
        cleaned = handler.apply(df = self._df, outlier_mask = outlier_mask)
        return cleaned