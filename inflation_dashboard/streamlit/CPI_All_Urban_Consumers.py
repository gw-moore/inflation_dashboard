"""Streamlit app for the inflation dashboard."""

import pandas as pd
import plotly.express as px
import streamlit as st

from inflation_dashboard import (
    add_sidebar_title,
    cpi_series_column_name,
    inflation_long_df,
)
from inflation_dashboard.utils.pandas import (
    _get_subset_long_cpi_data,
    calc_groupby_pct_chg,
    get_dates,
)
from inflation_dashboard.utils.plotly import _mk_line_plot

st.set_page_config(layout="wide", page_title="U.S. CPI", page_icon=":dollar:")
PLOT_SIZE = {"height": 800, "width": 1400}

add_sidebar_title()

options = sorted(inflation_long_df[cpi_series_column_name].unique())
dates = get_dates(inflation_long_df, "date")

st.markdown("# U.S. Inflation Dashboard")
st.markdown(
    f"### Latest CPI data from the U.S. Bureau of Labor Statistics: {dates.max}"
)

####################
# Headline Numbers
####################
col1, col2 = st.columns(2, gap="small")

headline_long_df = _get_subset_long_cpi_data(
    long_df=inflation_long_df, series="All items"
)

core_mtm_pct_chg_df = calc_groupby_pct_chg(
    df=headline_long_df,
    by=cpi_series_column_name,
    periods=1,
).dropna()
latest_core_mtm_pct_chg = core_mtm_pct_chg_df["pct_chg_value"].iloc[-1]
mtm_delta = round(
    latest_core_mtm_pct_chg - core_mtm_pct_chg_df["pct_chg_value"].iloc[-2]
)

with col1:
    st.metric(
        label="CPI All Items - 1 Month Percent Change",
        value=round(latest_core_mtm_pct_chg * 100, 2),
        delta=mtm_delta,
        delta_color="off" if mtm_delta == 0 else "inverse",
    )

core_yty_pct_chg_df = calc_groupby_pct_chg(
    df=headline_long_df,
    by=cpi_series_column_name,
    periods=12,
).dropna()
latest_core_yty_pct_chg = core_yty_pct_chg_df["pct_chg_value"].iloc[-1]
yty_delta = round(
    latest_core_yty_pct_chg - core_yty_pct_chg_df["pct_chg_value"].iloc[-2], 4
)

with col2:
    st.metric(
        label="CPI All Items - 12 Month Percent Change",
        value=round(latest_core_yty_pct_chg * 100, 2),
        delta=yty_delta,
        delta_color="off" if yty_delta == 0 else "inverse",
    )

##############
# Prep Data
##############
barchart_series = st.sidebar.multiselect(
    label="Filter Series in Bar chart:",
    options=options,
)

bar_chart_long_df = _get_subset_long_cpi_data(
    long_df=inflation_long_df, series=barchart_series
)

mtm_pct_chg_df = calc_groupby_pct_chg(
    df=bar_chart_long_df,
    by=cpi_series_column_name,
    periods=1,
).dropna()

yty_pct_chg_df = calc_groupby_pct_chg(
    df=bar_chart_long_df,
    by=cpi_series_column_name,
    periods=12,
).dropna()

##############
# Bar Plot
##############

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
        cpi_series="CPI Category",
        group="Months Ago",
        pct_chg_value="Percent Change",
        date="Date",
    ),
    **PLOT_SIZE,
)
bar_plot.layout.yaxis.tickformat = ",.0%"
bar_plot.update_layout(
    title_text=f"U.S. Consumer Price Index for All Urban Consumers, 1 & 12 Month Percent Change, {dates.max}",
)
st.plotly_chart(bar_plot)

##############
# Line Plots
##############
lineplot_series = st.sidebar.multiselect(
    label="Filter Series in Line chart:",
    options=options,
    default="All items",
)
# mtm = st.sidebar.checkbox("Month-to-Month Percent Change", value=True, key="mtm")
# yty = st.sidebar.checkbox("Year-to-Year Percent Change", value=True, key="yty")

lineplot_df = _get_subset_long_cpi_data(
    long_df=inflation_long_df, series=lineplot_series
)

mtm_lineplot_df = calc_groupby_pct_chg(
    df=lineplot_df,
    by=cpi_series_column_name,
    periods=1,
).dropna()
mtm_lineplot_df["type"] = "month-to-month"

yty_lineplot_df = calc_groupby_pct_chg(
    df=lineplot_df,
    by=cpi_series_column_name,
    periods=12,
).dropna()
yty_lineplot_df["type"] = "year-to-year"
lineplot_df = yty_lineplot_df

# if mtm and yty:
#     lineplot_df = pd.concat([mtm_lineplot_df, yty_lineplot_df])
# elif mtm:
#     lineplot_df = mtm_lineplot_df
# elif yty:
#     lineplot_df = yty_lineplot_df

yty_line_plot = _mk_line_plot(
    df=lineplot_df,
    title=f"U.S. CPI for All Urban Consumers, 12-Month Percent Change, {dates.min} - {dates.max}",
    plot_size=PLOT_SIZE,
)

# st.plotly_chart(mtm_line_plot)
st.plotly_chart(yty_line_plot)
