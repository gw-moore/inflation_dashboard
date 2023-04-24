# Inflation Dashboard

This project is exploration of different dashboard tools in the Python ecosystem.

The data used is the U.S. Consumer Price Index published by the Bureau of Labor Statistic. The data is sourced Federal Reserve Economic Data (FRED) API with the [pyfredapi](https://github.com/gw-moore/pyfredapi) package.

## Setup

- Set your FRED API key in a `.env` file

```
FRED_API_KEY="your-api-key"
```

## Launch Dashboard

### Streamlit Dashboard

![alt text](_static/streamlit_example.png)
*Streamlit Dashboard*

Launch the dashboard with Streamlit

```bash
streamlit run inflation_dashboard/streamlit/app.py
```

Launch the dashboard with Docker

```bash
docker build -t streamlit_cpi_app -f streamlit_cpi_app.Dockerfile .
docker run -p 8050:8050 streamlit_cpi_app
```


### Dash Dashboard

Launch the dashboard with Python

```bash
python inflation_dashboard/dash/app.py
```

Launch the dashboard with Docker

```bash
docker build -t dash_cpi_app -f dash_cpi_app.Dockerfile .
docker run -p 8051:8051 dash_inflation_app
```
