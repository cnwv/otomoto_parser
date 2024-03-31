# Указываем базовый образ, содержащий Python и все необходимые зависимости
FROM python:3.9-slim

# Устанавливаем необходимые инструменты для работы с MongoDB
RUN apt-get update && apt-get install -y \
    build-essential \
    libssl-dev \
    libffi-dev \
    libxml2-dev \
    libxslt1-dev \
    zlib1g-dev \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем Poetry
RUN pip install poetry

# Копируем файлы проекта и устанавливаем зависимости
WORKDIR /app
COPY . /app
RUN poetry config virtualenvs.create false && poetry install --no-dev

# Запускаем парсер Scrapy
CMD ["python", "main.py"]

