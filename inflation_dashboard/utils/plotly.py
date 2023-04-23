"""Make plotly time series plot for percent change"""

from typing import Dict

import pandas as pd
import plotly.express as px
from plotly.graph_objects import Figure


def _mk_line_plot(
    df: pd.DataFrame,
    title: str,
    series_column_name: str = "cpi_series",
    plot_size: Dict[str, int] | None = None,
) -> Figure:
    """Create plotly line graph for CPI Series.

    Parameters
    ----------
    df : pd.DataFrame
        Long pandas data graph
    title : str
        Graph title
    series_column_name : str, optional
        Column name of the cpi series, by default "cpi_series"
    plot_size : Dict[str, int] | None, optional
        Customize the plot size with dictionary, by default None
        Example:
            {"height": 600, "width": 800}

    Returns
    -------
    Figure
    """
    if plot_size is None:
        plot_size = {}
    plot = px.line(
        data_frame=df,
        x="date",
        y="pct_chg_value",
        color=series_column_name,
        title=title,
        labels=dict(
            cpi_series="CPI Series", pct_chg_value="Percent Change", date="Date"
        ),
        hover_data={"pct_chg_value": ":.2%"},
        color_discrete_sequence=px.colors.qualitative.Safe,
        **plot_size,
    )
    plot.layout.yaxis.tickformat = ",.2%"

    return plot
