FROM python:latest

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8703

CMD ["streamlit", "run", "serverless-function.py"]