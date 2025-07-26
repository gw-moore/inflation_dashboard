import pyfredapi as pf
import streamlit as st

from inflation_dashboard import add_sidebar_title, all_cpi_series
from inflation_dashboard.utils.pandas import calc_groupby_pct_chg, get_dates
from inflation_dashboard.utils.plotly import _mk_line_plot

st.set_page_config(layout="wide")
add_sidebar_title()
st.markdown("# U.S. Personal Consumption Expenditures Price Index")

series_column_name = "pci_series"

pci_series = [
    s
    for s in all_cpi_series.values()
    if s.title.startswith("Personal Consumption Expenditures:")
]

main_series = [s for s in pci_series if s.id == "PCEPI"][0]

st.markdown(main_series.notes)


sc = pf.SeriesCollection(series_id=[si.id for si in pci_series])

pci_long_df = sc.merge_long(col_name=series_column_name)
dates = get_dates(pci_long_df, "date")

yty_lineplot_df = calc_groupby_pct_chg(
    df=pci_long_df,
    by=series_column_name,
    periods=12,
).dropna()
yty_lineplot_df["type"] = "year-to-year"

yty_line_plot = _mk_line_plot(
    df=yty_lineplot_df,
    title=f"Personal Consumption Expenditures Price Index, 12-Month Percent Change, {dates.min} - {dates.max}",
    series_column_name=series_column_name,
)

st.plotly_chart(yty_line_plot)
