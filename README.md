# 🚀 Django First Site - Complete Blog & Landing Page Platform

A fully functional, production-ready Django web application combining a professional landing page, multi-feature blog, and contact management system with comprehensive security configurations and deployment readiness.

**Project Status:** ✅ Complete & Production-Ready

---

## 📚 Quick Documentation Links

📖 **Essential Guides:**
- ⚡ [Quick Start (5 min)](QUICKSTART.md) - Get running in 5 minutes
- 🚀 [Deployment Guide](DEPLOYMENT.md) - Production deployment (Linux/Nginx/PostgreSQL)
- 🔐 [Security Documentation](SECURITY.md) - All security features explained
- ✅ [Project Status](FINAL_REPORT.md) - Completion report

---

## 📌 Project Title

**Django First Site — Production-Ready Blog & Landing Platform**

---

## 🧭 Project Description

This is a complete, production-ready Django web application featuring a multi-app architecture with a professional landing page, full-featured blog system, user authentication, contact management, and comprehensive security configurations.

The project demonstrates advanced Django concepts including environment-based configuration, database abstraction, security hardening, and deployment readiness. It's designed for learning best practices and for real-world deployment.

---

## 🎯 Key Features

**Complete & Production-Ready:**
- ✅ Multi-app Django architecture
- ✅ Blog system with categories and tags
- ✅ User authentication and authorization
- ✅ Contact form with CAPTCHA protection
- ✅ Newsletter subscription system
- ✅ Admin panel customization
- ✅ Security-hardened for production
- ✅ Environment-based configuration
- ✅ PostgreSQL/MySQL support
- ✅ Comprehensive documentation

---

## 📋 Table of Contents

1. [Quick Start](#quick-start)
2. [Installation](#installation)
3. [Documentation](#documentation)
4. [Technology Stack](#technology-stack)
5. [Security Features](#security-features)
6. [Project Structure](#project-structure)
7. [License](#license)

---

## Quick Start

Get the application running in 5 minutes:

**[👉 Read QUICKSTART.md](QUICKSTART.md)**

Or quick commands:
```bash
git clone https://github.com/yourusername/Django_Learning.git
cd Django_Learning
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver --settings=First_Site.setting.dev
```

Visit: http://localhost:8000

---

## 🏗️ Technology Stack

| Component | Technology |
|-----------|-----------|
| Framework | Django 6.0.1 |
| Database | SQLite (dev), PostgreSQL (prod) |
| Server | Gunicorn + Nginx |
| Frontend | Bootstrap 4, jQuery |
| Rich Text | Summernote |
| Admin | Django Admin + CAPTCHA |

---

## Installation

---

### Step-by-Step

1. **Clone Repository**
   ```bash
   git clone https://github.com/yourusername/Django_Learning.git
   cd Django_Learning
   ```

2. **Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment**
   ```bash
   cp .env.example .env
   # No changes needed for local development!
   ```

5. **Setup Database**
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   python manage.py collectstatic --noinput
   ```

6. **Run Server**
   ```bash
   python manage.py runserver --settings=First_Site.setting.dev
   ```

7. **Access Application**
   - Website: http://localhost:8000
   - Admin: http://localhost:8000/admin
   - Blog: http://localhost:8000/blog

---

## Documentation

Complete guides for all aspects:

### 🚀 For Deployment
**[📖 DEPLOYMENT.md](DEPLOYMENT.md)** - Complete production deployment guide
- Ubuntu/Linux server setup
- PostgreSQL configuration
- Nginx + Gunicorn setup
- SSL/TLS with Let's Encrypt
- Database backups
- Monitoring & maintenance

### 🔐 For Security
**[🛡️ SECURITY.md](SECURITY.md)** - Complete security documentation
- All 12+ security features explained
- OWASP Top 10 protection
- Secrets management
- Database hardening
- Incident response

### ✅ For Project Status
**[📋 FINAL_REPORT.md](FINAL_REPORT.md)** - Project completion report
- All changes made
- Files created/modified
- Status summary
- Next steps

---

## Project Structure

```
Django_Learning/
├── manage.py                 # Django management
├── db.sqlite3               # Dev database
├── requirements.txt         # Dependencies
├── .env                     # Dev config (⚠️ not committed)
├── .env.example             # Config template
│
├── First_Site/              # Main project
│   ├── settings.py         # Base settings
│   ├── urls.py             # URL config
│   └── setting/
│       ├── dev.py          # Dev settings
│       └── prod.py         # Prod settings
│
├── Blog/                   # Blog app
├── accounts/               # Auth app
├── First_App/              # Landing app
├── templates/              # HTML templates
└── statics/                # CSS/JS/Images
```

---

## Security Features

✅ CSRF Protection  
✅ XSS Prevention  
✅ SQL Injection Protection  
✅ Click-jacking Protection  
✅ HTTPS/SSL Support  
✅ Secure Cookies  
✅ Password Hashing  
✅ HTTP Security Headers  
✅ Environment-based Secrets  
✅ Database Security  
✅ CAPTCHA Protection  
✅ Logging System  

---

## Technology Stack

- **Backend:** Django 6.0.1
- **Database:** SQLite (dev) / PostgreSQL (prod)
- **Server:** Gunicorn + Nginx
- **Frontend:** Bootstrap 4, jQuery
- **Rich Text:** Summernote
- **Admin:** Django + CAPTCHA

---

## Features Included

### Blog System
- Create/edit/delete posts
- Categories and tags
- Comments with moderation
- Featured images
- View counting
- Login required option

### User Management
- Registration and login
- Password management
- User profiles
- Admin interface

### Contact & Newsletter
- Contact form with CAPTCHA
- Newsletter subscription
- Email notifications
- Automated responses

### SEO
- XML Sitemaps
- Robots.txt
- Meta tags
- Structured URLs

---

## Deployment

### Quick Checklist
- [ ] Generate new SECRET_KEY
- [ ] Set ALLOWED_HOSTS to your domain
- [ ] Configure PostgreSQL database
- [ ] Set up HTTPS/SSL certificate
- [ ] Configure environment variables
- [ ] Run security check: `python manage.py check --deploy --settings=First_Site.setting.prod`

**👉 [Read DEPLOYMENT.md](DEPLOYMENT.md) for complete guide**

---

## Environment Variables

| Variable | Purpose | Default |
|----------|---------|---------|
| `DEBUG` | Debug mode | `False` (prod) |
| `SECRET_KEY` | Django secret | ⚠️ Must set |
| `ALLOWED_HOSTS` | Allowed domains | ⚠️ Must set |
| `DB_ENGINE` | Database type | `sqlite3` |
| `SECURE_SSL_REDIRECT` | Force HTTPS | `True` (prod) |

**[👉 See .env.example for all variables](.env.example)**

---

## Testing

```bash
# Run security check
python manage.py check --deploy --settings=First_Site.setting.prod

# Run tests
python manage.py test --settings=First_Site.setting.dev

# Check static files
python manage.py collectstatic --noinput
```

---

## Need Help?

1. **Quick Start:** [QUICKSTART.md](QUICKSTART.md) (5 minutes)
2. **Deployment:** [DEPLOYMENT.md](DEPLOYMENT.md) (production setup)
3. **Security:** [SECURITY.md](SECURITY.md) (all features explained)
4. **Status:** [FINAL_REPORT.md](FINAL_REPORT.md) (what's done)

---

## License

MIT License - See [LICENSE](LICENSE) for details

---

## Ready to Use!

This project is **production-ready** with:
- ✅ Professional code organization
- ✅ Comprehensive security
- ✅ Full documentation
- ✅ Deployment-Ready
- ✅ Best practices

**👉 [Start here: QUICKSTART.md](QUICKSTART.md)**

---

**Made with ❤️ for Django learning**
- A template integration reference
- A static-to-Django conversion example
- A backend onboarding checkpoint

---
## Contribution Policy

Currently a solo learning repository.
Suggestions and improvement pull requests are welcome.

---
## License

Educational Use — Learning Project

---
## Author

Kourosh Beheshtinejad — Django track — landing page integration phase complete.

---