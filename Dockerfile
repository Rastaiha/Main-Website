FROM python:3.8-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# System deps: build toolchain for Python packages, plus nginx + supervisor so
# a single container can run the reverse proxy and the app server together
# (they share a filesystem, which removes the need for a shared static volume).
RUN apt-get update && apt-get install --no-install-recommends -y \
        build-essential \
        curl \
        netcat-openbsd \
        nginx \
        supervisor \
    && \
    apt-get clean && rm -rf /var/lib/apt/lists/* \
    # Send nginx logs to the container's stdout/stderr (like the official image).
    && ln -sf /dev/stdout /var/log/nginx/access.log \
    && ln -sf /dev/stderr /var/log/nginx/error.log \
    # Drop the default site so only our config is active.
    && rm -f /etc/nginx/sites-enabled/default /etc/nginx/conf.d/default.conf

RUN pip install --no-cache-dir --upgrade pip wheel

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# nginx + supervisor configuration for the combined process.
COPY nginx/app.conf /etc/nginx/conf.d/app.conf
COPY supervisord.conf /etc/supervisord.conf

# nginx is the public entrypoint; gunicorn stays on loopback inside the container.
EXPOSE 80

# entrypoint.prod.sh waits for the DB, runs migrate + collectstatic, then execs CMD.
ENTRYPOINT ["/app/entrypoint.prod.sh"]
CMD ["supervisord", "-c", "/etc/supervisord.conf"]
