#Versão do Python
FROM python:3.12-slim

#Impede que o Python gere arquivo .pyc e permite logs em tempo real
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

#Instala dependências do sistema
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    libssl-dev \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

#Instala as dependências do projeto
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

#Copia o restante do código
COPY . .

#Expõe a porta da aplicação
EXPOSE 8000

#Comando para iniciar a aplicação
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]