# Usa uma imagem base leve do Python
FROM python:3.9-slim

# Define o diretório de trabalho
WORKDIR /app

# Copia o script da função para o container
COPY serverless_function.py /app/serverless_function.py

# Instala dependências, se houver um arquivo requirements.txt
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt || echo "Nenhum pacote necessário"

# Mantém o container rodando
CMD ["python", "-c", "import time; print('Serverless function container started...'); time.sleep(3600)"]
