#!/bin/sh

# Set defaults
DOMAIN_NAME=${DOMAIN_NAME:-localhost}
SSL_TYPE=${SSL_TYPE:-none}

echo "Starting Nginx entrypoint. SSL_TYPE=${SSL_TYPE}, DOMAIN_NAME=${DOMAIN_NAME}"

# Ensure configuration directory exists
mkdir -p /etc/nginx/conf.d

# Generate config based on SSL_TYPE
if [ "$SSL_TYPE" = "none" ]; then
    echo "Configuring HTTP-only mode..."
    cat <<EOF > /etc/nginx/conf.d/default.conf
server {
    listen 80;
    listen [::]:80;
    server_name ${DOMAIN_NAME};

    location / {
        proxy_pass http://web:8000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
EOF

elif [ "$SSL_TYPE" = "custom" ]; then
    echo "Configuring Custom SSL mode..."
    mkdir -p /etc/nginx/ssl

    # Check if base64 encoded certificate and key are provided in env
    if [ -n "$SSL_CERT_CONTENT_B64" ] && [ -n "$SSL_KEY_CONTENT_B64" ]; then
        echo "Decoding SSL cert and key from environment variables..."
        echo "$SSL_CERT_CONTENT_B64" | base64 -d > /etc/nginx/ssl/custom.crt
        echo "$SSL_KEY_CONTENT_B64" | base64 -d > /etc/nginx/ssl/custom.key
    else
        echo "WARNING: SSL_CERT_CONTENT_B64 or SSL_KEY_CONTENT_B64 is missing!"
        echo "Using default/existing certs if mounted to /etc/nginx/ssl/custom.crt..."
    fi

    cat <<EOF > /etc/nginx/conf.d/default.conf
server {
    listen 80;
    listen [::]:80;
    server_name ${DOMAIN_NAME};
    return 301 https://\$host\$request_uri;
}

server {
    listen 443 ssl;
    listen [::]:443 ssl;
    server_name ${DOMAIN_NAME};

    ssl_certificate /etc/nginx/ssl/custom.crt;
    ssl_certificate_key /etc/nginx/ssl/custom.key;

    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_prefer_server_ciphers on;
    ssl_ciphers HIGH:!aNULL:!MD5;

    location / {
        proxy_pass http://web:8000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
EOF

elif [ "$SSL_TYPE" = "certbot" ]; then
    echo "Configuring Certbot SSL mode..."
    CERT_PATH="/etc/letsencrypt/live/${DOMAIN_NAME}/fullchain.pem"
    KEY_PATH="/etc/letsencrypt/live/${DOMAIN_NAME}/privkey.pem"

    if [ ! -f "$CERT_PATH" ]; then
        echo "Certificates not found at ${CERT_PATH}. Starting in HTTP-challenge mode first..."
        cat <<EOF > /etc/nginx/conf.d/default.conf
server {
    listen 80;
    listen [::]:80;
    server_name ${DOMAIN_NAME};

    location /.well-known/acme-challenge/ {
        root /var/www/certbot;
    }

    location / {
        return 503 "Nginx is waiting for Certbot to request the certificate. Please run Certbot.";
    }
}
EOF
    else
        echo "Certificates found! Enabling full HTTPS configuration..."
        cat <<EOF > /etc/nginx/conf.d/default.conf
server {
    listen 80;
    listen [::]:80;
    server_name ${DOMAIN_NAME};
    
    location /.well-known/acme-challenge/ {
        root /var/www/certbot;
    }

    location / {
        return 301 https://\$host\$request_uri;
    }
}

server {
    listen 443 ssl;
    listen [::]:443 ssl;
    server_name ${DOMAIN_NAME};

    ssl_certificate ${CERT_PATH};
    ssl_certificate_key ${KEY_PATH};

    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_prefer_server_ciphers on;
    ssl_ciphers HIGH:!aNULL:!MD5;

    location / {
        proxy_pass http://web:8000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
EOF
    fi
fi

echo "Nginx configuration generated. Starting Nginx..."
exec nginx -g "daemon off;"
