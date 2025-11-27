import pandas as pd
import numpy as np
from typing import Optional, List
from .base import OutlierHandlerBase
from ..exceptions.handling import HandlingException

class OutlierHandler(OutlierHandlerBase):
    """
    Concrete implementation of OutlierHandlerBase.
    Provides strategies to correct, replace, or mitigate outliers.

    Additional Args in __init__:
        fill_value (Any): Value to use for 'constant' replacement.
        limits (Tuple[float, float]): Percentiles for 'winsorization' (e.g., (0.05, 0.95)).
        group_col (str): Column name to group by for 'group_based' replacement.
    """

    def __init__(self, 
                 method: str = "mean", 
                 columns: Optional[List[str]] = None, 
                 **kwargs):
        super().__init__(method=method, columns=columns)
        self.kwargs = kwargs

        self.ALLOWED_METHODS = [
            "remove", "mean", "median", "winsorization", 
            "constant", "group_based", "interpolation"
        ]

    def apply(self, df: pd.DataFrame, outlier_mask: Optional[pd.DataFrame] = None) -> pd.DataFrame:
        """
        Apply the selected outlier handling strategy.
        """
        self._validate_input(df)
        self._validate_strategy(self.ALLOWED_METHODS)
        
        # Work on a copy to avoid SettingWithCopy warnings on the user's original df
        df_clean = df.copy()

        # Strategy: Winsorization (Self-contained, no mask needed)
        if self.method == "winsorization":
            return self._handle_winsorization(df_clean)

        # -- VALIDATION FOR MASK-DEPENDENT METHODS --
        if outlier_mask is None:
             raise HandlingException(f"Method '{self.method}' requires an outlier_mask.")
        
        # Robustness Check 1: Ensure Indices Match
        if not df.index.equals(outlier_mask.index):
            raise HandlingException("Index mismatch: DataFrame and outlier_mask must have the same index.")

        # Strategy: Removal
        if self.method == "remove":
            return self._handle_removal(df_clean, outlier_mask)

        # Strategy: Constant Replacement
        if self.method == "constant":
            return self._handle_constant(df_clean, outlier_mask)

        # Strategy: Mean/Median Replacement
        if self.method in ["mean", "median"]:
            return self._handle_central_tendency(df_clean, outlier_mask)

        # Strategy: Interpolation
        if self.method == "interpolation":
            return self._handle_interpolation(df_clean, outlier_mask)

        # Strategy: Group-Based Replacement
        if self.method == "group_based":
            return self._handle_group_based(df_clean, outlier_mask)

        return df_clean

    def _handle_removal(self, df: pd.DataFrame, mask: pd.DataFrame) -> pd.DataFrame:
        """Deletes rows containing at least one outlier in the selected columns."""
        # Robustness Check 2: Intersect columns to avoid KeyErrors
        valid_cols = [c for c in self.columns if c in mask.columns]
        
        if not valid_cols:
            return df # No columns to check, return original
            
        relevant_mask = mask[valid_cols]
        # Keep rows where NO outliers exist in the relevant columns
        return df[~relevant_mask.any(axis=1)]

    def _handle_winsorization(self, df: pd.DataFrame) -> pd.DataFrame:
        """Caps values at defined percentiles."""
        limits = self.kwargs.get('limits', (0.05, 0.95))
        
        # Logic Fix: Validate limits to prevent crashes or logical errors
        if not (isinstance(limits, tuple) and len(limits) == 2):
             raise HandlingException("Winsorization 'limits' must be a tuple of two floats (e.g., (0.05, 0.95)).")
        
        lower_q, upper_q = limits
        if not (0 <= lower_q < upper_q <= 1):
             raise HandlingException("Winsorization limits must be between 0 and 1, and lower < upper.")

        for col in self.columns:
            # Skip non-numeric columns if they slipped through validation
            if not pd.api.types.is_numeric_dtype(df[col]):
                continue
                
            lower_limit = df[col].quantile(lower_q)
            upper_limit = df[col].quantile(upper_q)
            df[col] = df[col].clip(lower=lower_limit, upper=upper_limit)
        
        return df

    def _handle_constant(self, df: pd.DataFrame, mask: pd.DataFrame) -> pd.DataFrame:
        """Replaces outliers with a fixed constant."""
        fill_value = self.kwargs.get('fill_value', 0)
        
        for col in self.columns:
            if col in mask.columns:
                df.loc[mask[col], col] = fill_value
        return df

    def _handle_central_tendency(self, df: pd.DataFrame, mask: pd.DataFrame) -> pd.DataFrame:
        """Replaces outliers with Mean or Median."""
        for col in self.columns:
            if col in mask.columns:
                # 1. Isolate the column
                series = df[col].copy()
                
                # 2. Set outliers to NaN locally so they don't skew the calculation
                outliers = mask[col]
                if not outliers.any():
                    continue # Nothing to replace
                    
                series[outliers] = np.nan
                
                # 3. Calculate stat on valid data
                val = series.mean() if self.method == "mean" else series.median()
                
                # 4. Inject value ONLY into outlier positions in the main DF
                df.loc[outliers, col] = val
        return df

    def _handle_interpolation(self, df: pd.DataFrame, mask: pd.DataFrame) -> pd.DataFrame:
        """Uses interpolation to fill outlier positions."""
        for col in self.columns:
            if col in mask.columns:
                # Set to NaN specifically where outliers are
                df.loc[mask[col], col] = np.nan
                # Interpolate fills NaNs based on neighbors
                df[col] = df[col].interpolate(method='linear', limit_direction='both')
        return df

    def _handle_group_based(self, df: pd.DataFrame, mask: pd.DataFrame) -> pd.DataFrame:
        """Replaces outliers based on group summary statistics."""
        group_col = self.kwargs.get('group_col')
        if not group_col or group_col not in df.columns:
            raise HandlingException("Method 'group_based' requires a valid 'group_col' in kwargs.")

        for col in self.columns:
            if col in mask.columns and col != group_col:
                outliers = mask[col]
                if not outliers.any():
                    continue

                # 1. Create a series where outliers are NaN
                temp_series = df[col].copy()
                temp_series[outliers] = np.nan

                # 2. Calculate the transform (median) per group ignoring NaNs
                # Logic Fix: Optimized groupby to avoid creating a full DataFrame copy
                replacements = temp_series.groupby(df[group_col]).transform('median')
                
                # 3. Fill ONLY the outliers with the calculated replacements
                df.loc[outliers, col] = replacements[outliers]

                # 4. Fallback: If a group was entirely outliers/NaNs, fill with global median
                remaining_nans = df[col].isna() & outliers
                if remaining_nans.any():
                    global_median = temp_series.median()
                    df.loc[remaining_nans, col] = global_median

        return df
