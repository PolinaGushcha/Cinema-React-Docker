FROM python:3.11 AS builder
WORKDIR /app
ADD pyproject.toml poetry.lock /app/

RUN apt-get update && apt-get install -y build-essential libffi-dev libgeos-dev ssh
RUN pip install poetry
RUN poetry config virtualenvs.in-project true
RUN --mount=type=ssh poetry install --no-ansi

# ---

FROM python:3.11-slim
WORKDIR /app

COPY --from=builder /app /app
ENV VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH"


ADD . /app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "1000", "--log-config=./log_conf.yaml"]