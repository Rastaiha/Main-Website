# Stage 1: Build stage
FROM python:3.8-alpine AS builder

# Set environment variables for Python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /usr/src/app

# Install build dependencies
RUN apk add --no-cache \
    build-base \
    gcc \
    musl-dev \
    libc-dev \
    postgresql-dev \
    libffi-dev \
    openssl-dev \
    jpeg-dev \
    zlib-dev \
    libxslt-dev \
    && apk add --no-cache --virtual .build-deps linux-headers

# Upgrade pip and install pip-tools for dependency management
RUN pip install --upgrade pip pip-tools

# Copy requirements file and compile dependencies
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application source code
COPY . .

# Stage 2: Runtime stage
FROM python:3.8-alpine

# Set environment variables for Python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /usr/src/app

# Install runtime dependencies
RUN apk add --no-cache \
    libpq \
    libffi \
    jpeg \
    zlib \
    libxslt

# Copy dependencies from the builder image
COPY --from=builder /usr/src/app /usr/src/app

# Add a non-root user and set permissions
RUN adduser -D -H -u 1001 django \
    && chown -R django /usr/src/app \
    && mkdir -p /usr/src/app/logging /usr/src/app/staticfiles /usr/src/app/media \
    && chown -R django /usr/src/app/logging /usr/src/app/staticfiles /usr/src/app/media

# Switch to non-root user
USER django

# Expose the application port (if applicable)
EXPOSE 8000

# Run the entrypoint script
ENTRYPOINT ["/usr/src/app/entrypoint.prod.sh"]
