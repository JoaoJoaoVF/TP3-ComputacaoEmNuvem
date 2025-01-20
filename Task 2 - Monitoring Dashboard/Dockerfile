FROM python:3.9-slim

WORKDIR /app

COPY dashboard.py /app/dashboard.py

COPY requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8703

CMD ["streamlit", "run", "dashboard.py", "--server.port=8703", "--server.address=0.0.0.0"]
