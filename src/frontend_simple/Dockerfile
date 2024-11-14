FROM node:14.9.0-buster-slim

# Update baseline and ensure we don't run the app as root.
RUN set -ex; \
    apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y --no-install-recommends openssl && \
    npm install -g http-server && \
    useradd -ms /bin/bash app -d /home/app -G sudo -u 2000 -p "$(openssl passwd -1 Passw0rd)" && \
    mkdir -p /app && \
    chown app:app /app

# Expose port for HTTP server
EXPOSE 8080

# Set user and working directory
USER app
WORKDIR /app

# Copy static files to container
ADD --chown=app:app . /app

# Start HTTP server automatically on container start
CMD ["http-server", "-p", "8080"]