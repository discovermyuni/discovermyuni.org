# ---- Builder ----
FROM python:3.12-bookworm AS builder
RUN apt-get update && \
    apt-get install --no-install-recommends -y pipx curl libpq-dev gcc && \
    rm -rf /var/lib/apt/lists/*
ENV PATH="/root/.local/bin:${PATH}"
RUN pipx install poetry && pipx inject poetry poetry-plugin-bundle

WORKDIR /src
COPY pyproject.toml poetry.lock* ./
RUN poetry bundle venv --python=/usr/bin/python3 --only=main /venv
COPY . .

# ---- Final ----
FROM python:3.12-slim-bookworm AS final
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH="/venv/bin:${PATH}"

# psycopg2 deps
RUN apt-get update && \
    apt-get install --no-install-recommends -y libpq5 curl && \
    rm -rf /var/lib/apt/lists/*

# create non-root user
RUN useradd -m django
WORKDIR /app
COPY --from=builder /venv /venv
COPY --chown=django:django --from=builder /src /app
USER django

RUN python manage.py collectstatic --noinput

HEALTHCHECK CMD curl --fail http://localhost:8000/health/ || exit 1