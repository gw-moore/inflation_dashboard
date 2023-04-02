# Inflation Dashboard

Dashboard of American Inflation Data.

## Setup

- Set your FRED API key in a `.env` file

## Launch dashboards

### Dash Dashboard

Launch the dashboard with Docker

```bash
docker build -t dash_inflation_app -f dash_app.Dockerfile .
docker run -p 8050:8050 dash_inflation_app
```

Launch the dashboard directly with Python

```bash
❯ python inflation_dashboard/dash/app.py
```