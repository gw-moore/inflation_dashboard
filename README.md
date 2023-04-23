# Inflation Dashboard

Dashboard of American Inflation Data.

## Setup

- Set your FRED API key in a `.env` file

```
FRED_API_KEY="your-api-key"
```

## Launch Dashboard

### Dash Dashboard

Launch the dashboard with Docker

```bash
❯ docker build -t dash_inflation_app -f dash_app.Dockerfile .
❯ docker run -p 8050:8050 dash_inflation_app
```

Launch the dashboard with Python

```bash
❯ python inflation_dashboard/dash/app.py
```

### Streamlit Dashboard

Launch the dashboard with Streamlit

```bash
> streamlit run inflation_dashboard/streamlit/app.py
```
