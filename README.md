# 🚀 Django First Site - Complete Blog & Landing Page Platform

---

# 📌 Project Title

**Django Landing Page — Template & Static Integration Phase**

---

# 🧭 Project Description

This repository contains a Django-based web project developed as part of my backend learning path.  
At this stage, the focus is on building a fully functional **multi-page landing website** using Django’s core architectural components — without database models yet — emphasizing template rendering, static asset management, routing, and project structure discipline.

The primary objective of this project is to convert a static HTML landing template into a properly structured Django application and serve it through Django’s template engine and URL dispatcher.

This project demonstrates practical understanding of how frontend assets and layouts are integrated into a backend framework environment.

---

# 🎯 Development Goals of This Phase

This phase of the project was designed to validate and implement the following backend fundamentals:

- Django project & app architecture
- Template rendering pipeline
- Template inheritance system
- Static file serving
- Asset path normalization
- URL routing and naming
- Multi-page navigation
- Template tag usage
- Error debugging in templates
- GitHub project publishing
- Virtual environment usage
- Clean folder organization
- Converting static HTML to Django templates

---

# 🏗️ Core Django Concepts Demonstrated

---

## ✅ Django Project Initialization

- Created Django project using `django-admin startproject`
- Configured settings module
- Verified WSGI entrypoint
- Development server execution tested

---

## ✅ Django App Modularization

Multiple apps registered and configured inside `INSTALLED_APPS`:

- Blog app
- Base app components
- Django contrib modules

Each app maintains separation of concerns and independent template/static directories.

---

## ✅ Template Engine Usage

Django template engine is used to render HTML pages dynamically.

Implemented features:

- Template inheritance
- Base layout reuse
- Block overriding
- Template extension
- Template tags
- Static and URL tag usage

Example pattern used:

```django
{% extends "base.html" %}
{% load static %}

{% block content %}
<!-- page content -->
{% endblock %}
```

---
## ✅ Template Inheritance Strategy
A shared base template defines:
- Header
- Navigation
- Footer
- Global CSS/JS includes

Child templates override content blocks only — ensuring:
- DRY structure
- Maintainability
- Reusability
- Clean layout separation

---

## ✅ Static File Management
Static files are organized using Django static system.
Asset types integrated:
- CSS
- JavaScript
- Images
- Fonts
- Vendor libraries

Static loading pattern:
```django
{% load static %}
<link rel="stylesheet" href="{% static 'blog/css/style.css' %}">
<script src="{% static 'blog/js/main.js' %}"></script>
<img src="{% static 'blog/img/logo.png' %}">
```

---

## ✅ Static Folder Structure Strategy

Static directories organized by responsibility:
```cpp
static/
└── blog/
    ├── css/
    ├── js/
    ├── img/
    └── vendor/
```
This prevents asset collision across apps and keeps namespaces clean.

---

## ✅ URL Routing System

URL dispatcher configured using named routes instead of hardcoded paths.
Benefits:
- Refactor-safe
- Template-safe
- Prevents broken links
- Enables reverse resolution

Example:
```python
path('', views.blog_view, name='index')
path('single', views.single_view, name='single')
```
Template usage:
```django
<a href="{% url 'single' %}">
```

---

## ✅ View Layer (Function-Based Views)

Views are responsible for:
- Receiving HTTP request
- Selecting template
- Returning rendered response

Example:
```python
def blog_view(request):
    return render(request, "blog/blog-home.html")
```
---

## 🎨 Frontend Template Integration Process

A static HTML landing theme was integrated into Django through the following steps:

1. Copied template files into Django templates directory
2. Extracted base layout
3. Created base.html
4. Converted asset paths to Django static tags
5. Converted page links to URL tags
6. Split pages into views
7. Created URL patterns
8. Moved assets into static folders
9. Tested asset loading
10. Debugged template tag errors

---

# 🧪 Debugging Experience Gained

During implementation, multiple real Django errors were encountered and resolved

---
### TemplateSyntaxError
**Cause**: Typo in template tag
```matlab
{% staic %}
```
**Fix**:
```cpp
{% static %}
```
---
### Static File Not Loading

**Cause**: Incorrect path or missing `{% load static %}`
**Fix**: Added static tag loader and corrected paths

---

### 404 URL Errors

**Cause**: HTML file links used instead of Django URL names
**Fix**: Replaced with:
```django
{% url 'route_name' %}
```

---
### Image Not Displaying
**Cause**: Wrong static folder structure
**Fix**x: Reorganized static directories per app namespace

---
## 📂 Full Project Structure
```adruino
Django_Learning/
│
├── manage.py
│
├── First_Site/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── Blog/
│   ├── views.py
│   ├── urls.py
│   ├── apps.py
│   ├── templates/
│   │   └── blog/
│   │       ├── base.html
│   │       ├── blog-home.html
│   │       └── blog-single.html
│   │
│   └── static/
│       └── blog/
│           ├── css/
│           ├── js/
│           └── img/
│
├── templates/
├── statics/
├── media/
├── venv/
└── db.sqlite3
```

---

## ⚙️ Environment Setup Guide

---

### Create Virtual Environment
```nginx
python -m venv venv
```
---

### Activate Environment
##### Windows
```
venv\Scripts\activate
```

##### Linux / Mac
```bash
source venv/bin/activate
```

---

### Install Dependencies
```nginx
pip install django
```

---
### Run Development Server
```nginx
python manage.py runserver
```

---
## 🔧 Key Settings Configuration
---
### Static Settings
```python
STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "statics"]
STATIC_ROOT = BASE_DIR / "static"
```
---

### Template Settings
```python
TEMPLATES = [
    {
        "APP_DIRS": True,
        "DIRS": [BASE_DIR / "templates"],
    }
]
```
---
## 🧭 Page Navigation Map
```css
Landing Page → Blog Home → Single Blog Page
```
Navigation implemented through named URL routing.

---

## 🛠️ Tools & Technologies Used
- Python
- Django
- HTML/CSS Template
- JavaScript
- VS Code
- Git
- GitHub
- Virtualenv
- Chrome DevTools

---
## 📈 Skills Demonstrated

---
### Backend Skills
- Django setup & configuration
- Template engine usage
- Static file pipeline
- URL routing
- View architecture
- Debugging Django errors

---
### Engineering Skills
- Folder structuring
- Naming conventions
- Template refactoring
- Error tracing
- Stack trace reading
- Git version control
- Repository documentation

---
## 🚧 Current Scope Limitations
To keep documentation transparent:
This project **does not yet include**:
- Database models
- Forms processing
- Authentication
- Admin customization
- Dynamic content
- REST APIs
- Deployment config
- Production server setup

This repository represents the **foundation stage** of Django backend learning.

---

## 🔮 Next Development Phases

Planned next milestones:
- Django Models
- Database integration
- CRUD operations
- Forms handling
- Admin panel usage
- Authentication system
- Dynamic blog posts
- REST API layer
- Deployment with Nginx + Gunicorn
- Production static serving

---
## 📚 Educational Value

This project serves as:
- A Django fundamentals milestone
- A template integration reference
- A static-to-Django conversion example
- A backend onboarding checkpoint

---
## 🤝 Contribution Policy

Currently a solo learning repository.
Suggestions and improvement pull requests are welcome.

---
## 📜 License

Educational Use — Learning Project

---
## 👨‍💻 Author

Kourosh Beheshtinejad — Django track — landing page integration phase complete.

---