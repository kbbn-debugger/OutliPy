# under utilized


import pandas as pd
from typing import Optional, List

def select_numeric_columns(
        df: pd.DataFrame, 
        columns: Optional[List[str]] = None
) -> pd.DataFrame:
    """
    Returns a numeric-only dataframe using either explicit columns or auto-selection.
    
    :param df: The DataFrame
    :type df: pd.DataFrame
    :param columns: The columns selected, if None (default) automatically selects numerical columns.
    :type columns: Optional[List[str]]
    :return: The numeric-only DataFrame.
    :rtype: DataFrame
    """

    if columns:
        return df[columns]
    
    return df.select_dtypes(include = "number")