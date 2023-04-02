import datetime
from dataclasses import dataclass
from typing import List, Union

import pandas as pd
from dateutil.relativedelta import relativedelta
from IPython.display import display


@dataclass
class Date:
    min: datetime.date
    max: datetime.date


def get_dates(df: pd.DataFrame, date_col: str = "date") -> Date:
    """Get minimum and date from pandas date column

    Parameters
    ----------
    df : pd.DataFrame
        Pandas dataframe.
    date_col : str, optional
        Date column. Defaults to "date"

    Returns
    -------
    Date class. The date class as the attributes min_date & max_date.
    Both are datetime.date.
    """
    min_date = df[[date_col]].min().date.date()
    max_date = df[[date_col]].max().date.date()

    return Date(min=min_date, max=max_date)


def calc_pct_chg_for_latest_obv(
    df: pd.DataFrame,
    periods: List[int],
    series_col: str,
    value_col: str = "value",
    date_col: str = "date",
    period_col: str = "lag",
) -> pd.DataFrame:
    """Calculate the percent change the for given periods and extracts the latest observation
    into a new dataframe.

    For example, suppose you have CPI data and want to calculate the percent change in the latest
    print from 1-month ago, 6-months ago, 12-months ago, and 24-months ago.

    Parameters
    ----------
    df : pd.DataFrame
        A long pandas dataframe.
    periods : List[int]
        The periods to calculate percent change.
    series_col : str
        Name of the column holding the series labels.
    value_col : str, optional
        Name of the column holding the series values. Defaults to "value"
    date_col : str, optional
        Name of the dates column. Defaults to 'date'
    period_col : str, optional
        Name to give the column representing the period for the percent change.
        Defaults to "lag".

    Returns
    -------
    Pandas dataframe.
    """
    dates = get_dates(df=df)
    max_date = dates.max

    df = df.set_index(date_col)
    pct_chg_dfs = []
    for lag in periods:
        pct_chg_df = calc_groupby_pct_chg(
            df=df,
            by=series_col,
            periods=lag,
            value_col=value_col,
        )

        pct_chg_df = round(
            pct_chg_df.groupby(series_col, sort=False, group_keys=True).tail(1), 4
        )

        pct_chg_df["vs_date"] = pd.to_datetime(max_date - relativedelta(months=lag))
        pct_chg_df["lag"] = lag
        pct_chg_df[period_col] = lag
        pct_chg_dfs.append(pct_chg_df)

    pct_chg_df = pd.concat(pct_chg_dfs)
    pct_chg_df = pct_chg_df.reset_index()
    return pct_chg_df.dropna()


def calc_groupby_pct_chg(
    df: pd.DataFrame,
    by: Union[str, List[str]],
    periods: int = 1,
    value_col: str = "value",
) -> pd.DataFrame:
    """Calculate a group by percent change. Useful when calculating a percent change
    on a long dataframe.


    Parameters
    ----------
    df : pd.DataFrame
        A long pandas dataframe.
    by :
        Columns to group by.
    periods : int
        Periods to shift for forming percent change.
    value_col : str
        Column to calculate percent change on.

    Return
    -------
    pd.DataFrame
    """
    pct_chg_df = df.copy()
    pct_chg_df[f"pct_chg_{value_col}"] = (
        pct_chg_df.groupby(by, sort=False, group_keys=True)[value_col]
        .apply(lambda x: x.pct_change(periods))
        .to_numpy()
    )

    return pct_chg_df.dropna()


def pivot_pct_chg_tbl(
    df: pd.DataFrame,
    index_col: str,
    pct_chg_col: str = "pct_chg_value",
    date_col: str = "date",
    n: Union[int, str] = 6,
    other_cols: List[str] = None,
) -> pd.DataFrame:
    """Pivot a percent change dataframe. Designed to work with the `calc_groupby_pct_chg` and
    `calc_pct_chg_for_latest_obv` functions.

    Parameters
    ----------
    df : pd.DataFrame
        Pandas dataframe.
    index_col : str
        Column to make the index.
    pct_chg_col : str
        Name of the percent change column.
    date_col : str, optional
        Name of the date column. Defaults to date.
    n : int | str, optional
        Number of periods to show in pivot table. Defaults to 6.
        Accepts positive in or "all".
    other_cols : List[str]
        Other columns to include in the pivot table header.

    Returns
    -------
    pd.DataFrame
        Pandas pivot table.
    """
    pv_df = df.copy()
    pv_df["Date"] = pv_df[date_col].dt.strftime("%b %Y")

    if n == "all":
        pv_dates = pv_df["Date"].tolist()
        pv_dates = sorted(list(set(pv_dates)))
    else:
        pv_dates = pv_df["Date"].tail(n).tolist()

    pv_df = pv_df.loc[pv_df["Date"].isin(pv_dates)]

    columns = ["Date"]
    if isinstance(other_cols, list):
        for col in other_cols:
            pv_df = pv_df.rename(columns={col: col.replace("_", " ").title()})
        columns = columns + [c.replace("_", " ").title() for c in other_cols]
    pivot_table = pd.pivot_table(
        pv_df,
        index=index_col,
        values=pct_chg_col,
        columns=columns,
        sort=False,
    )
    pivot_table.index.name = index_col.replace("_", " ").title()

    return pivot_table


def display_pct_chg_df(df: pd.DataFrame, title: str) -> None:
    """Applies formatting and title to table and displays.

    Designed to used with the `pivot_pct_chg_tbl` function.

    Parameters
    ----------
    df : pd.DataFrame
        Pandas dataframe.
    title : str
        Table title.

    Returns
    -------
    None
    """
    display(
        df.style.format("{:.1%}")
        .set_caption(f"{title}")
        .set_table_styles(
            [
                {
                    "selector": "caption",
                    "props": [
                        ("font-size", "18px"),
                        ("font-weight", "bold"),
                        ("text-align", "center"),
                    ],
                }
            ]
        )
    )


def walkback_to_nearest_date(df, date) -> str:
    """Take a pandas dataframe and returns the date on of before the given date."""
    date_list = [date.to_pydatetime() for date in df.date.tolist()]
    wb_dict = {(date - df_date).days: df_date for df_date in date_list}
    nearest_date = wb_dict[min([days for days in wb_dict.keys() if int(days) > 0])]
    return str(nearest_date.date())
