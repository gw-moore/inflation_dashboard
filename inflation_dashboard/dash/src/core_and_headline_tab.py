"""Dash object for the home page."""

import dash_bootstrap_components as dbc
from dash import dcc, html

from inflation_dashboard import cpi_series_column_name, inflation_long_df
from inflation_dashboard.utils.pandas import (
    _get_subset_long_cpi_data,
    calc_groupby_pct_chg,
    get_dates,
    pivot_pct_chg_tbl,
)
from inflation_dashboard.utils.plotly import _mk_line_plot

core_and_headline_series = ["All items", "All items less food and energy"]
category = "Core & Headline"

long_df = _get_subset_long_cpi_data(
    long_df=inflation_long_df, series=core_and_headline_series
)
dates = get_dates(long_df, "date")

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


def generate_table(dataframe, max_rows=10):
    return html.Table(
        [
            html.Thead(html.Tr([html.Th(col) for col in dataframe.columns])),
            html.Tbody(
                [
                    html.Tr(
                        [html.Td(dataframe.iloc[i][col]) for col in dataframe.columns]
                    )
                    for i in range(min(len(dataframe), max_rows))
                ]
            ),
        ]
    )


month_over_month_tab_content = dbc.Card(
    dbc.CardBody([dcc.Graph(figure=mtm_line_plot)]),
    class_name="mtm",
)

year_over_year_tab_content = dbc.Card(
    dbc.CardBody([dcc.Graph(figure=yty_line_plot)]),
    class_name="yty",
)

headline_and_core_content = dbc.Container(
    [
        dcc.Store(id="store"),
        html.H1("Core & Headline CPI"),
        html.Hr(),
        dcc.Markdown(
            """
            # Percent Change Time Series Plots
            """
        ),
        dbc.Tabs(
            [
                dbc.Tab(year_over_year_tab_content, label="Year-over-Year", id="yty"),
                dbc.Tab(
                    month_over_month_tab_content, label="Month-over-Month", id="mtm"
                ),
            ],
            id="headline_and_core_tabs",
        ),
        html.Div(id="tab-content", className="p-4"),
    ]
)
