FROM python:3.11-slim
COPY ./requirements.txt ./requirements.txt
RUN pip install -r requirements.txt
COPY . ./
RUN pip install .
CMD gunicorn -b 0.0.0.0:8050 inflation_dashboard.dash.app:server
