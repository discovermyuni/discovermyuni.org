# Build python using poetry then bundle into a venv
FROM python:3.12-bookworm AS builder
RUN apt-get update && \
    apt-get install --no-install-suggests --no-install-recommends --yes pipx curl && \
    apt-get -y install libpq-dev gcc && \
    curl -o /wait-for-it.sh https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh && \
    chmod +x /wait-for-it.sh && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

ENV PATH="/root/.local/bin:${PATH}"
RUN pipx install poetry
RUN pipx inject poetry poetry-plugin-bundle
WORKDIR /src
COPY . .
RUN poetry bundle venv --python=/usr/bin/python3 --only=main /venv


# Add the venv to the final image
FROM python:3.12-slim-bookworm AS final

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH="/venv/bin:${PATH}"

COPY --from=builder /venv /venv

# keep libpq5 for psycopg2
RUN apt-get update && apt-get install -y libpq5 && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY --from=builder /src /app

COPY --from=builder /wait-for-it.sh /wait-for-it.sh
RUN chmod +x /wait-for-it.sh

# copy entrypoint and dev start script
COPY ./compose/production/django/entrypoint.sh /entrypoint.sh
COPY ./compose/local/django/start.sh /start.sh

RUN chmod +x /entrypoint.sh /start.sh

ENTRYPOINT ["/entrypoint.sh"]
