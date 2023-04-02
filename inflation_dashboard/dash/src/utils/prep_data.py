"""Routine data prep used in each tab of the report.
"""

from typing import List, Union
import pandas as pd


def _get_subset_long_cpi_data(
    long_df: pd.DataFrame,
    series: Union[List[str], None] = None,
) -> pd.DataFrame:
    """Get a subset of the CPI series in the CPI series collection."""

    if series:
        long_df = long_df[long_df["cpi_series"].isin(series)]

    return long_df
