"""Streamlit app for the inflation dashboard."""

import pandas as pd
import plotly.express as px
import streamlit as st

from inflation_dashboard import cpi_series_column_name, inflation_long_df
from inflation_dashboard.utils.pandas import (
    _get_subset_long_cpi_data,
    calc_groupby_pct_chg,
    get_dates,
)
from inflation_dashboard.utils.plotly import _mk_line_plot

PLOT_SIZE = {"height": 800, "width": 1100}

# st.set_page_config(layout="wide")

options = inflation_long_df[cpi_series_column_name].unique()
option = st.sidebar.multiselect(
    label="Filter Series:",
    options=options,
)

long_df = _get_subset_long_cpi_data(long_df=inflation_long_df, series=option)
dates = get_dates(long_df, "date")

st.markdown("# U.S. Inflation Dashboard")
st.markdown(f"### Latest CPI data from the BLS: {dates.max}")

##############
# Prep Data
##############
mtm_pct_chg_df = calc_groupby_pct_chg(
    df=long_df,
    by=cpi_series_column_name,
    periods=1,
).dropna()

yty_pct_chg_df = calc_groupby_pct_chg(
    df=long_df,
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
    title_text=f"1 & 12 Month Percent Change, U.S. Consumer Price Index for All Urban Consumers, {dates.max}",
)
st.plotly_chart(bar_plot)

##############
# Line Plots
##############
mtm_line_plot = _mk_line_plot(
    df=mtm_pct_chg_df,
    title="U.S. CPI for All Urban Consumers, 1-Month Percent Change",
    plot_size=PLOT_SIZE,
)

yty_line_plot = _mk_line_plot(
    df=yty_pct_chg_df,
    title="U.S. CPI for All Urban Consumers, 12-Month Percent Change",
    plot_size=PLOT_SIZE,
)

st.plotly_chart(mtm_line_plot)
st.plotly_chart(yty_line_plot)
