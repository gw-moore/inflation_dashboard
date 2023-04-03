import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
from dash import dcc, html

from inflation_dashboard import inflation_long_df
from inflation_dashboard.utils.pandas import calc_groupby_pct_chg, get_dates

dates = get_dates(inflation_long_df, "date")
cpi_series_column_name = "cpi_series"

mtm_pct_chg_df = calc_groupby_pct_chg(
    df=inflation_long_df,
    by=cpi_series_column_name,
    periods=1,
).dropna()

yty_pct_chg_df = calc_groupby_pct_chg(
    df=inflation_long_df,
    by=cpi_series_column_name,
    periods=12,
).dropna()

mtm_bp_df = (
    mtm_pct_chg_df.groupby(cpi_series_column_name).tail(1).copy().reset_index(drop=True)
)
mtm_bp_df["group"] = "1 Month Percent Change"

yty_bp_df = (
    yty_pct_chg_df.groupby(cpi_series_column_name).tail(1).copy().reset_index(drop=True)
)
yty_bp_df["group"] = "12 Month Percent Change"

bar_plot_df = (
    pd.concat([mtm_bp_df, yty_bp_df]).sort_values("cpi_series").reset_index(drop=True)
)

bar_plot = px.bar(
    data_frame=bar_plot_df,
    x=cpi_series_column_name,
    color="group",
    y="pct_chg_value",
    hover_data={"pct_chg_value": ":.2%"},
    barmode="group",
    color_discrete_sequence=px.colors.qualitative.Safe,
    labels=dict(
        cpi_category="CPI Category",
        group="Months Ago",
        pct_chg_value="Percent Change",
        date="Date",
    ),
)
bar_plot.layout.yaxis.tickformat = ",.0%"
bar_plot.update_layout(
    title_text=f"1 & 12 Month Percent Change, Consumer Price Index for All Urban Consumers, {dates.max}",
)

line_plot = px.line(
    data_frame=inflation_long_df,
    x="date",
    y="value",
    color=cpi_series_column_name,
    title=f"Consumer Price Index for All Urban Consumers, {dates.min} - {dates.max}",
    labels=dict(cpi_category="CPI Category", value="CPI", date="Date"),
    color_discrete_sequence=px.colors.qualitative.Safe,
)

yoy_headline_inflation = yty_bp_df[
    (yty_bp_df[cpi_series_column_name] == "All items")
].iloc[0]["pct_chg_value"]

mtm_headline_inflation = mtm_bp_df[
    (mtm_bp_df[cpi_series_column_name] == "All items")
].iloc[0]["pct_chg_value"]

overview_content = dbc.Container(
    [
        html.H1("CPI Summary"),
        html.Hr(),
        html.H3(f"Latest CPI Data: {dates.max}"),
        html.H2(
            f"Year over year Headline Inflation: {round((yoy_headline_inflation*100),2)}%"
        ),
        html.H2(
            f"Month over month Headline Inflation: {round((mtm_headline_inflation*100),2)}%"
        ),
        html.Br(),
        dcc.Markdown(
            """
            # Percent Change, 1 & 12 Month
            """
        ),
        dcc.Graph(id="barplot", figure=bar_plot),
        dcc.Graph(id="lineplot", figure=line_plot),
    ]
)
