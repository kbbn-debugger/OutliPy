import pandas as pd
from pandas.api.extensions import register_dataframe_accessor

@register_dataframe_accessor("Outli")
class OutlierAccessor:
    def __init__(self, pandas_obj):
        self._df = pandas_obj
        pass

    # ------------------------------------
    #            Direct method
    # ------------------------------------

