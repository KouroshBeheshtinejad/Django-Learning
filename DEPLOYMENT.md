# 🚀 Django First Site - Comprehensive Deployment Guide

Complete guide for deploying Django First Site to production environments.

---

## 📋 Table of Contents

1. [Pre-Deployment Checklist](#pre-deployment-checklist)
2. [Local Development Setup](#local-development-setup)
3. [Production Server Setup](#production-server-setup)
4. [Database Configuration](#database-configuration)
5. [Web Server Configuration](#web-server-configuration)
6. [SSL/HTTPS Setup](#sslhttps-setup)
7. [Monitoring & Maintenance](#monitoring--maintenance)
8. [Troubleshooting](#troubleshooting)

---

## ✅ Pre-Deployment Checklist

Before deploying to production, ensure all of the following are completed:

### Security Settings
- [ ] `SECRET_KEY` is unique and stored in `.env` (not in code)
- [ ] `DEBUG = False` in production settings
- [ ] `ALLOWED_HOSTS` is set to your domain(s)
- [ ] `SECURE_SSL_REDIRECT = True` (for HTTPS)
- [ ] `CSRF_COOKIE_SECURE = True`
- [ ] `SESSION_COOKIE_SECURE = True`
- [ ] SSL certificate is installed (Let's Encrypt or paid)
- [ ] HSTS headers are enabled
- [ ] Security headers are configured

### Database & Files
- [ ] Database is migrated: `python manage.py migrate`
- [ ] Static files are collected: `python manage.py collectstatic --noinput`
- [ ] Media directory is writable
- [ ] Database backups are scheduled
- [ ] Log directory exists and is writable

### Application
- [ ] All dependencies are in `requirements.txt`
- [ ] Virtual environment is configured
- [ ] Django security check passes: `python manage.py check --deploy`
- [ ] No hardcoded secrets in code
- [ ] Error logging is configured
- [ ] Email service is configured

### Infrastructure
- [ ] Server firewall is configured
- [ ] SSH keys are properly set up (no password login)
- [ ] Server is fully patched and updated
- [ ] Monitoring is in place (error tracking, uptime)
- [ ] Backup strategy is implemented

---

## 🏠 Local Development Setup

### 1. Clone and Setup
```bash
git clone https://github.com/yourusername/Django_Learning.git
cd Django_Learning
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

### 2. Configure .env
```bash
cp .env.example .env
# Edit .env with local development values
# For development, DEBUG=True is fine
```

### 3. Initialize Database
```bash
python manage.py migrate --settings=First_Site.setting.dev
python manage.py createsuperuser --settings=First_Site.setting.dev
python manage.py collectstatic --noinput --settings=First_Site.setting.dev
```

### 4. Run Development Server
```bash
python manage.py runserver --settings=First_Site.setting.dev
```

Visit `http://localhost:8000` and verify:
- [ ] Homepage loads correctly
- [ ] Admin panel works (`/admin`)
- [ ] Blog functionality works
- [ ] Static files are loading (CSS/JS)

---

## 🖥️ Production Server Setup

### Recommended Server Specs
- Ubuntu 20.04 LTS or higher
- 2GB+ RAM (for small-medium traffic)
- 2+ CPU cores
- 20GB+ disk space
- Static IP address

### Step 1: Initial Server Setup

```bash
# Connect to server
ssh -i your_key.pem ubuntu@your_server_ip

# Update system
sudo apt update && sudo apt upgrade -y

# Install dependencies
sudo apt install -y python3.10 python3.10-venv python3.10-dev
sudo apt install -y postgresql postgresql-contrib postgresql-client
sudo apt install -y nginx
sudo apt install -y supervisor
sudo apt install -y git curl wget htop
sudo apt install -y certbot python3-certbot-nginx
sudo apt install -y redis-server  # Optional, for caching
```

### Step 2: Create Application User
```bash
# Create dedicated user for Django app
sudo useradd -m -s /bin/bash djangoapp
sudo usermod -aG sudo djangoapp

# Switch to djangoapp user
sudo su - djangoapp
```

### Step 3: Clone Repository
```bash
# As djangoapp user
cd ~
git clone https://github.com/yourusername/Django_Learning.git
cd Django_Learning

# Set proper permissions
sudo chown -R djangoapp:djangoapp /home/djangoapp/Django_Learning
```

### Step 4: Setup Python Virtual Environment
```bash
# As djangoapp user
cd /home/djangoapp/Django_Learning
python3.10 -m venv venv
source venv/bin/activate

# Install production dependencies
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
pip install gunicorn whitenoise psycopg2-binary
```

### Step 5: Create Production .env File
```bash
# Create .env with secure values
nano /home/djangoapp/Django_Learning/.env
```

Add the following (replace with your values):
```env
DEBUG=False
ENVIRONMENT=production
SECRET_KEY=YOUR_GENERATED_SECRET_KEY

# Domains
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# Security
SECURE_SSL_REDIRECT=True
CSRF_COOKIE_SECURE=True
SESSION_COOKIE_SECURE=True
SECURE_HSTS_SECONDS=31536000

# Database (configure next step)
DB_ENGINE=django.db.backends.postgresql
DB_NAME=django_db
DB_USER=django_user
DB_PASSWORD=YOUR_SECURE_PASSWORD
DB_HOST=localhost
DB_PORT=5432

# Email
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=YOUR_APP_PASSWORD
DEFAULT_FROM_EMAIL=your-email@gmail.com

# Caching
CACHE_BACKEND=django.core.cache.backends.locmem.LocMemCache
```

Make sure only djangoapp can read it:
```bash
chmod 600 /home/djangoapp/Django_Learning/.env
```

### Step 6: Create Logs Directory
```bash
mkdir -p /home/djangoapp/Django_Learning/logs
chmod 755 /home/djangoapp/Django_Learning/logs
```

---

## 🗄️ Database Configuration

### PostgreSQL Setup

```bash
# Connect as postgres user
sudo -u postgres psql

# In PostgreSQL shell:
CREATE DATABASE django_db;
CREATE USER django_user WITH PASSWORD 'YOUR_SECURE_PASSWORD';

ALTER ROLE django_user SET client_encoding TO 'utf8';
ALTER ROLE django_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE django_user SET default_transaction_deferrable TO 'on';
ALTER ROLE django_user SET timezone TO 'UTC';

GRANT ALL PRIVILEGES ON DATABASE django_db TO django_user;

# Connect to the database and grant schema permissions
\c django_db
GRANT ALL ON SCHEMA public TO django_user;

\q  # Exit PostgreSQL
```

### Run Migrations

```bash
# As djangoapp user
cd /home/djangoapp/Django_Learning
source venv/bin/activate
python manage.py migrate --settings=First_Site.setting.prod --noinput
```

### Create Superuser

```bash
python manage.py createsuperuser --settings=First_Site.setting.prod
# Follow the prompts to create admin account
```

### Collect Static Files

```bash
python manage.py collectstatic --noinput --settings=First_Site.setting.prod
```

---

## 🌐 Web Server Configuration

### Gunicorn Setup

Create a systemd service file for Gunicorn:

```bash
sudo nano /etc/systemd/system/gunicorn.service
```

Add the following:
```ini
[Unit]
Description=Gunicorn application server for Django
After=network.target
Documentation=https://gunicorn.org

[Service]
Type=notify
User=djangoapp
Group=www-data
WorkingDirectory=/home/djangoapp/Django_Learning
Environment=DJANGO_SETTINGS_MODULE=First_Site.setting.prod
ExecStart=/home/djangoapp/Django_Learning/venv/bin/gunicorn \
    --workers 3 \
    --worker-class sync \
    --bind unix:/home/djangoapp/Django_Learning/gunicorn.sock \
    --timeout 120 \
    --access-logfile /home/djangoapp/Django_Learning/logs/access.log \
    --error-logfile /home/djangoapp/Django_Learning/logs/error.log \
    --log-level info \
    First_Site.wsgi:application

Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start Gunicorn:
```bash
sudo systemctl daemon-reload
sudo systemctl enable gunicorn
sudo systemctl start gunicorn
sudo systemctl status gunicorn
```

### Nginx Configuration

Create Nginx configuration:

```bash
sudo nano /etc/nginx/sites-available/django_app
```

Add the following (replace yourdomain.com with your domain):
```nginx
upstream gunicorn {
    server unix:/home/djangoapp/Django_Learning/gunicorn.sock fail_timeout=0;
}

# Redirect HTTP to HTTPS
server {
    listen 80;
    listen [::]:80;
    server_name yourdomain.com www.yourdomain.com;
    
    # Allow Let's Encrypt validation
    location /.well-known/acme-challenge/ {
        root /var/www/certbot;
    }
    
    # Redirect all other traffic to HTTPS
    location / {
        return 301 https://$server_name$request_uri;
    }
}

# HTTPS server block
server {
    listen 443 ssl http2;
    listen [::]:443 ssl http2;
    server_name yourdomain.com www.yourdomain.com;
    
    # SSL Certificates (set after Let's Encrypt)
    # ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    # ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;
    
    # SSL Configuration
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 10m;
    
    # Security Headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-Frame-Options "DENY" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;
    add_header Permissions-Policy "geolocation=(), microphone=(), camera=()" always;
    
    # Logging
    access_log /var/log/nginx/django_access.log combined buffer=32k flush=5s;
    error_log /var/log/nginx/django_error.log warn;
    
    client_max_body_size 10M;
    
    # Static files (long cache)
    location /static/ {
        alias /home/djangoapp/Django_Learning/staticfiles/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }
    
    # Media files (moderate cache)
    location /media/ {
        alias /home/djangoapp/Django_Learning/media/;
        expires 7d;
        add_header Cache-Control "public";
    }
    
    # Proxy to Gunicorn
    location / {
        proxy_pass http://gunicorn;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
        proxy_buffering off;
        proxy_request_buffering off;
        
        # Timeouts for long-running requests
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }
    
    # Deny access to sensitive files
    location ~ /\. {
        deny all;
    }
    location ~ ~$ {
        deny all;
    }
}
```

Enable the Nginx configuration:
```bash
# Remove default config
sudo rm -f /etc/nginx/sites-enabled/default

# Enable our config
sudo ln -s /etc/nginx/sites-available/django_app /etc/nginx/sites-enabled/

# Test Nginx configuration
sudo nginx -t

# Restart Nginx
sudo systemctl restart nginx
```

---

## 🔒 SSL/HTTPS Setup

### Install Let's Encrypt Certificate

```bash
# Install Certbot
sudo apt install -y certbot python3-certbot-nginx

# Request certificate (first update Nginx config without SSL lines above)
sudo certbot certonly --webroot \
    -w /var/www/certbot \
    -d yourdomain.com \
    -d www.yourdomain.com \
    --non-interactive \
    --agree-tos \
    --email your-email@gmail.com

# Certificate location:
# /etc/letsencrypt/live/yourdomain.com/fullchain.pem
# /etc/letsencrypt/live/yourdomain.com/privkey.pem
```

### Uncomment SSL Lines in Nginx

After certificates are installed, uncomment the SSL lines in Nginx config:

```bash
sudo nano /etc/nginx/sites-available/django_app
```

Uncomment these lines:
```nginx
ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;
```

Test and restart:
```bash
sudo nginx -t
sudo systemctl restart nginx
```

### Auto-Renew Certificates

```bash
# Test auto-renewal
sudo certbot renew --dry-run

# Auto-renewal is typically enabled by default via systemd timer
# Verify:
sudo systemctl status certbot.timer
```

---

## 📊 Monitoring & Maintenance

### Check Service Status

```bash
# Gunicorn
sudo systemctl status gunicorn
sudo journalctl -u gunicorn -n 50 -f  # View logs

# Nginx
sudo systemctl status nginx
tail -f /var/log/nginx/django_error.log

# Django application logs
tail -f /home/djangoapp/Django_Learning/logs/django.log
tail -f /home/djangoapp/Django_Learning/logs/security.log
```

### Database Backups

Schedule regular PostgreSQL backups:

```bash
sudo nano /home/djangoapp/backup_db.sh
```

Add:
```bash
#!/bin/bash
BACKUP_DIR="/home/djangoapp/backups"
DATE=$(date +%Y%m%d_%H%M%S)

mkdir -p $BACKUP_DIR

sudo -u postgres pg_dump django_db | gzip > $BACKUP_DIR/django_db_$DATE.sql.gz

# Keep only last 30 backups
find $BACKUP_DIR -name "django_db_*.sql.gz" -mtime +30 -delete

echo "Database backed up to $BACKUP_DIR/django_db_$DATE.sql.gz"
```

Make executable and schedule with crontab:
```bash
chmod +x /home/djangoapp/backup_db.sh

# Add to crontab (daily at 2 AM)
sudo crontab -e
# Add: 0 2 * * * /home/djangoapp/backup_db.sh
```

### System Monitoring

Install monitoring tools:
```bash
# Monitor logs for errors
sudo apt install -y logwatch

# System health monitoring
sudo apt install -y netdata

# Application error tracking (optional)
# pip install sentry-sdk
```

### Update Application

To update the application from Git:

```bash
# Pull latest changes
cd /home/djangoapp/Django_Learning
git pull origin main

# Activate virtual environment
source venv/bin/activate

# Install any new dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate --settings=First_Site.setting.prod --noinput

# Collect static files
python manage.py collectstatic --noinput --settings=First_Site.setting.prod

# Restart services
sudo systemctl restart gunicorn
sudo systemctl restart nginx
```

---

## 🐛 Troubleshooting

### Gunicorn Won't Start

```bash
# Check logs
sudo journalctl -u gunicorn -n 100

# Test manually
cd /home/djangoapp/Django_Learning
source venv/bin/activate
gunicorn --bind unix:gunicorn.sock First_Site.wsgi:application --settings=First_Site.setting.prod
```

### Nginx 502 Bad Gateway

```bash
# Check Gunicorn is running
sudo systemctl status gunicorn

# Check socket exists
ls -l /home/djangoapp/Django_Learning/gunicorn.sock

# Check Nginx logs
sudo tail -f /var/log/nginx/django_error.log
```

### Database Connection Error

```bash
# Test PostgreSQL connection
sudo -u postgres psql -h localhost -U django_user -d django_db

# Check .env file
cat /home/djangoapp/Django_Learning/.env

# Verify database exists
sudo -u postgres psql -l | grep django_db
```

### Static Files Not Loading

```bash
# Collect static files again
python manage.py collectstatic --clear --noinput --settings=First_Site.setting.prod

# Check ownership
ls -la /home/djangoapp/Django_Learning/staticfiles/

# Check Nginx has read permissions
sudo -u www-data ls /home/djangoapp/Django_Learning/staticfiles/
```

### SSL Certificate Issues

```bash
# Check certificate validity
sudo openssl x509 -in /etc/letsencrypt/live/yourdomain.com/fullchain.pem -text -noout | grep -A 2 "Validity"

# Test SSL configuration
sudo ssl-test yourdomain.com

# Renew certificate manually
sudo certbot renew --force-renewal
```

### Out of Memory

```bash
# Check system memory
free -h

# Reduce Gunicorn workers
# Edit /etc/systemd/system/gunicorn.service
# Change: --workers 3 to --workers 1

sudo systemctl daemon-reload
sudo systemctl restart gunicorn
```

---

## 📞 Support & Next Steps

1. **Monitoring**: Set up error tracking (Sentry)
2. **Caching**: Enable Redis for better performance
3. **CDN**: Use CloudFlare or Cloudfront for static files
4. **Backups**: Test restore procedures regularly
5. **Security**: Run regular security audits
6. **Updates**: Keep system and packages updated

---

**Happy Deployment! 🚀**
