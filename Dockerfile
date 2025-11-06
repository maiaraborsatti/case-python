# Dockerfile para Sistema de Coleta e Processamento de Dados
# Python 3.11 slim para reduzir tamanho da imagem

FROM python:3.11-slim

# Metadados da imagem
LABEL maintainer="Sistema de Avaliação Técnica"
LABEL version="2.0.0"
LABEL description="Sistema de coleta e processamento de dados de APIs públicas"

# Variáveis de ambiente
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Define diretório de trabalho
WORKDIR /app

# Instala dependências do sistema necessárias
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copia apenas requirements primeiro (cache de layers do Docker)
COPY requirements.txt .

# Instala dependências Python
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código da aplicação
COPY . .

# Cria diretório para dados de saída
RUN mkdir -p /app/data && \
    chmod 755 /app/data

# Define variáveis de ambiente padrão da aplicação
ENV APP_ENV=production \
    LOG_LEVEL=INFO \
    PYTHONPATH=/app

# Expõe porta (caso futuramente adicione API REST)
EXPOSE 8000

# Health check (verifica se a aplicação está respondendo)
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import sys; sys.exit(0)"

# Volume para persistência de dados
VOLUME ["/app/data"]

# Comando padrão de execução
CMD ["python", "app/main.py"]

