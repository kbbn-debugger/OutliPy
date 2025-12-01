import pandas as pd

from typing import Optional, List, Tuple

from .base import OutlierHandlerBase
from ..exceptions import HandlingException, ConfigurationException

class WinsorizationHandler(OutlierHandlerBase):
    
    METHOD_NAME = "winsorization"
    
    def __init__(
        self, 
        limits: Tuple[float, float] = (0.05, 0.95), 
        columns: Optional[List[str]] = None
    ):
        super().__init__(method=self.METHOD_NAME, columns=columns)
        
        # Validation for limits
        if not (isinstance(limits, tuple) and len(limits) == 2 and all(isinstance(i, (int, float)) for i in limits)):
            raise ConfigurationException(
                error_code="CON004", 
                method=self.__class__.__name__, 
                parameter="limits", 
                suggestion="Winsorization 'limits' must be a tuple of two floats (e.g., (0.05, 0.95))."
            )
            
        lower_q, upper_q = limits

        if not (0 <= lower_q < upper_q <= 1):
             raise ConfigurationException(
                error_code="CON002",
                method=self.__class__.__name__,
                parameter_context="Winsorization limits must be between 0 and 1, and lower < upper.",
                suggestion="Ensure 0.0 <= lower_limit < upper_limit <= 1.0."
            )

        self.limits = limits

    def apply(self, df: pd.DataFrame, outlier_mask: Optional[pd.DataFrame] = None) -> pd.DataFrame:
        """Caps values at defined percentiles."""
        
        # No mask needed, but we check if columns are set
        if self.columns is None:
            return df.copy() # Return copy if no columns specified
            
        df_clean = df.copy()
        lower_q, upper_q = self.limits

        for col in self.columns:
            if col not in df_clean.columns or not pd.api.types.is_numeric_dtype(df_clean[col]):
                continue # Skip non-existent or non-numeric columns
                
            lower_limit = df_clean[col].quantile(lower_q)
            upper_limit = df_clean[col].quantile(upper_q)
            
            # Check for invalid bounds
            if lower_limit >= upper_limit:
                 raise HandlingException(
                    error_code="HEX003",
                    method=self.__class__.__name__,
                    suggestion=f"Winsorization bounds are identical or reversed for column '{col}'. Data may be constant."
                )

            # Core winsorization logic
            df_clean[col] = df_clean[col].clip(lower=lower_limit, upper=upper_limit)
            
        return df_clean