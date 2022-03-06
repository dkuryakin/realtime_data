FROM python:3.9-alpine

WORKDIR /app

RUN apk add --no-cache gcc musl-dev libffi-dev && pip install --no-cache-dir poetry==1.1.13

COPY poetry.lock .
COPY pyproject.toml .

RUN poetry install

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY src/ /app/
COPY entrypoint.sh .

ENTRYPOINT ["sh", "entrypoint.sh"]