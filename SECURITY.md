# 🔐 Security Implementation & Best Practices

Comprehensive documentation of security measures implemented in Django First Site project.

---

## 📋 Table of Contents

1. [Security Overview](#security-overview)
2. [Implemented Security Features](#implemented-security-features)
3. [Environment Variables & Secrets](#environment-variables--secrets)
4. [Database Security](#database-security)
5. [Authentication & Authorization](#authentication--authorization)
6. [Protocol Security](#protocol-security)
7. [Code Security](#code-security)
8. [Infrastructure Security](#infrastructure-security)
9. [Incident Response](#incident-response)
10. [Security Checklist](#security-checklist)

---

## 🛡️ Security Overview

Django First Site implements multiple layers of security to protect against common web vulnerabilities including:

- **OWASP Top 10** vulnerabilities
- SQL Injection attacks
- Cross-Site Scripting (XSS)
- Cross-Site Request Forgery (CSRF)
- Click-jacking attacks
- Insecure data transmission
- Weak password policies
- Unauthorized access

---

## ✨ Implemented Security Features

### 1. CSRF (Cross-Site Request Forgery) Protection

**Implementation:**
```python
# In settings.py
MIDDLEWARE = [
    'django.middleware.csrf.CsrfViewMiddleware',
]

# In templates
{% csrf_token %}  <!-- Added to all forms -->
```

**Details:**
- CSRF tokens generated for each request
- Token validation on state-changing requests (POST, PUT, DELETE)
- Tokens are cryptographically signed
- Token mismatch results in 403 Forbidden error

**Testing:**
```python
# Test CSRF protection
python manage.py test --settings=First_Site.setting.dev
```

---

### 2. SQL Injection Prevention

**Implementation:**
- Uses Django ORM exclusively
- Parameterized queries automatically
- Never concatenates user input directly into SQL

**Example:**
```python
# ✅ SAFE - Using ORM
posts = Post.objects.filter(title__icontains=search_term)

# ❌ NEVER DO THIS
posts = Post.objects.raw(f"SELECT * FROM blog_post WHERE title LIKE '%{search_term}%'")
```

**Mitigation:**
- ORM parameterizes all queries
- Raw SQL should ALWAYS use parameters:
```python
# ✅ SAFE raw SQL
Post.objects.raw('SELECT * FROM blog_post WHERE title LIKE %s', [f'%{term}%'])
```

---

### 3. XSS (Cross-Site Scripting) Protection

**Implementation:**
```python
# In settings.py - Template auto-escaping is ON by default
TEMPLATES = [
    {
        'OPTIONS': {
            'autoescape': True,
        },
    },
]
```

**Template Usage:**
```django
{# ✅ SAFE - Automatically escaped #}
<p>{{ user_input }}</p>

{# ❌ UNSAFE - Only use when absolutely necessary #}
<p>{{ trusted_html|safe }}</p>
```

**Content Types:**
- User-provided content is always escaped
- HTML from rich text editors (Summernote) is sanitized in forms
- JavaScript execution within user content is prevented

---

### 4. Click-jacking (UI Redressing) Protection

**Implementation:**
```python
# In settings.py
MIDDLEWARE = [
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

X_FRAME_OPTIONS = 'DENY'  # Prevents embedding in frames
```

**Effect:**
- Sets `X-Frame-Options: DENY` header
- Prevents site from being loaded in `<iframe>`, `<frame>`, `<embed>`, `<object>`
- Protects against click-jacking attacks

---

### 5. HTTP Security Headers

**Implemented Headers:**

```python
# In settings.py
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

SECURE_CONTENT_SECURITY_POLICY = {
    'default-src': ("'self'",),
    'script-src': ("'self'", "'unsafe-inline'", "cdn.jsdelivr.net"),
    'style-src': ("'self'", "'unsafe-inline'", "cdn.jsdelivr.net"),
    'img-src': ("'self'", "data:", "https:"),
}
```

**Headers Set:**
| Header | Purpose |
|--------|---------|
| `Strict-Transport-Security` | Force HTTPS usage |
| `Content-Security-Policy` | Control resource loading |
| `X-Content-Type-Options` | Prevent MIME sniffing |
| `X-Frame-Options` | Click-jacking protection |
| `X-XSS-Protection` | XSS filter enablement |

---

### 6. Secure Cookie Configuration

**Implementation:**
```python
# In settings.py
CSRF_COOKIE_SECURE = True        # Only send over HTTPS
CSRF_COOKIE_HTTPONLY = True      # Not accessible via JavaScript
SESSION_COOKIE_SECURE = True     # Only send over HTTPS
SESSION_COOKIE_HTTPONLY = True   # Not accessible via JavaScript
SESSION_COOKIE_SAMESITE = 'Strict'  # CSRF protection
```

**Security Implications:**
- Cookies not exposed to XSS attacks
- Cookies only sent over encrypted connections
- Cannot be stolen by network sniffing

---

### 7. Password Security

**Implementation:**
```python
# In settings.py - Password validators
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 8,  # Minimum 8 characters
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]
```

**Password Requirements:**
- ✅ Minimum 8 characters
- ✅ Not similar to user attributes (username, email, etc.)
- ✅ Not in common password list
- ✅ Not entirely numeric
- ✅ Stored as bcrypt/Argon2 hash (not plaintext)

**Enforced At:**
- User registration
- Password change
- Admin user creation

---

### 8. Authentication & Authorization

**Implementation:**
```python
# Login required decorator
from django.contrib.auth.decorators import login_required

@login_required(login_url='login')
def protected_view(request):
    return render(request, 'protected.html')

# Permission required
@permission_required('blog.view_post')
def admin_view(request):
    pass
```

**Features:**
- Django's built-in authentication system
- Session-based authentication
- Password hashing with strong algorithms
- Account lockout after failed attempts (optional)
- Two-factor authentication ready

---

### 9. HTTPS/SSL/TLS Support

**Configuration:**
```python
# In production settings
SECURE_SSL_REDIRECT = True          # Redirect HTTP to HTTPS
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
```

**Certificate Management:**
- Let's Encrypt (free, recommended)
- Auto-renewal via Certbot
- TLS 1.2 or higher only
- Strong cipher suites

---

### 10. Secret Key Management

**Implementation:**
```python
# Never hardcode SECRET_KEY!
import os
from dotenv import load_dotenv

load_dotenv()
SECRET_KEY = os.getenv('SECRET_KEY')

if not SECRET_KEY:
    raise ValueError("SECRET_KEY not set in .env file")
```

**Key Rotation:**
```bash
# Generate new key
python -c 'from django.core.management.utils import get_random_secret_key; \
print(get_random_secret_key())'

# Update .env file with new key
echo "SECRET_KEY=new_generated_key" >> .env
```

---

### 11. CAPTCHA Protection

**Implementations:**
```python
# Admin login protection
MULTI_CAPTCHA_ADMIN = {
    'engine': 'simple-captcha',
}

# Contact form protection
class ContactForm(forms.ModelForm):
    captcha = ReCaptchaField()
```

**Protects Against:**
- Brute force login attempts
- Automated spam
- Bot submissions

---

### 12. Security Middleware Stack

**Active Middleware:**
```python
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',       # HTTP header injection
    'django.contrib.sessions.middleware.SessionMiddleware',  # Session management
    'django.middleware.common.CommonMiddleware',            # Host validation
    'django.middleware.csrf.CsrfViewMiddleware',            # CSRF protection
    'django.contrib.auth.middleware.AuthenticationMiddleware',  # User authentication
    'django.contrib.messages.middleware.MessageMiddleware',  # Message framework
    'django.middleware.clickjacking.XFrameOptionsMiddleware',  # Click-jacking protect
    'debug_toolbar.middleware.DebugToolbarMiddleware',     # Debug (dev only)
]
```

---

## 🔑 Environment Variables & Secrets

### Sensitive Data Management

**Files to NEVER commit:**
```
.env                 # Production secrets
*.pem, *.key        # SSL certificates
db.sqlite3          # Database with data
local_settings.py   # Local overrides
```

**`.env` Template Variables:**
```env
# Core Secrets
SECRET_KEY=<unique-random-value>

# Database Credentials
DB_PASSWORD=<strong-password>

# Email Service
EMAIL_HOST_PASSWORD=<email-app-password>

# API Keys
STRIPE_SECRET_KEY=<stripe-key>
SENTRY_DSN=<sentry-url>
```

### Rotating Secrets

```bash
# 1. Generate new SECRET_KEY
python -c 'from django.core.management.utils import get_random_secret_key; \
print(get_random_secret_key())'

# 2. Update .env file
nano .env

# 3. Restart application
sudo systemctl restart gunicorn

# 4. Verify application works
curl https://yourdomain.com
```

**Best Practices:**
- ✅ Encrypt secrets in version control if needed (sealed-secrets, HashiCorp Vault)
- ✅ Rotate secrets regularly (monthly/quarterly)
- ✅ Use managed secrets services (AWS Secrets Manager, Azure KeyVault)
- ✅ Never share .env files via email or Slack
- ✅ Use environment-specific secrets

---

## 🗄️ Database Security

### PostgreSQL Hardening

**User Permissions:**
```sql
-- Principle of Least Privilege
CREATE USER django_user WITH PASSWORD 'strong_password';
GRANT CONNECT ON DATABASE django_db TO django_user;
GRANT USAGE ON SCHEMA public TO django_user;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO django_user;

-- No superuser rights
ALTER USER django_user NOSUPERUSER;
ALTER USER django_user NOCREATEDB;
```

**Connection Security:**
```python
# In settings.py (production)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'django_db',
        'USER': 'django_user',
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': 'localhost',
        'PORT': '5432',
        'CONN_MAX_AGE': 600,
        'OPTIONS': {
            'sslmode': 'require',  # Enforce SSL connections
        }
    }
}
```

**Backup Security:**
```bash
# Encrypted backups
pg_dump django_db | gpg --symmetric --output backup.sql.gpg

# Secure storage
# - Encrypt backups
# - Store off-site
# - Restrict access to backups
```

### Query Logging

```python
# Monitor database queries
LOGGING = {
    'loggers': {
        'django.db.backends': {
            'level': 'DEBUG',
            'handlers': ['secure_file'],
        },
    },
}
```

---

## 👥 Authentication & Authorization

### User Authentication

**Default Django Auth:**
- PBKDF2 hashing (default)
- Optional Argon2 (recommended)
- Bcrypt support

**Setup Argon2:**
```bash
pip install argon2-cffi

# In settings.py
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.Argon2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
]
```

### Authorization Levels

```python
# Object-level permissions
class BlogPost(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def can_edit(self, user):
        return self.author == user or user.is_staff

# View-level permissions
@permission_required('blog.change_post')
def edit_post(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    return render(request, 'edit_post.html', {'post': post})

# Admin customization
class BlogPostAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            return qs.filter(author=request.user)
        return qs
```

---

## 🔒 Protocol Security

### HTTPS Enforcement

**Nginx Configuration:**
```nginx
# Redirect HTTP to HTTPS
server {
    listen 80;
    server_name yourdomain.com;
    return 301 https://$server_name$request_uri;
}

# HTTPS server
server {
    listen 443 ssl http2;
    
    ssl_certificate /path/to/certificate.pem;
    ssl_certificate_key /path/to/key.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
}
```

### HSTS (HTTP Strict Transport Security)

```python
# In settings.py
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
```

**Effect:**
- Browser remembers to always use HTTPS
- Protection against man-in-the-middle (MITM) attacks
- Prevents protocol downgrading

---

## 💻 Code Security

### Input Validation

```python
# Always validate user input
from django.core.exceptions import ValidationError

class ContactForm(forms.Form):
    email = forms.EmailField()  # Built-in email validation
    message = forms.CharField(
        max_length=1000,
        min_length=10,
    )
    
    def clean_message(self):
        message = self.cleaned_data.get('message', '')
        # Custom validation
        if 'spam_keyword' in message.lower():
            raise ValidationError('Your message contains spam.')
        return message
```

### Output Encoding

```django
{# ✅ Automatically escaped (safe) #}
{{ user_input }}

{# ❌ Only for trusted content #}
{{ html_content|safe }}

{# Better approach: use safe HTML library #}
{{ html_content|truncatewords_html:50 }}
```

### File Upload Security

```python
# Validate uploaded files
class BlogPostForm(forms.ModelForm):
    image = forms.ImageField(
        max_length=25000000,  # 25MB max
        allow_empty_file=False,
    )
    
    def clean_image(self):
        image = self.cleaned_data.get('image')
        
        # Validate file type
        if image:
            if image.size > 5242880:  # 5MB
                raise ValidationError("Image is too large (max 5MB)")
            
            # Check MIME type
            if image.content_type not in ['image/jpeg', 'image/png', 'image/gif']:
                raise ValidationError("Only JPEG, PNG, GIF allowed")
        
        return image
```

---

## 🏗️ Infrastructure Security

### Firewall Configuration

```bash
# Enable UFW firewall
sudo ufw enable
sudo ufw default deny incoming
sudo ufw default allow outgoing

# Allow specific ports
sudo ufw allow 22/tcp     # SSH
sudo ufw allow 80/tcp     # HTTP
sudo ufw allow 443/tcp    # HTTPS

# Check status
sudo ufw status
```

### Access Control

```bash
# SSH hardening
sudo nano /etc/ssh/sshd_config

# Disable password auth (use keys only)
PasswordAuthentication no
PermitRootLogin no
PubkeyAuthentication yes
Protocol 2
Port 22  # Change to unusual port if desired

# Apply changes
sudo systemctl restart sshd
```

### Monitoring

**Failed Login Attempts:**
```bash
sudo tail -f /var/log/auth.log | grep "Failed"
```

**System Updates:**
```bash
# Enable automatic security updates
sudo apt install -y unattended-upgrades
sudo dpkg-reconfigure -plow unattended-upgrades
```

---

## 🚨 Incident Response

### Security Breach Procedure

**If You Suspect a Breach:**

1. **Immediate Actions:**
   ```bash
   # 1. Rotate all secrets immediately
   # 2. Check logs for unauthorized access
   tail -f /var/log/django/security.log
   
   # 3. Check recent git commits
   git log --oneline --all | head -20
   
   # 4. Revoke compromised credentials
   # 5. Notify users if needed
   ```

2. **Investigation:**
   ```bash
   # Check for unauthorized file changes
   sudo aide --init
   sudo aide --check
   
   # Review database access logs
   sudo -u postgres psql -d django_db -c "SELECT * FROM pg_stat_statements;"
   
   # Check for backdoors
   sudo rootkit-hunter --check --skip-keypress
   ```

3. **Recovery:**
   ```bash
   # Restore from backup
   # Redeployment
   # Security updates
   # User notification
   ```

### Logging & Monitoring

```python
# Enhanced security logging
LOGGING = {
    'loggers': {
        'django.security': {
            'handlers': ['security_file'],
            'level': 'WARNING',
        },
    },
}

# Monitor for:
# - Failed login attempts
# - Permission denied errors
# - Suspicious database queries
# - File access anomalies
```

---

## ✅ Security Checklist

### Before Going Live

**Development:**
- [ ] No hardcoded secrets in code
- [ ] All inputs validated
- [ ] All outputs escaped
- [ ] CSRF tokens on all forms
- [ ] Security check passes: `python manage.py check --deploy`

**Deployment:**
- [ ] DEBUG = False
- [ ] SECRET_KEY rotated and in .env
- [ ] ALLOWED_HOSTS configured
- [ ] HTTPS certificate installed
- [ ] SSL/TLS 1.2+ enabled
- [ ] Strong database user permissions
- [ ] Backup system operational
- [ ] Logging configured
- [ ] Firewall configured
- [ ] SSH hardened

**Post-Deployment:**
- [ ] Monitor security logs daily
- [ ] Update Django monthly
- [ ] Update OS security patches
- [ ] Test backup restoration
- [ ] Review access logs weekly
- [ ] Update dependencies

### Regular Maintenance

- [ ] Monthly: Security updates
- [ ] Quarterly: Penetration testing
- [ ] Quarterly: Dependency updates
- [ ] Semi-annually: Security audit
- [ ] Annually: Full security review

---

## 📚 Additional Resources

### Security Documentation
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Django Security](https://docs.djangoproject.com/en/6.0/topics/security/)
- [Django Deployment Checklist](https://docs.djangoproject.com/en/6.0/howto/deployment/checklist/)

### Tools
- [OWASP ZAP](https://www.zaproxy.org/) - Security scanning
- [Snyk](https://snyk.io/) - Dependency vulnerability scanning
- [Bandit](https://bandit.readthedocs.io/) - Python AST security checker
- [Safety](https://safety.io/) - Dependency vulnerability checking

### Practices
- [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework)
- [CIS Security Benchmarks](https://www.cisecurity.org/benchmarks/)
- [Secure Coding Standards](https://www.securecoding.cert.org/)

---

**Always prioritize security. When in doubt, assume the worst and implement defense-in-depth.**

Last Updated: 2026-02-24
