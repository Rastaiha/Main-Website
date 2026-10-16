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

# Nginx serves /app/staticfiles. Include collected assets in the image so they
# are present even when a deployment starts supervisord without the entrypoint.
RUN DJANGO_SETTINGS_MODULE=Rasta_Web.settings.production \
    python3 manage.py collectstatic --no-input --clear \
    && test -f /app/staticfiles/images/background.jpeg \
    && test -f /app/staticfiles/images/logo_darkblue.png

# nginx + supervisor configuration for the combined process.
COPY nginx/app.conf /etc/nginx/conf.d/app.conf
COPY supervisord.conf /etc/supervisord.conf

# nginx is the public entrypoint; gunicorn stays on loopback inside the container.
EXPOSE 80

# entrypoint.prod.sh waits for the DB, runs migrate + collectstatic, then execs CMD.
ENTRYPOINT ["/app/entrypoint.prod.sh"]
CMD ["supervisord", "-c", "/etc/supervisord.conf"]
