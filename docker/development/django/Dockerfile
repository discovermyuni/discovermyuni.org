FROM python:3.12-slim-bullseye

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    DEBIAN_FRONTEND=noninteractive

# Create and set the working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libjpeg-dev \
    libpng-dev \
    libffi-dev \
    git \
    libssl-dev \
    gettext \
    dos2unix \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Create virtual environment
RUN python -m venv /venv
ENV PATH="/venv/bin:$PATH"

# Upgrade pip
RUN pip install --upgrade pip

# Copy requirements first for better caching
COPY requirements/ /tmp/requirements/

# Install Python dependencies
RUN pip install -r /tmp/requirements/development.txt

# Add wait-for-it script for database readiness
ADD https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh /wait-for-it.sh
RUN chmod +x /wait-for-it.sh

# Copy project files
COPY . /app/

# Copy entrypoint script
COPY docker/production/django/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Copy start script
COPY docker/development/django/start.sh /start.sh
RUN chmod +x /start.sh

# Normalize line endings to avoid `exec: /start.sh: not found` due to CRLF
RUN dos2unix /entrypoint.sh /start.sh || true

# Set proper permissions
RUN chown -R root:root /app

# Expose port
EXPOSE 8000

# Set entrypoint
ENTRYPOINT ["/entrypoint.sh"]
