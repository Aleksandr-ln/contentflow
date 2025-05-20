
![Django](https://img.shields.io/badge/Django-4.x-brightgreen)
![Python](https://img.shields.io/badge/Python-3.11-blue)
![Coverage](https://img.shields.io/badge/Coverage-94%25-brightgreen)
![License](https://img.shields.io/badge/License-MIT-lightgrey)
![Status](https://img.shields.io/badge/Status-Production--ready-success)

## Table of Contents
- [Features](#features)
- [Functionality Overview](#functionality-overview)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [UML Class Diagram](#uml-class-diagram)
- [Local Development & Testing](#local-development--testing)
- [Frontend Testing](docs/frontend-testing.md)
- [Storage Configuration (S3 + CloudFront)](#storage-configuration-s3--cloudfront)
- [Security Configuration (Production)](#security-configuration-production)
- [Deployment Guide (Production)](#deployment-guide-production)
- [Author](#author)

# ContentFlow - Social Media Django Application

A production-ready social media-like web application built with Django, supporting user profiles, posts with images, hashtags, likes, and interactive feed browsing.

---

## Features

- User registration & profile management
- Post creation with multiple images & hashtags
- Responsive feed & tag filtering
- AJAX-based like system
- Media storage via AWS S3 & CloudFront
- Secure production deployment with NGINX & Gunicorn
- Local time conversion for posts
- Frontend unit tests (Jest)
- Backend tests with coverage reports

See [Architecture Overview](docs/architecture.md/#functional-highlights) for in-depth functionality breakdown.

---

## Tech Stack

- Python 3.11
- Django 4.x
- SQLite (dev) / PostgreSQL (prod-ready structure)
- AWS S3 / EC2 / RDS / CloudFront
- Gunicorn / NGINX
- Bootstrap / Vanilla JS
- Jest (frontend testing) / Pytest / Coverage

---

## Project Structure

```
project-root/
├── contentflow/            # Django settings, URLs, WSGI, S3 storage config
├── core/                   # Base views (e.g., home)
├── users/                  # Custom user model, profile logic
├── posts/                  # Posts, images, hashtags
├── likes/                  # AJAX like handling
├── seed/                   # Fake data generator (management command)
├── templates/              # HTML templates
├── static/js/              # Frontend logic (like-toggle, modal, etc.)
├── tests/                  # Backend unit tests
│   └── frontend/           # Frontend unit tests (Jest)
├── media/                  # Uploaded media files (in DEBUG mode)
├── docs/                   # UML diagram and project description
├── manage.py               # Django management CLI
├── jest.config.js          # Jest configuration
├── babel.config.js         # Babel config for ES6 support
├── requirements.txt        # Python dependencies
└── README.md
```

## UML Class Diagram

This diagram illustrates the relationship between core models (`User`, `Post`, `Like`, `Image`, `Tag`).

See model relationships in the [Architecture Overview](docs/architecture.md#uml-class-diagram)

## Local Development & Testing

### Local Setup

```
git clone https://git.foxminded.ua/foxstudent107874/task-12-create-basic-application.git
cd task-12-create-basic-application
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Create .env file for Local Development based on .env.example:

```
DEBUG=True
SECRET_KEY=your-secret-key
EMAIL_HOST=your-smtp-host (e.g., sandbox.smtp.mailtrap.io)
EMAIL_HOST_USER=your-mailtrap-username
EMAIL_HOST_PASSWORD=your-mailtrap-password
EMAIL_PORT=2525
EMAIL_USE_TLS=True
DEFAULT_FROM_EMAIL=noreply@contentflow.com
ALLOWED_HOSTS=127.0.0.1,localhost
```

## Database Setup & Migrations

```
python manage.py migrate
```

## (Optional) Fake Data Management: `seed_data` Command

This project includes a custom Django management command to generate and reset fake users, posts, images, and tags.

### Usage

```
python manage.py seed_data                      # Create 5 fake users (default)
python manage.py seed_data --count 10           # Create 10 users
python manage.py seed_data --clear              # Remove all fake data
python manage.py seed_data --clear --count 15   # Reset fake data
```

Created:

- Users: user0@example.com, user1@...
- All fake users created with password: password1234
- Posts: Each with caption, tags, and up to 5 images
- Tags: Extracted from captions
- Thumbnails: Auto-generated from images

Learn more about the logic behind this command in the [Architecture Overview](docs/architecture.md/#fake-data-generation).

## Run the development Server

```
python manage.py runserver
```

## Open the app in your browser
```
http://127.0.0.1:8000
```

## Running Backend Tests
### Ensure the environment is activated and run:

```
coverage run -m pytest tests
coverage report -m
```

## Frontend Tests

This project uses [Jest](https://jestjs.io/) to test interactive frontend features (e.g. like-toggle, modal gallery).

Basic command:

```
npm install
npm run test -- --coverage
```

Full guide: [docs/frontend-testing.md](docs/frontend-testing.md)

---

## Storage Configuration (S3 + CloudFront)

This project supports local storage in development and AWS S3 + CloudFront in production.

For detailed storage classes, S3/CloudFront integration, and environment mapping, see: 
[Architecture Overview](docs/architecture.md/#s3--cloudfront-configuration)

### Database Configuration

The project uses **PostgreSQL** in production.  
You can configure connection settings via `.env`:

```
DB_NAME=your-db-name
DB_USER=your-db-user
```

In local development, SQLite is supported as a fallback by modifying settings.py.

See [Architecture Overview](docs/architecture.md/#database--storage-settings-in-settingspy) for detailed settings structure.

---

## Security Configuration (Production)

Django security features activated when `DEBUG=False`:

- `SECURE_SSL_REDIRECT`
- `CSRF_COOKIE_SECURE`, `SESSION_COOKIE_SECURE`
- `SECURE_HSTS_SECONDS`, `SECURE_HSTS_PRELOAD`
- `SECURE_PROXY_SSL_HEADER`

These are defined in `settings.py` and complemented by HTTPS enforcement in `nginx.conf`.

For detailed explanations and configuration examples, see [Architecture Overview](docs/architecture.md#security-configuration)

---

## Deployment Guide (Production)

This guide outlines the steps to deploy ContentFlow using AWS EC2, RDS (PostgreSQL), S3 (static/media), CloudFront, NGINX, and Gunicorn.

### Clone and Set Up the Project

```
git clone https://git.foxminded.ua/foxstudent107874/task-12-create-basic-application.git
cd task-12-create-basic-application
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Configure Environment Variables

Use .env.example as a template to create your .env file.

Make sure to include:

- AWS credentials
- Database connection settings
- Email provider config

See full list of environment variables in the [Architecture Overview](docs/architecture.md#configuration--environment)

### Set Up PostgreSQL (RDS)

- Launch a PostgreSQL instance via AWS RDS
- Allow EC2 to connect (security group settings)
- Update .env with DB_HOST, DB_NAME, etc.

Then run migrations:

```
python manage.py migrate
```

### Configure S3 & CloudFront (Static/Media)

Create an S3 bucket and CloudFront distribution

Update .env:

```
AWS_STORAGE_BUCKET_NAME=...
AWS_S3_REGION_NAME=...
AWS_S3_CUSTOM_DOMAIN=your-cloudfront-domain.cloudfront.net
```

Then collect static files:

```
python manage.py collectstatic --noinput
```

### Set Up Gunicorn (systemd)

Start and enable:

```
sudo systemctl daemon-reexec
sudo systemctl start gunicorn
sudo systemctl enable gunicorn
```

### Configure NGINX

- Use contentflow.conf as a base config
- Set proxy to gunicorn.sock
- Configure CloudFront or static fallback as needed

```
sudo ln -s /etc/nginx/sites-available/contentflow.conf /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### Set Up SSL (Let's Encrypt or Self-Signed)

```
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

Or configure self-signed certs (if for testing only).

### Use CloudFront for CDN Delivery

Ensure static/media URLs are delivered via your CloudFront domain for optimal performance.

Example Config Files
- contentflow.conf — NGINX site config
- gunicorn.service — Gunicorn systemd unit
- .env.example — Deployment-ready environment file

## Docker & CI/CD

This project does not currently include Docker support or CI/CD pipelines.

However, the structure is compatible with containerization and automated deployment, and these features can be added in future iterations.

## Author
**Author:** Oleksandr Onupko  
**License:** MIT
