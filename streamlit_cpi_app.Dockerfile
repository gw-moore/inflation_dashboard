FROM python:3.11-slim
COPY ./requirements.txt ./requirements.txt
RUN pip install -r requirements.txt
COPY . ./
RUN pip install .
# CMD streamlit run inflation_dashboard/streamlit/app.py
EXPOSE 8050
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health
ENTRYPOINT ["streamlit", "run", "inflation_dashboard/streamlit/CPI_All_Urban_Consumers.py.py", "--server.port=8050", "--server.address=0.0.0.0"]
