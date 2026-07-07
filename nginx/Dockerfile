# ---- Stage 1: collect static files from the application image ----
# Reuses the already-built web image so the app code & deps are available.
ARG WEB_IMAGE=ghcr.io/rastaiha/main-website-web:main
FROM ${WEB_IMAGE} AS static

# collectstatic does not touch the database. Use production settings so
# STATIC_ROOT resolves to /app/staticfiles (WORKDIR is /app).
ENV DJANGO_SETTINGS_MODULE=Rasta_Web.settings.production
RUN python manage.py collectstatic --no-input --clear

# ---- Stage 2: nginx image with the static files baked in ----
FROM nginx:1.25-alpine

# Served by the `location /static/ { alias /var/www/static/; }` block.
COPY --from=static /app/staticfiles /var/www/static

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
