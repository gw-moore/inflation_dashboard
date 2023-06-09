"""Dash object for the home page."""

import dash_bootstrap_components as dbc
from dash import dcc, html

from inflation_dashboard import cpi_series_column_name, inflation_long_df
from inflation_dashboard.utils.pandas import (
    _get_subset_long_cpi_data,
    calc_groupby_pct_chg,
    pivot_pct_chg_tbl,
)
from inflation_dashboard.utils.plotly import _mk_line_plot

category = "Education"
edu_series = [
    "Educational books and supplies",
    "Tuition, other school fees, and childcare",
]

long_df = _get_subset_long_cpi_data(long_df=inflation_long_df, series=edu_series)


mtm_pct_chg_df = calc_groupby_pct_chg(
    df=long_df, by=cpi_series_column_name, periods=1
).dropna()

yty_pct_chg_df = calc_groupby_pct_chg(
    df=long_df, by=cpi_series_column_name, periods=12
).dropna()

mtm_pct_chg_pivot_tbl = pivot_pct_chg_tbl(
    df=mtm_pct_chg_df,
    index_col=cpi_series_column_name,
    pct_chg_col="pct_chg_value",
)

mtm_line_plot = _mk_line_plot(
    df=mtm_pct_chg_df,
    title=f"CPI for All Urban Consumers, {category} 1-Month Percent Change",
)

yty_line_plot = _mk_line_plot(
    df=yty_pct_chg_df,
    title=f"CPI for All Urban Consumers, {category} 12-Month Percent Change",
)

month_over_month_tab_content = dbc.Card(
    dbc.CardBody([dcc.Graph(figure=mtm_line_plot)]),
    class_name="mtm",
)

year_over_year_tab_content = dbc.Card(
    dbc.CardBody([dcc.Graph(figure=yty_line_plot)]),
    class_name="yty",
)

edu_content = dbc.Container(
    [
        dcc.Store(id="store"),
        html.H1("Education CPI"),
        html.Hr(),
        dcc.Markdown(
            """
            # Percent Change in Education Prices
            """
        ),
        dbc.Tabs(
            [
                dbc.Tab(year_over_year_tab_content, label="Year-over-Year", id="yty"),
                dbc.Tab(
                    month_over_month_tab_content, label="Month-over-Month", id="mtm"
                ),
            ],
            id="education_tabs",
        ),
        html.Div(id="tab-content", className="p-4"),
    ]
)
