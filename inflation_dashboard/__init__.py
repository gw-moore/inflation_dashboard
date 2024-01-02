from functools import lru_cache
from typing import List

import pyfredapi as pf
import streamlit as st


def add_sidebar_title():
    st.markdown(
        """
        <style>
            [data-testid="stSidebarNav"]::before {
                content: "U.S. Inflation Dashboard";
                margin-left: 20px;
                margin-top: 20px;
                font-size: 30px;
                position: relative;
                top: 50px;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


all_cpi_series = pf.get_category_series("9")
all_personal_income_and_outlays_series = pf.get_category_series("110")

cpi_series_column_name = "cpi_series"
cpi_series = [
    "CPIAUCSL",
    "CPIUFDSL",
    "CUSR0000SAF11",
    "CUSR0000SEFV",
    "CPIENGSL",
    "CUSR0000SETB01",
    "CUUR0000SEHE",
    "CUSR0000SEHF",
    "CUSR0000SACE",
    "CUSR0000SEHF01",
    "CUSR0000SEHF02",
    "CPILFESL",
    "CUSR0000SACL1E",
    "CUSR0000SETA01",
    "CUSR0000SETA02",
    "CPIAPPSL",
    "CUUR0000SAM1",
    "CUSR0000SASLE",
    "CPIMEDSL",
    "CUSR0000SEEA",
    "CUSR0000SEEB",
    "CUSR0000SEHA",
    "CUSR0000SEHC",
]


def _parse_cpi_series_title(title: str) -> str:
    """Function to parse a CPI series title into a human readable label."""
    return (
        title.lower()
        .replace("consumer price index for all urban consumers: ", "")
        .replace(" in u.s. city average", "")
        .capitalize()
    )


inflation_sc = pf.SeriesCollection(series_id=cpi_series, rename=_parse_cpi_series_title)
inflation_long_df = inflation_sc.merge_long(col_name=cpi_series_column_name)
inflation_wide_df = inflation_sc.merge_asof(base_series_id="CPIAUCSL")
