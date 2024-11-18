# Use the official Debian-hosted Python image
FROM python:3.11-slim-bookworm

# Required arguments and environment settings
ARG DEBIAN_PACKAGES="build-essential git screen vim"
ENV DEBIAN_FRONTEND=noninteractive
ENV LANG=C.UTF-8
ENV PYENV_SHELL=/bin/bash
ENV PYTHONUNBUFFERED=1

# Update system, install dependencies, and create non-root user
RUN set -ex; \
    for i in $(seq 1 8); do mkdir -p "/usr/share/man/man${i}"; done && \
    apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y --no-install-recommends $DEBIAN_PACKAGES && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    pip install --no-cache-dir --upgrade pip && \
    pip install pipenv && \
    useradd -ms /bin/bash app -d /home/app -u 1000 -p "$(openssl passwd -1 Passw0rd)" && \
    mkdir -p /app /persistent && \
    chown app:app /persistent /app

# Set user to avoid running the app as root and set working directory
USER app
WORKDIR /app

# Install Python packages using Pipfile and Pipfile.lock
ADD --chown=app:app Pipfile Pipfile.lock /app/
RUN pipenv sync

# Add source code for the application
ADD --chown=app:app . /app

# Expose port for API service
EXPOSE 9000

# Start the application
ENTRYPOINT ["/bin/bash", "./docker-entrypoint.sh"]