from pathlib import Path

import pyfredapi as pf
from rich.console import Console

console = Console()

cpi_series = [
    "CPIAUCSL",
    "CPIUFDSL",
    "CUSR0000SAF11",
    "CUSR0000SEFV",
    "CPIENGSL",
    "CUSR0000SETB01",
    "CUUR0000SEHE",
    "CUSR0000SEHF",
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

series_column_name = "cpi_series"


def parse_title(title: str) -> str:
    """Function to parse a CPI series title into a human readable label."""
    return (
        title.lower()
        .replace("consumer price index for all urban consumers: ", "")
        .replace(" in u.s. city average", "")
        .capitalize()
    )


def main():
    """Collect CPI data from FRED."""

    data_path = str(Path(__file__).resolve().parent) + "/src/data/cpi/"

    cpi_sc = pf.SeriesCollection()
    cpi_sc.add_series(series_ids=cpi_series, rename=parse_title)

    long_df = cpi_sc.merge_long(col_name=series_column_name)
    wide_df = cpi_sc.merge_asof(base_series_id="CPIAUCSL")

    long_df.to_csv(data_path + "long_df.csv", index=False)
    wide_df.to_csv(data_path + "wide_df.csv", index=False)


if __name__ == "__main__":
    main()
