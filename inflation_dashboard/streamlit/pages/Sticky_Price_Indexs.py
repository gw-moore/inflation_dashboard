import pandas as pd
import plotly.express as px
import pyfredapi as pf
import streamlit as st

from inflation_dashboard import add_sidebar_title
from inflation_dashboard.utils.pandas import (
    calc_groupby_pct_chg,
    get_dates,
)

st.set_page_config(layout="wide", page_title="cpi", page_icon=":moneybag:")
add_sidebar_title()
st.markdown("# U.S. Inflation Dashboard - Sticky Price Indexes")

cpi_series_column_name = "sticky_cpi_series"
# The category id for special indexes is 32424
special_indexes = pf.get_category_series("32424")

sticky_indexes = []

for series_info in special_indexes.values():
    if series_info.title.startswith("Sticky"):
        sticky_indexes.append(series_info)


# st.markdown(sticky_indexes[0].notes)

st.markdown(
    """The Personal Consumption Expenditures Price Index is a measure of the prices that people living in the United States, or those buying on their behalf, pay for goods and services. The change in the PCE price index is known for capturing inflation (or deflation) across a wide range of consumer expenses and reflecting changes in consumer behavior. For example, if the price of beef rises, shoppers may buy less beef and more chicken.

The PCE Price Index is produced by the Bureau of Economic Analysis (BEA), which revises previously published PCE data to reflect updated information or new methodology, providing consistency across decades of data that's valuable for researchers. The PCE price index is used primarily for macroeconomic analysis and forecasting.

The PCE Price index is the Federal Reserve’s preferred measure of inflation. The PCE Price Index is similar to the Bureau of Labor Statistics' consumer price index for urban consumers. The two indexes, which have their own purposes and uses, are constructed differently, resulting in different inflation rates."""
)

sc = pf.SeriesCollection(series_id=[si.id for si in sticky_indexes])


def _parse_cpi_series_title(title: str) -> str:
    """Function to parse a sticky CPI series title into a human readable label."""
    return title


sticky_long_df = sc.merge_long(col_name=cpi_series_column_name)
dates = get_dates(sticky_long_df, "date")

mtm_pct_chg_df = calc_groupby_pct_chg(
    df=sticky_long_df,
    by=cpi_series_column_name,
    periods=1,
).dropna()

yty_pct_chg_df = calc_groupby_pct_chg(
    df=sticky_long_df,
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
    pd.concat([mtm_bp_df, yty_bp_df])
    .sort_values("sticky_cpi_series")
    .reset_index(drop=True)
)

PLOT_SIZE = {"height": 800, "width": 1400}

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
