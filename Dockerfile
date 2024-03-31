FROM python:3.9-slim

RUN apt-get update && apt-get install -y \
    build-essential \
    libssl-dev \
    libffi-dev \
    libxml2-dev \
    libxslt1-dev \
    zlib1g-dev \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip install poetry

WORKDIR /app
COPY . /app
RUN poetry config virtualenvs.create false && poetry install --no-dev

CMD ["python", "main.py"]

