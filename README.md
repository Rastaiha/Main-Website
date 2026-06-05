# Rasta Main Website (رستایی‌ها)

Rasta Main Website is a Django-based web application developed for **Rastaiha** (رستایی‌ها), a student-led educational community dedicated to producing interactive educational content and promoting collaborative learning among students.

---

## 🚀 Features

- **Blog & Comments:** Fully-fledged blogging system with Jalali date support, rich-text uploading, and hierarchical comment replies.
- **Events Management:** Organizes and showcases community events, featuring an automated image-resizing pipeline for event posters.
- **URL Shortener:** Built-in lightweight link shortener mapping shortened hashes to long URLs.
- **Newsletter Subscription:** Automated newsletter subscriptions with asynchronous email dispatching powered by Celery.
- **Members Directory:** Displays community terms, members, education details, and visible/hidden profile images.
- **Dynamic SSL Reverse Proxy:** Custom Nginx container supporting both Let's Encrypt Certbot challenge and manual Wildcard SSL certificates.

---

## 🛠️ Tech Stack

- **Framework:** Django 3.1.5 (Python 3.8)
- **Database:** PostgreSQL 15 & SQLite (for dev)
- **Message Broker:** Redis 7
- **Task Queue:** Celery 5.2.7
- **Reverse Proxy:** Nginx 1.25 (Alpine)
- **Deployment:** Docker & Docker Compose
- **CI/CD:** GitHub Actions (compiling and pushing to GHCR)
- **UI Framework:** Semantic UI (RTL Version) & Vanilla CSS

---

## ⚙️ Project Structure

```
├── .github/workflows/      # GitHub Actions CI/CD workflows
├── Rasta_Web/              # Main configuration app (settings, celery, urls)
│   └── settings/           # Base, Development, and Production settings
├── apps/                   # Application-specific Django apps
│   ├── blog/               # Blog system (Posts, Categories, Comments)
│   ├── contact_us/         # User feedback forms
│   ├── doc/                # Generic document manager
│   ├── events/             # Events organization
│   ├── intro/              # Homepage content & featured events
│   ├── members/            # Term-based members directory
│   ├── newsletter/         # Subscriptions & Celery tasks
│   └── shortener/          # MD5-based URL shortener
├── nginx/                  # Nginx Dockerfile and custom entrypoint configurations
├── templates/              # Base HTML and global layouts
├── Dockerfile              # Web application Dockerfile (Slim Debian)
├── docker-compose.yml      # Multi-container orchestrator configuration
├── env.example             # Template file for environment variables
└── manage.py               # Django management utility
```

---

## 📦 Getting Started with Docker

### Prerequisites
Make sure you have [Docker](https://docs.docker.com/get-docker/) and [Docker Compose](https://docs.docker.com/compose/install/) installed.

### 1. Configure Environment Variables
Copy the template configuration file:
```bash
cp env.example .env
```
Open the `.env` file and configure your settings (such as database credentials, domain names, and Django secret keys).

### 2. Run the Stack
Build and start the containers in detached mode:
```bash
docker-compose up -d --build
```
On startup:
1. The database and Redis containers spin up.
2. The web application waits for PostgreSQL availability.
3. Django migrations automatically apply.
4. Static files are collected into `/app/staticfiles`.
5. The development server starts listening on `http://localhost:80` (handled by Nginx).

To stop the application completely:
```bash
docker-compose down
```

---

## 🔒 SSL Configurations (Nginx)

This stack supports two automated SSL termination modes configured dynamically via `.env`:

### Option A: Certbot (Let's Encrypt)
1. In `.env`, set `SSL_TYPE=certbot` and set your `DOMAIN_NAME` and `CERTBOT_EMAIL`.
2. Start the stack:
   ```bash
   docker-compose up -d
   ```
3. Generate the initial certificate (run this once):
   ```bash
   docker compose run --rm certbot certonly --webroot --webroot-path=/var/www/certbot --email $CERTBOT_EMAIL --agree-tos --no-eff-email -d yourdomain.com
   ```
4. Restart Nginx to load the newly created SSL certificates:
   ```bash
   docker compose restart nginx
   ```

### Option B: Custom / Wildcard SSL
1. Base64-encode your certificate and private key files on your terminal:
   ```bash
   cat wildcard.crt | base64 | tr -d '\n'
   cat wildcard.key | base64 | tr -d '\n'
   ```
2. In your `.env`, set `SSL_TYPE=custom` and paste the base64 strings into `SSL_CERT_CONTENT_B64` and `SSL_KEY_CONTENT_B64`.
3. Restart the stack:
   ```bash
   docker-compose down && docker-compose up -d
   ```
   *At startup, Nginx will decode these back into certificate files inside the container and spin up secured HTTPS on port 443.*

---

## 🔄 CI/CD & GitHub Actions

A GitHub Action is configured under [.github/workflows/docker-publish.yml](.github/workflows/docker-publish.yml). 

Whenever you push to the `main` branch or release a tag matching `v*.*.*`, it will:
1. Build the Slim Debian Web image and Nginx image.
2. Publish them to the **GitHub Container Registry (GHCR)** at `ghcr.io/<your-github-username>/rasta-main-website-web` and `nginx`.
3. Utilize caching (`type=gha`) to ensure that subsequent pipeline runs compile in seconds.
