"""Make plotly time series plot for percent change"""

from typing import Tuple

import pandas as pd
import plotly.express as px
from plotly.graph_objects import Figure


def _mk_line_plot(
    month_over_month_df: pd.DataFrame,
    year_over_year_df: pd.DataFrame,
    category: str,
    series_column_name: str = "cpi_series",
) -> Tuple[Figure, Figure]:
    mtm_line_plot = px.line(
        data_frame=month_over_month_df,
        x="date",
        y="pct_chg_value",
        color=series_column_name,
        title=f"CPI for All Urban Consumers, {category}, 1-Month Percent Change",
        labels=dict(
            cpi_series="CPI Series", pct_chg_value="Percent Change", date="Date"
        ),
        hover_data={"pct_chg_value": ":.2%"},
        color_discrete_sequence=px.colors.qualitative.Safe,
    )
    mtm_line_plot.layout.yaxis.tickformat = ",.2%"

    yty_line_plot = px.line(
        data_frame=year_over_year_df,
        x="date",
        y="pct_chg_value",
        color=series_column_name,
        title=f"CPI for All Urban Consumers, {category}, 12-Month Percent Change",
        labels=dict(
            cpi_series="CPI Series", pct_chg_value="Percent Change", date="Date"
        ),
        hover_data={"pct_chg_value": ":.2%"},
        color_discrete_sequence=px.colors.qualitative.Safe,
    )
    yty_line_plot.layout.yaxis.tickformat = ",.2%"

    return mtm_line_plot, yty_line_plot
