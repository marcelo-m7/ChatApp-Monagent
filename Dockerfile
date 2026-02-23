FROM python:3.11-slim

# Cria diretório de trabalho
WORKDIR /app

# Copia arquivo de dependências e instala
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copia a aplicação
COPY app/ ./app/
COPY README.md ./README.md

# Expõe a porta onde o Uvicorn irá rodar
EXPOSE 8000

# Comando para iniciar a API
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]